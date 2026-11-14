"""Data-only LRU cache with actual bytes, write-allocate and WB/WT memory traffic."""
from collections import defaultdict

class Cache:
    def __init__(self,capacity=64,line_size=16,ways=1,write_policy='WB',initial=None):
        assert capacity%line_size==0 and capacity//line_size%ways==0
        assert write_policy in ['WB','WT']
        self.capacity=capacity;self.line_size=line_size;self.ways=ways;self.set_count=capacity//line_size//ways
        self.lines=[[None]*ways for _ in range(self.set_count)]
        self.memory=dict(initial or {});self.clock=0;self.seen=set();self.events=[]
        self.hits=0;self.misses=0;self.writes=0;self.write_policy=write_policy
    def access(self,ref):
        address,size=ref['address'],ref['size'];block=address//self.line_size
        assert block==(address+size-1)//self.line_size,'Split crossing accesses before simulation'
        set_no=block%self.set_count;tag=block//self.set_count;offset=address%self.line_size
        slots=self.lines[set_no];slot=next((j for j,e in enumerate(slots) if e and e['tag']==tag),None)
        hit=slot is not None;evicted=None;dirty_eviction=False;seen_before=block in self.seen
        self.clock+=1
        if hit:self.hits+=1
        else:
            self.misses+=1
            slot=next((j for j,e in enumerate(slots) if e is None),None)
            if slot is None:
                slot=min(range(self.ways),key=lambda j:slots[j]['used']);old=slots[slot];evicted=old['block']*self.line_size
                if old['dirty']:
                    dirty_eviction=True;self.writes+=1
                    base=old['block']*self.line_size
                    self.memory.update({base+j:v for j,v in enumerate(old['data'])})
            base=block*self.line_size
            slots[slot]=dict(tag=tag,block=block,dirty=False,used=self.clock,
                             data=bytearray(self.memory.get(base+j,0) for j in range(self.line_size)))
        entry=slots[slot];entry['used']=self.clock
        if ref['rw']=='R':
            value=int.from_bytes(entry['data'][offset:offset+size],'little')
            assert value==ref['value'],('Cache load differs from original execution',ref,value)
        else:
            data=ref['value'].to_bytes(size,'little');entry['data'][offset:offset+size]=data
            if self.write_policy=='WB':entry['dirty']=True
            else:
                self.writes+=1;self.memory.update({address+j:v for j,v in enumerate(data)})
        self.seen.add(block)
        event=dict(ref,tag=tag,set=set_no,way=slot,offset=offset,hit=hit,evicted=evicted,seen_before=seen_before,dirty_eviction=dirty_eviction)
        self.events.append(event);return event
    def peek(self,address,size):
        values=[]
        for a in range(address,address+size):
            block=a//self.line_size;set_no=block%self.set_count;tag=block//self.set_count
            entry=next((e for e in self.lines[set_no] if e and e['tag']==tag),None)
            values.append(entry['data'][a%self.line_size] if entry else self.memory.get(a,0))
        return int.from_bytes(bytes(values),'little')
    def snapshot(self):
        rows=[]
        for s,slots in enumerate(self.lines):
            order=sorted([e for e in slots if e],key=lambda e:e['used'],reverse=True)
            for way,e in enumerate(slots):
                rows.append(dict(line=s*self.ways+way,set=s,way=way,valid=bool(e),tag=e['tag'] if e else None,
                                 dirty=bool(e and e['dirty']),block=e['block']*self.line_size if e else None,
                                 lru=order.index(e) if e else None))
        return rows
    def summary(self):
        n=self.hits+self.misses;h=self.hits/n if n else 0
        return dict(capacity=self.capacity,line_size=self.line_size,ways=self.ways,sets=self.set_count,
                    references=n,hits=self.hits,misses=self.misses,H=h,memory_writes=self.writes,
                    Ts=1+(1-h)*30,speedup=30/(1+(1-h)*30),dirty_remaining=[r for r in self.snapshot() if r['dirty']])

def direct_steps(refs):
    """Independent first-30 arithmetic worksheet: quotient/remainder and four simple slots."""
    slots=[None]*4;seen=set();rows=[];writes=0
    for ref in refs:
        quotient,offset=divmod(ref['address'],16);tag,index=divmod(quotient,4)
        old=slots[index];hit=old is not None and old[0]==tag
        displaced=None if hit or old is None else (old[0]*4+index)*16
        dirty_evict=bool(not hit and old is not None and old[1])
        writes+=dirty_evict
        dirty=(old[1] if hit else False) or ref['rw']=='W'
        rows.append(dict(number=ref['number'],tag=tag,set=index,offset=offset,hit=hit,evicted=displaced,
                         seen_before=quotient in seen,dirty_eviction=dirty_evict))
        slots[index]=(tag,dirty);seen.add(quotient)
    return rows,slots,writes

def self_test():
    def r(a,rw='R',v=0):return dict(address=a,size=4,rw=rw,value=v)
    c=Cache(32,16,1,'WB');c.access(r(0,'W',7));c.access(r(32));c.access(r(0,v=7))
    assert c.writes==1 and c.memory[0]==7 and c.hits==0 and c.misses==3
    c=Cache(32,16,2,'WB')
    for a in [0,16,0,32]:c.access(r(a))
    assert c.events[-1]['evicted']==16 and c.events[2]['hit']
    c=Cache(32,16,1,'WT');c.access(r(0,'W',7));c.access(r(4,'W',9))
    assert c.writes==2 and c.peek(0,4)==7 and c.peek(4,4)==9
    assert not any(e['dirty'] for e in c.snapshot())
    print('Cache microtests: WB dirty eviction, two-way LRU and WT writes PASS')
if __name__=='__main__':self_test()
