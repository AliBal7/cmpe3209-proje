"""M2: execute both ELFs, map DWARF lines, encode ten RV32IM instructions independently."""
import bisect, csv, hashlib, json, re, shutil, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
deps=ROOT.parent/'tmp/cmpe3209-tools'
if deps.exists():sys.path.insert(0,str(deps))
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_RISCV, CS_MODE_RISCV32
from unicorn import Uc, UC_ARCH_RISCV, UC_MODE_RISCV32, UC_HOOK_CODE
from unicorn.riscv_const import UC_RISCV_REG_SP,UC_RISCV_REG_RA,UC_RISCV_REG_PC

OUT=ROOT/'m2';OUT.mkdir(exist_ok=True)
CS=Cs(CS_ARCH_RISCV,CS_MODE_RISCV32)
def elf_data(path):
    with path.open('rb') as f:
        e=ELFFile(f);text=e.get_section_by_name('.text')
        segments=[(s['p_vaddr'],s.data()) for s in e.iter_segments() if s['p_type']=='PT_LOAD']
        symbols={s.name:s['st_value'] for s in e.get_section_by_name('.symtab').iter_symbols()}
        sections=[{'name':s.name,'address':s['sh_addr'],'bytes':s['sh_size'],'type':s['sh_type']} for s in e.iter_sections() if s['sh_flags']&2]
        rows=[]
        dwarf=e.get_dwarf_info()
        for cu in dwarf.iter_CUs():
            lp=dwarf.line_program_for_CU(cu)
            if not lp:continue
            for ent in lp.get_entries():
                st=ent.state
                if st and not st.end_sequence: rows.append((st.address,st.line))
        rows.sort(key=lambda t:t[0]);starts=[a for a,l in rows]
        instructions=[]
        for ins in CS.disasm(text.data(),text['sh_addr']):
            j=bisect.bisect_right(starts,ins.address)-1
            instructions.append({'address':ins.address,'word':int.from_bytes(ins.bytes,'little'),
                'bytes':bytes(ins.bytes).hex(' '),'mnemonic':ins.mnemonic,'operands':ins.op_str,
                'c_line':rows[j][1] if j>=0 else None})
        assert all(len(i['bytes'].split())==4 for i in instructions),'Compressed instructions forbidden'
        return dict(segments=segments,symbols=symbols,sections=sections,instructions=instructions)

def execute(info):
    u=Uc(UC_ARCH_RISCV,UC_MODE_RISCV32);u.mem_map(0x10000,0x30000);u.mem_map(0x100000,0x10000)
    for address,data in info['segments']:u.mem_write(address,data)
    u.reg_write(UC_RISCV_REG_SP,0x110000);u.reg_write(UC_RISCV_REG_RA,0x3fff0)
    lookup={i['address']:i for i in info['instructions']};trace=[]
    def hook(uc,address,size,_):
        assert size==4;trace.append(lookup[address])
    u.hook_add(UC_HOOK_CODE,hook);u.emu_start(info['symbols']['main'],0x3fff0,count=100000)
    assert u.reg_read(UC_RISCV_REG_PC)==0x3fff0
    def read(name,n=1):
        data=bytes(u.mem_read(info['symbols'][name],4*n))
        v=[int.from_bytes(data[j:j+4],'little',signed=True) for j in range(0,len(data),4)]
        return v if n>1 else v[0]
    return {'trace':trace,'outputs':{k:read(k,5 if k=='bucket' else 1) for k in ['bucket','mean','below_count','pass_count']},'grades':read('grades',30)}

def stats(seq):
    regs=set()
    for ins in seq:
        regs.update(re.findall(r'\b(?:ra|sp|gp|tp|zero|s(?:[0-9]|10|11)|a[0-7]|t[0-6])\b',ins['operands']))
    regs.discard('zero')
    return {'instructions':len(seq),'loads':sum(i['mnemonic'] in ['lw','lbu','lb','lh','lhu'] for i in seq),
            'stores':sum(i['mnemonic'] in ['sw','sh','sb'] for i in seq),'registers':sorted(regs),'register_count':len(regs)}

def field(name,hi,lo,value):return {'name':name,'bits':f'{hi}:{lo}' if hi!=lo else str(hi),'binary':f'{value:0{hi-lo+1}b}'}
def encode(op,rd=0,rs1=0,rs2=0,imm=0):
    # Semantic inputs are specified below. No bits are copied from the original machine word.
    if op in ['lui','auipc']:
        opcode=0x37 if op=='lui' else 0x17
        fs=[field('imm[31:12]',31,12,imm&0xfffff),field('rd',11,7,rd),field('opcode',6,0,opcode)]
        word=((imm&0xfffff)<<12)|(rd<<7)|opcode;fmt='U'
    elif op=='mul':
        fs=[field('funct7',31,25,1),field('rs2',24,20,rs2),field('rs1',19,15,rs1),field('funct3',14,12,0),field('rd',11,7,rd),field('opcode',6,0,0x33)]
        word=(1<<25)|(rs2<<20)|(rs1<<15)|(rd<<7)|0x33;fmt='R'
    elif op in ['addi','ori','lw','jalr']:
        opcode={'addi':0x13,'ori':0x13,'lw':3,'jalr':0x67}[op]
        funct3={'addi':0,'ori':6,'lw':2,'jalr':0}[op]
        assert -2048<=imm<=2047
        fs=[field('imm[11:0]',31,20,imm&0xfff),field('rs1',19,15,rs1),field('funct3',14,12,funct3),field('rd',11,7,rd),field('opcode',6,0,opcode)]
        word=((imm&0xfff)<<20)|(rs1<<15)|(funct3<<12)|(rd<<7)|opcode;fmt='I'
    elif op=='sw':
        v=imm&0xfff
        fs=[field('imm[11:5]',31,25,v>>5),field('rs2',24,20,rs2),field('rs1',19,15,rs1),field('funct3',14,12,2),field('imm[4:0]',11,7,v&31),field('opcode',6,0,0x23)]
        word=((v>>5)<<25)|(rs2<<20)|(rs1<<15)|(2<<12)|((v&31)<<7)|0x23;fmt='S'
    elif op=='blt':
        assert imm%2==0 and -4096<=imm<=4094;v=imm&0x1fff
        fs=[field('imm[12]',31,31,(v>>12)&1),field('imm[10:5]',30,25,(v>>5)&63),field('rs2',24,20,rs2),field('rs1',19,15,rs1),field('funct3',14,12,4),field('imm[4:1]',11,8,(v>>1)&15),field('imm[11]',7,7,(v>>11)&1),field('opcode',6,0,0x63)]
        word=(((v>>12)&1)<<31)|(((v>>5)&63)<<25)|(rs2<<20)|(rs1<<15)|(4<<12)|(((v>>1)&15)<<8)|(((v>>11)&1)<<7)|0x63;fmt='B'
    elif op=='jal':
        assert imm%2==0 and -(1<<20)<=imm<(1<<20);v=imm&0x1fffff
        fs=[field('imm[20]',31,31,(v>>20)&1),field('imm[10:1]',30,21,(v>>1)&1023),field('imm[11]',20,20,(v>>11)&1),field('imm[19:12]',19,12,(v>>12)&255),field('rd',11,7,rd),field('opcode',6,0,0x6f)]
        word=(((v>>20)&1)<<31)|(((v>>1)&1023)<<21)|(((v>>11)&1)<<20)|(((v>>12)&255)<<12)|(rd<<7)|0x6f;fmt='J'
    else:raise ValueError(op)
    assert sum(int(f['bits'].split(':')[0])-int(f['bits'].split(':')[-1])+1 for f in fs)==32
    return word,fmt,fs

def asm_source_lines(path):
    source=0;result={}
    for no,line in enumerate(path.read_text().splitlines(),1):
        m=re.match(r'\s*\.loc\s+\d+\s+(\d+)',line)
        if m:source=int(m[1]);continue
        if re.match(r'^\s+[a-z][a-z0-9]*\s',line):result.setdefault(source,[]).append(no)
    return result
def compact(values):
    values=sorted(set(values));parts=[]
    for v in values:
        if not parts or v!=parts[-1][-1]+1:parts.append([v])
        else:parts[-1].append(v)
    return ','.join(str(p[0]) if len(p)==1 else f'{p[0]}-{p[-1]}' for p in parts)

def main():
    infos={k:elf_data(ROOT/f'evidence/main_{k}.elf') for k in ['O0','O1']}
    runs={k:execute(i) for k,i in infos.items()}
    expected={'bucket':[14,1,7,0,8],'mean':51,'below_count':14,'pass_count':15}
    for k,r in runs.items():assert r['outputs']==expected
    assert runs['O0']['grades']==runs['O1']['grades']
    m1=json.loads((ROOT/'evidence/verification.json').read_text())
    trace0=runs['O0']['trace'];start=next(i for i,t in enumerate(trace0) if t['address']==int(m1['kernel_first'],16))
    kernel0=trace0[start:start+20]
    assert [x['address'] for x in kernel0]==[x['address'] for x in m1['kernel']]
    # Same input-ready -> result-ready logical operation after inlining in main.
    trace1=runs['O1']['trace'];start1=next(i for i,t in enumerate(trace1) if t['address']==0x10178)
    kernel1=trace1[start1:start1+3]
    assert [x['mnemonic'] for x in kernel1]==['slt','slli','or']
    specs=[
        (0x10060,'lui',dict(rd=10,imm=0x12c),'SID üst 20 bit'),
        (0x10064,'addi',dict(rd=10,rs1=10,imm=1206),'SID alt 12 bit'),
        (0x100a4,'mul',dict(rd=10,rs1=10,rs2=11),'LCG çarpması'),
        (0x10018,'lw',dict(rd=10,rs1=8,imm=-12),'Notu stack üzerinden yükle'),
        (0x10034,'sw',dict(rs1=8,rs2=10,imm=-12),'İşaretli notu stack’e yaz'),
        (0x10020,'blt',dict(rs1=10,rs2=11,imm=8),'Ortalamanın altı: branch'),
        (0x10028,'jal',dict(rd=0,imm=4),'j sözde komutu: jal x0,+4'),
        (0x102d0,'auipc',dict(rd=1,imm=0),'call çiftinin üst kısmı'),
        (0x102d4,'jalr',dict(rd=1,rs1=1,imm=-720),'mark_below çağrısı'),
        (0x10030,'ori',dict(rd=10,rs1=10,imm=256),'8. biti set et'),
    ]
    lookup={i['address']:i for i in infos['O0']['instructions']};enc=[]
    for n,(address,op,args,purpose) in enumerate(specs,1):
        word,fmt,fields=encode(op,**args);actual=lookup[address]
        assert word==actual['word'],(address,op,hex(word),actual)
        enc.append(dict(number=n,address=f'0x{address:08X}',assembly=actual['mnemonic']+' '+actual['operands'],op=op,arguments=args,format=fmt,
            fields=fields,binary=f'{word:032b}',word=f'0x{word:08X}',bytes=word.to_bytes(4,'little').hex(' '),purpose=purpose,verified=True))
    assert set(x['format'] for x in enc)==set('RISBUJ')
    asm_map=asm_source_lines(ROOT/'evidence/asm_O0.s');lines=(ROOT/'main.c').read_text().splitlines();mapping=[]
    for n,line in enumerate(lines,1):
        ii=[i for i in infos['O0']['instructions'] if i['c_line']==n]
        addresses=[f"0x{x['address']:08X}" for x in ii]
        note=''
        if not ii:note='Bağımsız yürütülebilir instruction yok (bildirim/etiket/yorum/parantez).'
        if n==2:note='SID: .rodata; ayrıca C16 başlangıcı için lui/addi ile sabit katlanır.'
        if n==3:note='N=30 derleme zamanı sabiti; döngü limitlerine gömülür.'
        if n in [4,5]:note='Global diziler/sonuçlar .bss içindedir; başlangıç sıfırdır.'
        mapping.append(dict(c_line=n,source=line,asm_lines=compact(asm_map.get(n,[])),addresses=addresses,note=note))
    for opt in ['O0','O1']:
        shutil.copy2(ROOT/f'evidence/asm_{opt}.s',ROOT/f'asm_{opt}.s')
        (OUT/f'disassembly_{opt}.txt').write_text('\n'.join(f"0x{i['address']:08X}  {i['word']:08x}  {i['mnemonic']:<6} {i['operands']:<26} C:{i['c_line']}" for i in infos[opt]['instructions'])+'\n',encoding='utf-8')
    with (OUT/'c_to_assembly.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['c_line','C_source','asm_O0_s_lines','ELF_instruction_addresses','note'])
        for m in mapping:w.writerow([m['c_line'],m['source'],m['asm_lines'],';'.join(m['addresses']),m['note']])
    with (OUT/'machine_code.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['number','address','assembly','format','word','little_endian_bytes','verified'])
        for e in enc:w.writerow([e[k] for k in ['number','address','assembly','format','word','bytes','verified']])
    result={'compiler':'Clang 18.1.6 (Zig 0.13.0)','source_sha256':hashlib.sha256((ROOT/'main.c').read_bytes()).hexdigest(),
        'outputs':expected,'all_grades_match':True,'encoding_match_count':len(enc),'encodings':enc,'mapping':mapping,
        'sections':{k:infos[k]['sections'] for k in infos},
        'kernel':{'O0':kernel0,'O1':kernel1,'O0_stats':stats(kernel0),'O1_stats':stats(kernel1),
                  'definition':'C7-12: input-ready -> result-ready mark_below operation for i=0 (7<51). O0 uses approved 20-instruction M1 window; O1 inlines it into main (3 instructions). AUIPC setup before M1 window is excluded; including it gives O0=21.'},
        'program':{k:{'dynamic':stats(runs[k]['trace']),'static_instructions':len(infos[k]['instructions']),
                      'output_addresses':{name:f"0x{infos[k]['symbols'][name]:08X}" for name in expected}} for k in infos}}
    (OUT/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['outputs','all_grades_match','encoding_match_count','program']},ensure_ascii=False,indent=2))
    print('KERNEL',result['kernel']['O0_stats'],result['kernel']['O1_stats'])
if __name__=='__main__':main()
