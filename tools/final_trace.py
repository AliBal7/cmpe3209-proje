"""Instruction-by-instruction RV32IM execution, register changes and full DATA trace."""
import csv, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
deps=ROOT.parent/'tmp/cmpe3209-tools'
if deps.exists():sys.path.insert(0,str(deps))
sys.path.insert(0,str(ROOT/'tools'))
from m2_analysis import elf_data
from unicorn import Uc,UC_ARCH_RISCV,UC_MODE_RISCV32,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_MEM_READ
from unicorn.riscv_const import UC_RISCV_REG_SP,UC_RISCV_REG_RA,UC_RISCV_REG_PC,UC_RISCV_REG_X0

REGS=['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1','a0','a1','a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']
def category(word):
    op=word&127
    if op==3:return 'Load'
    if op==0x23:return 'Store'
    if op in (0x63,0x6f,0x67):return 'Branch/jump'
    if op==0x33 and (word>>25)==1:
        assert ((word>>12)&7)<=3,'Unexpected division: define its CPI explicitly'
        return 'Çarpma'
    return 'ALU'
def reference():
    x=1230006;values=[]
    for _ in range(30):
        x=(1664525*x+1013904223)&0xffffffff;values.append((x>>16)%101)
    mean=sum(values)//30
    outputs=dict(bucket=[sum(lo<=v<=hi for v in values) for lo,hi in [(0,49),(50,64),(65,74),(75,84),(85,100)]],
                 mean=mean,below_count=sum(v<mean for v in values),pass_count=sum(v>=56 for v in values))
    return outputs,[v|256 if v<mean else v for v in values]
def execute(path):
    info=elf_data(path);lookup={x['address']:x for x in info['instructions']}
    uc=Uc(UC_ARCH_RISCV,UC_MODE_RISCV32);uc.mem_map(0x10000,0x30000);uc.mem_map(0x100000,0x10000)
    initial={}
    for address,data in info['segments']:
        uc.mem_write(address,data)
        initial.update({address+j:b for j,b in enumerate(data) if b})
    uc.reg_write(UC_RISCV_REG_SP,0x110000);uc.reg_write(UC_RISCV_REG_RA,0x3fff0)
    instructions=[];refs=[]
    def regs():return {name:uc.reg_read(UC_RISCV_REG_X0+i)&0xffffffff for i,name in enumerate(REGS)}
    def finish(next_pc):
        if not instructions:return
        row=instructions[-1];after=regs();row['after']=after;row['next_pc']=next_pc
        row['changed']={k:after[k] for k in after if after[k]!=row['before'][k]}
    def code_hook(machine,address,size,_):
        finish(address);assert size==4
        item=dict(lookup[address]);item.update(number=len(instructions)+1,before=regs(),memory=[],category=category(item['word']))
        instructions.append(item)
    def memory_hook(machine,access,address,size,value,_):
        row=instructions[-1];rw='R' if access==UC_MEM_READ else 'W'
        if rw=='R':value=int.from_bytes(machine.mem_read(address,size),'little')
        value &= (1<<(8*size))-1
        ref=dict(number=len(refs)+1,rw=rw,address=address,size=size,value=value,c_line=row['c_line'],
                 stack=0x100000<=address<0x110000,pc=row['address'],instruction=row['number'])
        refs.append(ref);row['memory'].append(ref['number'])
    uc.hook_add(UC_HOOK_CODE,code_hook)
    uc.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,memory_hook)
    uc.emu_start(info['symbols']['main'],0x3fff0,count=200000)
    assert uc.reg_read(UC_RISCV_REG_PC)==0x3fff0;finish(0x3fff0)
    def read(name,n):
        b=bytes(uc.mem_read(info['symbols'][name],4*n));v=[int.from_bytes(b[j:j+4],'little',signed=True) for j in range(0,len(b),4)]
        return v if n>1 else v[0]
    outputs={k:read(k,5 if k=='bucket' else 1) for k in ['bucket','mean','below_count','pass_count']}
    grades=read('grades',30);expected,expected_grades=reference()
    assert outputs==expected and grades==expected_grades,(outputs,expected)
    return dict(info=info,instructions=instructions,refs=refs,initial=initial,outputs=outputs,grades=grades)
def export_csv(refs,path):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['sira','RW','adres_hex','boyut','c_satiri','stack_mi','pc_hex','instruction_no','value_hex'])
        for r in refs:w.writerow([r['number'],r['rw'],f"0x{r['address']:08X}",r['size'],r['c_line'],int(r['stack']),f"0x{r['pc']:08X}",r['instruction'],f"0x{r['value']:0{r['size']*2}X}"])
if __name__=='__main__':
    out=ROOT/'final';out.mkdir(exist_ok=True)
    for level in ['O0','O1']:
        r=execute(ROOT/f'evidence/main_{level}.elf');export_csv(r['refs'],out/f'trace_{level}.csv')
        print(level,len(r['instructions']),len(r['refs']),r['outputs'])
