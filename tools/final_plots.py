"""Standalone scientific figures for cache tradeoffs and interrupt ordering."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT.parent/'tmp/cmpe3209-tools'
if D.exists():sys.path.insert(0,str(D))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=json.loads((ROOT/'final/analysis.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(11.6,4.1),constrained_layout=True)
for ax,data,title in [(axes[0],A['mapping_sweep'],'Mapping (64 B cache, 16 B line)'),(axes[1],A['line_sweep'],'Line boyu (64 B cache, direct)')]:
    labels=[x['name'].replace('Fully associative','Fully assoc.') for x in data];values=[100*x['H'] for x in data]
    bars=ax.bar(labels,values,color=['#24617b','#398b8f','#6a9476','#b08245'])
    ax.bar_label(bars,labels=[f'{v:.2f}%' for v in values],padding=3,fontsize=9)
    ax.set_ylim(0,100);ax.set_ylabel('Hit oranı (%)');ax.set_title(title,fontweight='bold');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.suptitle('G2 / -O0: aynı 1490 data erişimi, write-back + write-allocate\nAssociative yapılarda LRU; cache başlangıçta boş',fontsize=11)
fig.savefig(ROOT/'final/cache_design_space.png',dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(11.5,3.4),constrained_layout=True)
colors={'A':'#24617b','B':'#cc7543','Program':'#718778'}
rows=[('Sequential (MIE=0)',0,[(0,2,'A'),(2,4,'B')]),('Nested (öncelik B>A)',1,[(0,1,'A'),(1,2,'B'),(2,4,'A')])]
for name,y,segments in rows:
    for begin,end,label in segments:
        ax.barh(y,end-begin,left=begin,height=.42,color=colors[label]);ax.text((begin+end)/2,y,f'ISR {label}',ha='center',va='center',color='white',weight='bold')
    ax.text(4.05,y,'Program: 0x00010014',va='center',fontsize=9)
ax.set_yticks([0,1],[r[0] for r in rows]);ax.invert_yaxis();ax.set_xticks(range(5),['t0: A','t1: B','t2','t3','t4']);ax.set_xlim(-.1,5.8)
ax.set_title('İkinci interrupt: bekletme ve iç içe işleme\nSembolik zaman; gerçek cycle ölçümü değildir.',fontweight='bold');ax.grid(axis='x',alpha=.2)
fig.savefig(ROOT/'final/interrupt_timeline.png',dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(11.8,3.2),constrained_layout=True);ax.axis('off')
boxes=[(.01,.4,'Çekirdek / cache\nBellek denetleyicisi'),(.27,.4,'QPI\nPacket → flit → phit'),(.52,.4,'IOH / root complex\nQPI ↔ PCIe çevirisi'),(.78,.4,'PCIe endpoint\nTLP / DLLP / PHY')]
for x,y,text in boxes:ax.text(x+.10,y+.16,text,ha='center',va='center',fontsize=10,bbox=dict(boxstyle='round,pad=.65',fc='#eef3f5',ec='#24617b'))
for x in [.18,.44,.69]:ax.annotate('',xy=(x+.08,.56),xytext=(x,.56),arrowprops=dict(arrowstyle='->',lw=1.6,color='#24617b'))
ax.text(.5,.04,'Stallings Fig. 3.17 / 3.21 topolojisi için kavramsal örnek. RV32IM ISA, QPI donanımını zorunlu kılmaz.',ha='center',fontsize=9)
fig.savefig(ROOT/'final/interconnect_path.png',dpi=180);plt.close(fig)
print('Wrote cache_design_space.png, interrupt_timeline.png and interconnect_path.png')
