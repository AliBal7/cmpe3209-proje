"""M3 + M4/final: actual traces, two independent first-30 models, cache replay and timing."""
import csv, json, math, shutil, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from final_trace import execute,export_csv,reference
from cache_sim import Cache,direct_steps,self_test

OUT=ROOT/'final';OUT.mkdir(exist_ok=True)
CPI={'ALU':1,'Çarpma':3,'Load':1,'Store':1,'Branch/jump':2}
F_GHZ=1.6;TAU_NS=1/F_GHZ;T2=30
def hex8(v):return f'0x{v:08X}'
def evaluate(run,capacity=64,line_size=16,ways=1,write_policy='WB'):
    cache=Cache(capacity,line_size,ways,write_policy,run['initial'])
    for ref in run['refs']:cache.access(ref)
    symbols=run['info']['symbols'];actual={}
    for name in ['bucket','mean','below_count','pass_count']:
        count=5 if name=='bucket' else 1
        values=[cache.peek(symbols[name]+4*i,4) for i in range(count)]
        actual[name]=values if count>1 else values[0]
    assert actual==run['outputs'],('Y7 changed with cache',capacity,line_size,ways,write_policy,actual)
    assert [cache.peek(symbols['grades']+4*i,4) for i in range(30)]==run['grades']
    return cache
def performance(run,cache):
    classes=Counter(i['category'] for i in run['instructions']);ic=len(run['instructions']);base=sum(classes[k]*CPI[k] for k in classes)
    n=len(run['refs']);summary=cache.summary();cycles_cache=base+n+cache.misses*T2
    assert abs(cycles_cache-(base+n*summary['Ts']))<1e-8
    return dict(classes=dict(classes),Ic=ic,base_cycles=base,CPI=base/ic,tau_ns=TAU_NS,
                T_base_ns=base*TAU_NS,MIPS=F_GHZ*1000/(base/ic),m=n/ic,
                T_no_cache_ns=(base+n*T2)*TAU_NS,T_cache_ns=cycles_cache*TAU_NS,
                cache_cycles=cycles_cache,Ts=summary['Ts'],H=summary['H'],data_references=n,
                cache_speedup=(base+n*T2)/cycles_cache)
def export_events(events,path):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        names=['number','rw','address','tag','set','way','offset','hit','evicted','seen_before','dirty_eviction']
        w=csv.writer(f);w.writerow(names)
        for e in events:w.writerow([hex8(e[k]) if k in ['address','tag','evicted'] and e.get(k) is not None else e.get(k,'-') for k in names])
def model_states(ins,mem):
    base='iac, if, iod'
    if ins['category']=='Load':return base+', oac, of'
    if ins['category']=='Store':return base+', oac, os'
    return base+', do'
def kernel_rows(run,cache):
    approved=json.loads((ROOT/'evidence/verification.json').read_text())['kernel']
    expected_pcs=[i['address'] for i in approved]
    start=next(i for i,r in enumerate(run['instructions']) if r['address']==expected_pcs[0])
    selected=run['instructions'][start:start+20]
    assert [i['address'] for i in selected]==expected_pcs
    refs={r['number']:r for r in run['refs']};events={r['number']:r for r in cache.events};rows=[]
    for n,ins in enumerate(selected,1):
        mem=[refs[k] for k in ins['memory']]
        bus=[dict(type='IF',address=ins['address'],data=ins['word'],control='Memory read; ACK; Clock')]
        for r in mem:bus.append(dict(type=r['rw'],address=r['address'],data=r['value'],control=('Memory read' if r['rw']=='R' else 'Memory write')+'; ACK; Clock'))
        mbr=[ins['word']]+[r['value'] for r in mem]
        alu=ins['mnemonic']+' '+ins['operands']
        if ins['category'] in ['Load','Store']:alu='EA='+hex8(mem[0]['address'])
        row=dict(number=n,pc_before=ins['address'],pc_fetch_next=(ins['address']+4)&0xffffffff,
                 pc_after=ins['next_pc'],assembly=ins['mnemonic']+' '+ins['operands'],IR=ins['word'],
                 states=model_states(ins,mem),MAR=[b['address'] for b in bus],MBR=mbr,ALU=alu,
                 changed=ins['changed'],before=ins['before'],after=ins['after'],bus=bus,
                 category='PM' if mem else 'C' if ins['category']=='Branch/jump' else 'DP',
                 data_refs=mem,cache=[dict(number=k,hit=events[k]['hit']) for k in ins['memory']])
        rows.append(row)
    return rows
def main():
    self_test()
    runs={name:execute(path) for name,path in [('O0',ROOT/'evidence/main_O0.elf'),('O1',ROOT/'evidence/main_O1.elf'),('V2',OUT/'main_v2_O0.elf')]}
    for k,r in runs.items():export_csv(r['refs'],OUT/f'trace_{k}.csv')
    shutil.copy2(OUT/'trace_O0.csv',ROOT/'trace.csv')
    caches={k:evaluate(r) for k,r in runs.items()}
    assert len(runs['O0']['refs'])==1490 and len(runs['O1']['refs'])==193
    for key in runs:assert runs[key]['outputs']==runs['O0']['outputs'] and runs[key]['grades']==runs['O0']['grades']
    first=Cache(initial=runs['O0']['initial'])
    for ref in runs['O0']['refs'][:30]:first.access(ref)
    manual,slots,manual_writes=direct_steps(runs['O0']['refs'][:30])
    for a,b in zip(manual,first.events):
        for k in ['tag','set','offset','hit','evicted','seen_before','dirty_eviction']:assert a[k]==b[k],(k,a,b)
    assert manual_writes==first.writes
    export_events(first.events,OUT/'cache_first30.csv');export_events(caches['O0'].events,OUT/'cache_full.csv')
    (OUT/'cache_first30_independent.json').write_text(json.dumps(dict(rows=manual,slots=slots,memory_writes=manual_writes),indent=2),encoding='utf-8')
    mapping=[]
    for name,ways in [('Direct',1),('2-way',2),('4-way',4),('Fully associative',4)]:
        c=evaluate(runs['O0'],ways=ways);mapping.append(dict(name=name,**c.summary(),outputs=runs['O0']['outputs']))
    lines=[]
    for line_size in [8,16,32,64]:
        c=evaluate(runs['O0'],line_size=line_size);lines.append(dict(name=f'{line_size} B',**c.summary(),outputs=runs['O0']['outputs']))
    extras=[]
    for capacity,policy in [(128,'WB'),(256,'WB'),(64,'WT')]:
        c=evaluate(runs['O0'],capacity=capacity,write_policy=policy);extras.append(dict(policy=policy,**c.summary(),outputs=runs['O0']['outputs']))
    perf={k:performance(r,caches[k]) for k,r in runs.items()}
    kernel=kernel_rows(runs['O0'],caches['O0'])
    krow=kernel[5];assert krow['assembly'].startswith('sw a0') and krow['pc_after']==0x10014
    first5=[];seen=set()
    for ref in runs['O0']['refs']:
        a=ref['address']
        if a not in seen:
            seen.add(a);first5.append(dict(address=a,binary=f'{a:032b}',tag=a>>6,line=(a>>4)&3,offset=a&15))
        if len(first5)==5:break
    counts=Counter((e['evicted'],e['address']//16*16,e['set']) for e in caches['O0'].events if e['evicted'] is not None)
    conflicts=[dict(old=old,new=new,line=line,count=n) for (old,new,line),n in counts.most_common(6)]
    fa=evaluate(runs['O0'],ways=4)
    protected=[dict(number=d['number'],address=d['address'],pc=d['pc'],fa_evicted=f['evicted']) for d,f in zip(caches['O0'].events,fa.events) if d['hit'] and not f['hit']]
    reverse=sum(not d['hit'] and f['hit'] for d,f in zip(caches['O0'].events,fa.events))
    assert len(protected)-reverse==fa.misses-caches['O0'].misses
    # Amdahl: phase includes the final loop and its helper; account for actual misses in that phase.
    phase_ids={i['number'] for i in runs['O0']['instructions'] if (i['c_line'] in range(33,38) or i['address']<0x10050)}
    phase_cpu=sum(CPI[i['category']] for i in runs['O0']['instructions'] if i['number'] in phase_ids)
    phase_events=[e for e in caches['O0'].events if e['instruction'] in phase_ids]
    phase_cycles=phase_cpu+sum(1+(0 if e['hit'] else T2) for e in phase_events)
    f=phase_cycles/perf['O0']['cache_cycles'];nc=5
    amdahl=dict(c_lines='33-37 ve çağrılan 7-12',phase_instructions=len(phase_ids),phase_references=len(phase_events),
                phase_cycles=phase_cycles,total_cycles=perf['O0']['cache_cycles'],f=f,Nc=nc,
                speedup=1/((1-f)+f/nc),limit=1/(1-f),
                assumption='Iterasyonlar farklı grades[i] hücrelerine yazar; mean salt okunur. below_count için thread-local sayım + reduction gerekir. Reduction ve iş parçacığı maliyeti yok sayılmış ideal üst sınırdır.')
    for key,run in runs.items():
        with (OUT/f'instructions_{key}.csv').open('w',newline='',encoding='utf-8-sig') as fp:
            w=csv.writer(fp);w.writerow(['number','PC','IR','assembly','C_line','class','data_references'])
            for i in run['instructions']:w.writerow([i['number'],hex8(i['address']),hex8(i['word']),i['mnemonic']+' '+i['operands'],i['c_line'],i['category'],len(i['memory'])])
    result=dict(outputs=runs['O0']['outputs'],kernel=kernel,
        kernel_totals=dict(instruction_fetch=20,operand_fetch=sum(len(r['data_refs']) for r in kernel if r['category']=='PM' and r['data_refs'][0]['rw']=='R'),
                           operand_store=sum(len(r['data_refs']) for r in kernel if r['category']=='PM' and r['data_refs'][0]['rw']=='W'),
                           control=[r['number'] for r in kernel if r['category']=='C'],bus32=31,bus16=62),
        interrupt=dict(k=6,kind='I/O',interrupted_pc=krow['pc_before'],instruction=krow['assembly'],resume_pc=krow['pc_after'],
                       mepc=krow['pc_after'],mcause=0x8000000b,mtvec=0x30000,registers_to_preserve=krow['after'],
                       completed_store=krow['data_refs'][0],handler_model='Privileged M-mode scenario, not an injected Unicorn interrupt.'),
        first30=dict(summary=first.summary(),snapshot=first.snapshot(),rows=first.events,independent_match=True),
        fields_first5=first5,mapping_sweep=mapping,line_sweep=lines,extra_configurations=extras,
        cache={k:c.summary() for k,c in caches.items()},performance=perf,amdahl=amdahl,
        conflicts=conflicts,associativity_tradeoff=dict(direct_hit_fa_miss=len(protected),direct_miss_fa_hit=reverse,examples=protected[:3]),all_cache_outputs_invariant=True,
        trace_stats={k:dict(references=len(r['refs']),loads=sum(e['rw']=='R' for e in r['refs']),stores=sum(e['rw']=='W' for e in r['refs']),
                            stack=sum(e['stack'] for e in r['refs']),array=sum(r['info']['symbols']['grades']<=e['address']<r['info']['symbols']['grades']+120 for e in r['refs'])) for k,r in runs.items()},
        symbols={k:{name:addr for name,addr in r['info']['symbols'].items() if name in ['grades','bucket','mean','below_count','pass_count','main','mark_below']} for k,r in runs.items()},
        speedup_O0_O1=perf['O0']['T_cache_ns']/perf['O1']['T_cache_ns'],
        pcie=dict(payload=120,header12=dict(total=140,efficiency=120/140,encoded=120/140*128/130),
                  header16=dict(total=148,efficiency=120/148,encoded=120/148*128/130)))
    (OUT/'analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in ['cache','trace_stats','performance','amdahl','kernel_totals','speedup_O0_O1']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
