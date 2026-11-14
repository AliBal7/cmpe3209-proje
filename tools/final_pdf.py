"""Fill all remaining official pages and append reproducible final evidence."""
import csv,html,io,json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader,PdfWriter
from final_content import TEXT,IAS,ARCH,SOURCES

ROOT=Path(__file__).resolve().parents[1];F=ROOT/'final'
TMP=ROOT.parent/'tmp/pdfs/final';TMP.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'pdf/Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf'
A=json.loads((F/'analysis.json').read_text(encoding='utf-8'))
for n,f in [('FA','arial.ttf'),('FB','arialbd.ttf'),('FM','CascadiaMono.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
styles={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=lead,spaceAfter=after) for k,font,size,lead,after in [('h','FB',14,18,10),('sub','FB',10,13,7),('p','FA',9,12,7),('s','FA',7,8.4,0),('tiny','FA',6.2,7.2,0),('mono','FM',7,9,5)]}
def P(t,k='p'):return Paragraph(html.escape(str(t)).replace('\n','<br/>'),styles[k])
def hx(n):return f'{n:08X}'
def table(rows,widths,kind='s'):
    t=Table([[P(v,kind) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#7b8792')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf0f4')),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t
def footer(c,d):
    c.setFont('FA',7);c.drawString(42,25,'Ali Bal | 5001230006 | CMPE3209 final | M3 + M4');c.drawRightString(d.pagesize[0]-42,25,str(d.page))
def write_doc(path,story,landscape=False):
    SimpleDocTemplate(str(path),pagesize=(792,612) if landscape else (612,792),leftMargin=36 if landscape else 48,rightMargin=36 if landscape else 48,topMargin=38,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
def put(c,t,x,y,w,size=6.8,maxh=21):
    # Original form cells are small; full readable details are also in appendices.
    size0=size
    while True:
        p=Paragraph(html.escape(str(t)).replace('\n','<br/>'),ParagraphStyle('cell',fontName='FA',fontSize=size,leading=size+0.5))
        _,height=p.wrap(w,1000)
        if height<=maxh or size<=4.4:break
        size-=.2
    if height>maxh+1:raise ValueError(('cell overflow',t,x,y,w,height,maxh,size0))
    p.drawOn(c,x,792-y-height)
def overlay(index):
    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(612,792))
    def v(t,x,y,w=65,s=6.8,h=21):put(c,t,x,y,w,s,h)
    def body(t,y,h=29):v(t,72,y,468,7,h)
    def mark(y):v('X',109,y,9,7,12)
    if index in [5,6]:
        if index==5:
            for y in [165.3,181.2,197.1,213.1]:mark(y)
            v('32',211,213,23,8);body(TEXT['real_model_difference'],245,32)
        for row in A['kernel']:
            n=row['number'];idx=5 if n<=15 else 6
            if idx!=index:continue
            y=390.7+(n-1)*22.15 if n<=15 else 75+(n-16)*22.15
            compact_alu=row['ALU'].replace('EA=0x','EA\n').replace('PC=0x','PC\n')
            bus='\n'.join(b['type']+' '+hx(b['address'])+'='+hx(b['data']) for b in row['bus'])+'\nACK/Clock'
            vals=[str(n),hx(row['pc_before'])[-5:]+'\n>'+hx(row['pc_after'])[-5:],row['assembly'].replace(' ','\n',1),hx(row['IR']),row['states'].replace(', ','/'),'\n'.join(hx(a) for a in row['MAR']),'\n'.join(hx(a) for a in row['MBR']),compact_alu,'; '.join(k+'=\n'+hx(z) for k,z in row['written'].items()) or '-',bus,row['category']]
            for t,x,w in zip(vals[1:],[108,152,195,232,277,315,352,395,437,497],[39,39,32,40,33,32,38,37,55,42]):v(t,x,y,w,5.0,21)
        if index==5:v('Tam adres, veri ve fetch/execute PC ayrımı: Ek-F3.A; kaynak: final/kernel_trace.csv.',72,732,468,7,12)
        if index==6:
            for y,t in zip([230,252.2,274.3,296.5],['20','6','5','#1,10,20; Ek-F3.A']):v(t,469,y,70,7)
            steps=[('1','Fetch','300->301','1940','0000','MAR300; MBR1940'),('2','Execute','301','1940','0007','M[940]=7 -> AC'),('3','Fetch','301->302','5941','0007','MAR301; MBR5941'),('4','Execute','302','5941','0107','AC+M[941]=263'),('5','Fetch','302->303','2940','0107','MAR302; MBR2940'),('6','Execute','303','2940','0107','M[940]=0107'),('7','I/O örnek','ayrı','3005','0007','Aygıt5 -> AC'),('8','I/O örnek','ayrı','7006','0007','AC -> Aygıt6')]
            for j,row in enumerate(steps):
                for t,x,w in zip(row[1:],[122,235,277,340,383],[108,37,58,38,156]):v(t,x,376.6+j*22.15,w,6.3)
            v('3',323,598.1,85,8);v('3 (6 F/E adımı)',414,598.1,126,7)
            body('Seçilen lw/ori/sw ile LOAD/ADD/STORE üçlüsü 3 instruction cycle sürer. Bellek transferleri RV32IM:5, hipotetik:6. AC tek ara sonuç register’ıdır; PDP-11 ADD B,A tek instruction olabilir. Opcode 3/7 I/O’dur; Ek-F3.B.',631,30)
            vals=IAS[0]
            for t,x,w in zip(vals[1:],[158,249,398],[86,144,142]):v(t,x,707.8,w,6.4)
    elif index==7:
        for j,row in enumerate(IAS[1:]):
            for t,x,w in zip(row[1:],[158,249,398],[86,144,142]):v(t,x,82+j*22.15,w,6.3)
        v('6',206,214.9,19,8);v('I/O',258,214.9,25,8)
        for y,t in zip([259.2,281.3,303.5,325.6,347.8,369.9,392.1],['0x10010; sw a0,\n-12(s0)','Store bitince; atomik\ninstruction sınırı','0x00010014','mstatus ve kullanılan\nGPR; Ek-F3.C','mepc/mcause/mstatus\nmtvec=0x30000','Priv.20240411 §3.1\nPDF32,40,47-49,57','0x00010014\nsw a1,-16(s0)']):v(t,470,y,70,6.2)
        for y,call,irq in [(458.5,'jalr; program başlatır','Haricî I/O isteği'),(480.7,'ra=0x000102D8; prologue stack','mepc; ISR GPR saklar'),(502.8,'ret / ra; bilinçli algoritma adımı','MRET; şeffaf devam')]:v(call,334,y,131,6.5);v(irq,472,y,68,6.2)
        for y,s,n in [(585,'Program: 1..6, sonra A','Program: 1..6, sonra A'),(609.4,'A çalışır; B pending','A context/CSR saklar; B açılır'),(633.8,'A tamamlanır','B, A’yı keser ve biter'),(658.2,'B çalışır ve biter','A kaldığı yerden biter'),(682.7,'Program 0x10014’ten devam','Program 0x10014’ten devam')]:v(s,263,y,146,6.5,24);v(n,414,y,126,6.5,24)
        v('Ayrıntı ve resmî ISA sayfaları: Ek-F3.C.',72,728,468,7,12)
    elif index==8:
        for y,t,ctl in [(96.3,20,'Memory read; ACK; Clock'),(118.4,6,'Memory read; ACK; Clock'),(140.6,5,'Memory write; ACK; Clock'),(162.8,31,'Cache yok; word-transfer sayısı')]:v(t,333,y,46,8);v(ctl,384,y,156,6.5)
        for y,t,why in [(229.2,'32 bit; 4 GiB','2^32 byte'),(251.4,'62','40 IF+12 R+10 W'),(273.5,'0.5','31/62; 2 kat')]:v(t,406,y,51,7);v(why,463,y,77,6.6)
        v('120',202,295.7,25,8)
        for j,(left,right) in enumerate([(1,1),(2,2),(12,16),(120,120),(0,4),(4,4),(1,1),(140,148),('85.7143%','81.0811%'),('84.3956%','79.8337%')]):v(left,215,340+j*22.15,157,8);v(right,378,340+j*22.15,162,8)
        body('DRAM/denetleyici -> QPI Protocol(packet), Routing, Link(flit), Physical(phit) -> IOH/root complex -> PCIe Transaction(TLP), Data Link(sıra/LCRC ve DLLP), Physical(lane/bit). QPI örneği: 80-bit flit / 20-bit phit. Ayrıntı ve sınırlar: Ek-F3.D.',588,32)
        v('-O0',449,701,91,8)
    elif index==9:
        for y,t in zip([75.2,97.3,119.5,141.6],['1490','988 / 502','1191','150']):v(t,449,y,91,8)
        v('w=4; r=2; s=28; tag=26; d=N/A (Ek-F4.A).',318,163.8,222,6.4,12)
        for j,row in enumerate(A['fields_first5']):
            for t,x,w in zip(['0x'+hx(row['address']),row['binary'][:26]+' | '+row['binary'][26:28]+' | '+row['binary'][28:],hex(row['tag']),row['line'],row['offset']],[72,184,318,375,480],[107,129,52,100,60]):v(t,x,208+j*22.15,w,6.3)
    elif index==10:
        for j,slot in enumerate(A['first30']['snapshot']):
            vals=[j,j,slot['valid'],hex(slot['tag']) if slot['tag'] is not None else '-',slot['dirty'],'N/A (direct)']
            for t,x,w in zip(vals[1:],[112,152,195,263,379],[35,38,62,110,160]):v(t,x,450.5+j*22.15,w,7)
        for j in range(4):v('N/A; cache 4 line içerir.',112,539.1+j*22.15,428,7)
        for y,vals in [(672,['','',1490]),(694.1,[27,27,1230])]:
            for t,x,w in zip(vals,[256,347,440],[86,86,100]):v(t,x,y,w,8)
    if index in [9,10]:
        for e in A['first30']['rows']:
            n=e['number']
            if (index==9)!=(n<=15):continue
            y=376.8+(n-1)*22.15 if n<=15 else 73.6+(n-16)*22.17
            vals=[n,e['rw'],hx(e['address']),hex(e['tag']),e['set'],hex(e['offset']),'H' if e['hit'] else 'M','-' if e['evicted'] is None else hx(e['evicted']),'Evet' if e['seen_before'] else 'Hayır']
            for t,x,w in zip(vals[1:],[108,144,190,226,269,307,351,423],[31,41,31,38,33,39,67,117]):v(t,x,y,w,6.2)
    elif index==11:
        for y,vals in [(73.6,[3,3,260]),(96,['0.9','0.9','0.825503']), (118.2,[0,0,157])]:
            for t,x,w in zip(vals,[256,347,440],[86,86,100]):v(t,x,y,w,8)
        body('Python byte düzeyinde cache simülatörü: tools/cache_sim.py. İlk 30, ayrı dört-slot/bölüm-kalan hesabıyla alan alan karşılaştırıldı. Tam replay’de gerçek load değerleri ve bütün Y7/dizi sonuçları doğrulandı. WB: dirty eviction sayılır; final flush hariçtir.',151,30);mark(185.7)
        v('16',195,229.7,23,8)
        for j,row in enumerate(A['mapping_sweep']):
            for t,x,w in zip([row['hits'],row['misses'],f"{row['H']:.6f}"],[371,426,484],[50,53,56]):v(t,x,251.9+j*22.15,w,7)
        v('Direct',197,362.6,150,8)
        for j,row in enumerate(A['line_sweep']):
            for t,x,w in zip([row['hits'],row['misses'],f"{row['H']:.6f}"],[366,423,483],[51,54,57]):v(t,x,384.8+j*22.15,w,7)
        body('Stack temporal, komşu grades spatial locality sağlar. Büyük line line sayısını düşürür ve çatışmayı artırır. Direct bazı stack bloklarını ortak LRU’dan iyi korur; 4-way her zaman daha iyi değildir. Grafik ve gerçek çakışan adresler: Ek-F4.C.',484,29)
        v('30',266,561,49,8)
        for t,x,w in zip(['0.825503','6.234899','4.811625'],[197,239,323],[39,79,217]):v(t,x,583.1,w,6.6)
        for y,b,a in [(649.6,'if (grades[i]&0x100)','if (v<mean)'),(671.7,'Değişmedi','Y7 + 30 eleman aynı'),(693.9,'0.825503','0.832903')]:v(b,378,y,70,6.1);v(a,455,y,85,6.4)
    elif index==12:
        v('6.234899',378,73.6,70,7);v('6.012903',455,73.6,85,7)
        body('Tek değişiklik C36: if (v<mean). Dizi erişimleri 150->120; stack 1191->1251. H artar ama ek stack hit’leri de paydayı büyütür. Model süre kazancı yalnız %0.2111; dirty write-back 157->165. Ayrıntı: Ek-F4.D.',107,31)
        for j,key in enumerate(['ALU','Çarpma','Load','Store','Branch/jump']):
            for name,x in [('O0',368),('O1',454)]:v(A['performance'][name]['classes'][key],x,208.3+j*22.15,86,8)
        for y,key in [(319.1,'Ic'),(341.2,'CPI')]:
            for name,x in [('O0',368),('O1',454)]:
                z=A['performance'][name][key];v(f'{z:.6f}' if isinstance(z,float) else z,x,y,86,8)
        v('1.6',207,363.4,24,8);v('0.625',274,363.4,32,8)
        for y,key in [(407.7,'T_base_ns'),(429.8,'MIPS'),(454.2,'m'),(476.4,'T_no_cache_ns'),(498.5,'T_cache_ns')]:
            for name,x in [('O0',456),('O1',498)]:v(f"{A['performance'][name][key]:.6f}".rstrip('0').rstrip('.'),x,y,40,6.1)
        v('4.066972',465,565,75,8);v('3.491907',465,587,75,8)
        body('T satırlarının birimi ns, m referans/instruction’dır. O1 daha düşük MIPS’e rağmen az instruction/data erişimiyle daha kısa sürer. Her derleme kendi H/Ts değerini kullanır; instruction fetch base 1 cycle içinde varsayılır. Ek-F5.A.',620,30)
        v('5',198,652.6,23,8);v('C33-37; helper7-12',471,696.9,69,6.6)
    elif index==13:
        for y,t in [(73.6,'mean salt okunur;\nthread-local reduction'),(96,'7991/14210=0.562350'),(118.2,'1.817786'),(140.3,'2.284933')]:v(t,471,y,69,6.5)
        for j,row in enumerate(ARCH):
            vals=[row[0],row[1],row[2],row[3]]
            for t,x,w in zip(vals,[108,157,272,389],[44,110,112,151]):v(t,x,220.5+j*22.15,w,5.8)
        for y,ins,why in [(486.3,'0x00010030: ori a0,a0,0x100','Veri işleme'),(508.4,'0x00010034: sw a0,-12(s0)','Yerel sonucu saklar'),(530.6,'0x0001002C: lw a0,-12(s0)','Bellek -> register'),(552.7,'0x00010020: blt a0,a1,+8','Koşullu PC değişimi')]:v(ins,181,y,279,7);v(why,465,y,75,6.4)
        for y in [631.2,647.2,663.1,679,694.9]:mark(y)
    elif index==14:
        mark(75.7);mark(91.6)
        for t,x,w in zip(['ChatGPT /\nCodex','M3 / M4','İz/model denetimi,\nhata düzeltme;\ntablo/rapor desteği','“Final paketini M3\n+ M4 olarak\ntamamla”','ELF yürütmesi; bağımsız\ncache hesabı; tüm sonuçların\nve 30 elemanın karşılaştırması'],[72,164,207,312,393],[88,39,100,76,147]):v(t,x,426,w,6.2,19)
    c.save();buf.seek(0);return PdfReader(buf).pages[0]

def appendices():
    paths=[];story=[]
    story += [P('Ek-F3.A | 20 instruction: CPU ve bus izi','h'),P(TEXT['kernel']),P(TEXT['model']),P(TEXT['states'])]
    story += [P('Okuma anahtarı: PC hücresinde önce fetch adresi, sonra fetch sonrası PC ve en sonda execute sonrası PC gösterilir. MAR/MBR sırası IF, ardından varsa data erişimidir. Bus: adres=data; R/W. Her bus işlemi ACK ve Clock içerir. Cache H/M ekleri yalnız tam programın sıcak data cache’i içindir; Adım 3 bus hesabı cache’sizdir.')]
    for half in range(2):
        if half:story.append(PageBreak())
        rows=[['#','PC: F / F+4 / E','Instruction','IR (hex)','Durumlar','MAR: IF / data','MBR: IR / data','ALU','Yazılan GPR','Bus adres=veri; kontrol','Kat.']]
        for r in A['kernel'][half*10:half*10+10]:
            bus='\n'.join(('IF R ' if b['type']=='IF' else b['type']+' ')+hx(b['address'])+'='+hx(b['data']) for b in r['bus'])
            if r['cache']:bus+='\nData cache: '+','.join('H' if e['hit'] else 'M' for e in r['cache'])
            alu='EA\n'+hx(r['MAR'][-1]) if r['data_refs'] else r['ALU']
            rows.append([r['number'],'\n'.join(hx(r[k]) for k in ['pc_before','pc_fetch_next','pc_after']),r['assembly'],hx(r['IR']),r['states'],'\n'.join(hx(x) for x in r['MAR']),'\n'.join(hx(x) for x in r['MBR']),alu,'\n'.join(k+'='+hx(z) for k,z in r['written'].items()) or '-',bus,r['category']])
        story.append(table(rows,[18,62,80,48,60,56,56,48,60,108,24],'tiny'))
    story += [Spacer(1,9),P('Toplam: 20 IF, 6 operand read, 5 store. Kontrol instruction’ları #1,10,11,15,20; yalnız #1,10,20 için execute PC, fetch PC+4’ten farklıdır. #11 ve #15 j+4 komutları kontrol sınıfındadır ama sıradaki instruction’a gider. PM=program-bellek, DP=veri işleme, C=kontrol; PIO yoktur.')]
    path=TMP/'cpu.pdf';write_doc(path,story,True);paths.append(path)
    s=[]
    def head(title,*keys):
        s.append(P(title,'h'))
        for key in keys:s.append(P(TEXT[key]))
    head('Ek-F3.B | IAS / Fig.3.4 aktarımı','ias')
    s.append(table([['Adım','F/E','PC sonra','IR','AC sonra','Bellek / işlem'],[1,'Fetch','301','1940','0000','MAR=300; MBR=IR=1940'],[2,'Execute','301','1940','0007','MAR=940; MBR=0007; AC=7'],[3,'Fetch','302','5941','0007','MAR=301; MBR=IR=5941'],[4,'Execute','302','5941','0107','MAR=941; MBR=0100; AC=7+256'],[5,'Fetch','303','2940','0107','MAR=302; MBR=IR=2940'],[6,'Execute','303','2940','0107','MAR=940; MBR=0107; M[940]=263']],[35,53,65,52,67,244]))
    s += [Spacer(1,9),P(TEXT['ias_comparison']),P(TEXT['io_opcodes']),table([['IAS register','Rol','RV32IM karşılığı','Programcı görünürlüğü']]+IAS,[55,123,205,133]),PageBreak()]
    head('Ek-F3.C | I/O interrupt ve context','interrupt','privileged','privileged_scope','call_interrupt','nested')
    s += [Image(str(F/'interrupt_timeline.png'),width=516,height=210),P('Kaynak: RISC-V Privileged Architecture 20240411: mstatus §3.1.6.1 s.26/PDF32; mtvec §3.1.7 s.34/PDF40; mepc §3.1.14 s.41-42/PDF47-48; mcause §3.1.15 s.42-43/PDF48-49 (external cause 11); MRET §3.3.2 s.51/PDF57. Basılı ve PDF sayfası ayrılmıştır.','s'),PageBreak()]
    head('Ek-F3.D | Bus ve PCIe/QPI','bus','pcie')
    s.append(table([['Alan (octet)','12 B header, ECRC yok','16 B header, ECRC var'],['STP framing',1,1],['Sequence',2,2],['Header',12,16],['Data',120,120],['ECRC',0,4],['LCRC',4,4],['End framing',1,1],['Toplam',140,148],['Data/toplam','85.7143%','81.0811%'],['128/130 dahil','84.3956%','79.8337%']],[182,167,167]))
    s += [Spacer(1,9),P(TEXT['path']),Image(str(F/'interconnect_path.png'),width=516,height=215),PageBreak()]
    head('Ek-F4.A | Data trace ve adres alanları','trace','cache_model')
    rows=[['Adres','26 bit tag | 2 bit line | 4 bit offset','Tag','Line','Offset']]
    for r in A['fields_first5']:rows.append(['0x'+hx(r['address']),r['binary'][:26]+' | '+r['binary'][26:28]+' | '+r['binary'][28:],hex(r['tag']),r['line'],r['offset']])
    s += [table(rows,[87,266,61,44,58]),Spacer(1,10),P(TEXT['first30']),P('Bağımsız hesap kuralı: block=adres//16; line=block%4; tag=block//4; offset=adres%16. Valid ve tag eşitse hit; aksi halde miss. Yazmada write-allocate ve dirty=1. Bu aritmetik model cache_sim.Cache sınıfını kullanmaz; iki çıktı alan alan karşılaştırılır.'),PageBreak()]
    head('Ek-F4.B | İlk 30: bağımsız adım tablosu')
    rows=[['#','R/W','Adres','Tag','Line','Offset','H/M','Çıkan blok','Önce görüldü']]
    for e in A['first30']['rows']:rows.append([e['number'],e['rw'],hx(e['address']),hex(e['tag']),e['set'],hex(e['offset']),'H' if e['hit'] else 'M','-' if e['evicted'] is None else hx(e['evicted']),'Evet' if e['seen_before'] else 'Hayır'])
    s += [table(rows,[25,29,75,58,32,40,31,90,136]),Spacer(1,10),P('İlk 30 snapshot: line0 invalid; line1 valid/tag0x800/dirty1; line2 ve line3 valid/tag0x43FF/dirty1. Direct mapping’de replacement için LRU alanı yoktur. Bellek yazma=0; 27 hit / 3 miss. Kaynaklar: cache_first30.csv ve cache_first30_independent.json.'),PageBreak()]
    head('Ek-F4.C | Tam cache, tasarım uzayı ve locality','writeback')
    rows=[['64 B / 16 B','Hit','Miss','H','Dirty eviction']]+[[r['name'],r['hits'],r['misses'],f"{r['H']:.6%}",r['memory_writes']] for r in A['mapping_sweep']]
    s += [table(rows,[180,65,65,106,100]),Spacer(1,9)]
    s.append(table([['Direct / 64 B','Hit','Miss','H']]+[[r['name'],r['hits'],r['misses'],f"{r['H']:.6%}"] for r in A['line_sweep']],[180,90,90,156]))
    s += [Spacer(1,9),P(TEXT['design']),P(TEXT['line_design']),P(TEXT['conflict']),Image(str(F/'cache_design_space.png'),width=516,height=195),P(TEXT['access_time']),PageBreak()]
    head('Ek-F4.D | Tek kaynak değişikliği','change')
    s.append(table([['Ölçü','main.c / O0','main_v2.c / O0'],['C36','if (grades[i] & 0x100) below_count++;','if (v < mean) below_count++;'],['Instruction',3878,3818],['Data referansı',1490,1550],['Array / stack','150 / 1191','120 / 1251'],['Hit / miss','1230 / 260','1291 / 259'],['H','82.550336%','83.290323%'],['Ts (cycle)','6.234899','6.012903'],['Dirty eviction',157,165],['Cache’li model süre (ns)','8881.25','8862.50'],['Y7 ve 30 eleman','Aynı','Aynı']],[174,171,171]))
    s += [Spacer(1,10),P('Sonuç: bucket={14,1,7,0,8}; mean=51; below_count=14; pass_count=15. Beklenen değerler bağımsız LCG referansıyla da doğrulanır. Tek satırlık değişikliğin diff’i Git geçmişinde bulunur; özgün M1 main.c değişmedi.'),PageBreak()]
    head('Ek-F5.A | Dinamik performans modeli','performance')
    rows=[['Sınıf / ölçü','CPI_i','O0','O1']]
    for key,cpi in [('ALU',1),('Çarpma',3),('Load',1),('Store',1),('Branch/jump',2)]:rows.append([key,cpi,A['performance']['O0']['classes'][key],A['performance']['O1']['classes'][key]])
    for label,key in [('Ic','Ic'),('Base cycle','base_cycles'),('Ortalama CPI','CPI'),('T base (ns)','T_base_ns'),('MIPS','MIPS'),('m=data ref/Ic','m'),('Ts (cycle)','Ts'),('T cache yok (ns)','T_no_cache_ns'),('T cache var (ns)','T_cache_ns')]:rows.append([label,'-',*[f"{A['performance'][n][key]:.6f}".rstrip('0').rstrip('.') for n in ['O0','O1']]])
    s += [table(rows,[174,62,140,140]),Spacer(1,9),P(TEXT['time']),P(TEXT['mips']),P('Ek-F5.B | Amdahl ve veri bağımlılığı','sub'),P(TEXT['amdahl']),PageBreak()]
    head('Ek-F5.C | Architecture / organization')
    s += [table([['Özellik','Sınıf','Gerekçe','Değişiklik ve kanıt']]+ARCH,[94,78,140,204]),Spacer(1,10),P('Dört temel fonksiyon: data processing = #13 ori; data storage = #14 sw; data movement = #12 lw; control = #10 blt. Aynı instruction birden fazla işleve dokunabilir; burada baskın rol gösterilmiştir.'),PageBreak()]
    head('Ek-Final | Çalıştırma kanıtı ve kaynaklar')
    if (F/'cache_register_verification.jpg').exists():s += [Image(str(F/'cache_register_verification.jpg'),width=516,height=338)]
    s += [P('Ekran görüntüsü: araç penceresinde gerçek ELF yürütmesi, cache replay, ilk 30 snapshot ve kernel sonrası GPR’ler. Makine kodu doğrulama görüntüsü önceki M2 ekinde korunmuştur. Tüm veri dosyaları final/analysis.json, trace.csv ve final/*.csv ile teslim edilir. Interrupt şeması ayrı varsayımsal mimari modeldir.'),P('Araç zinciri ve tekrar üretim','sub'),P('Clang 18.1.6 / Zig 0.13.0; RV32IM ILP32, C99; Unicorn 2.1.4; Capstone 5.0.9; pyelftools 0.33. python tools/final_analysis.py: üç ELF, cache mikro testleri, ilk30 bağımsız karşılaştırma, tüm cache konfigürasyonlarında coherent sonuç denetimi. tools/final_plots.py grafikleri üretir. main_v2.c aynı O0 seçenekleriyle derlenir. Objdump sürüm ve kaynak bilgisi final/objdump_provenance.json dosyasındadır.'),P('YZ kullanım kaydı','sub'),P('ChatGPT/Codex, model ve izlerin denetimi, hata düzeltimi ve tablo/rapor hazırlanmasına destek için kullanıldı. Örnek istek: “Final paketini M3 + M4 olarak tamamla”. Sayısal sonuçlar ELF yürütmesi, bağımsız referans ve ayrı cache aritmetiğiyle doğrulandı; tabloların hesaplanması araçlarla otomatikleştirildi. Bu araç kontrolleri öğrencinin sözlü açıklamasının veya kendi elle çalışmasının yerine geçtiği iddiası taşımaz.')]
    s += [P('Gerçek GNU objdump doğrulaması','sub'),P('xPack GNU RISC-V objdump 2.45 ile -d çıktısı alındı. O0’daki 211 ve O1’deki 109 statik instruction word’ü ELF ile tamamen eşleşir; M2’de elle kodlanan 10 word de bu bağımsız araçta doğrulandı. objdump_O0.txt ve objdump_O1.txt ham araç çıktısıdır. Önceki M2 ekinin Capstone/simülatör doğrulamasına bu finalde gerçek objdump denetimi eklenmiştir.'),PageBreak(),P('Ek-Kaynaklar | ISA ve kitap referansları','h')]
    for title,url,note in SOURCES:s += [P(title,'sub'),P(note),P(url,'s'),Spacer(1,8)]
    s += [P('xPack GNU RISC-V Embedded GCC / binutils 2.45','sub'),P('https://github.com/xpack-dev-tools/riscv-none-elf-gcc-xpack/releases/tag/v15.2.0-1','s')]
    path=TMP/'evidence.pdf';write_doc(path,s);paths.append(path)
    return paths

def editable():
    # Plain Markdown preserves all report data in an actually editable form.
    parts=['# CMPE3209 Final - Ali Bal / 5001230006','M3 + M4; G2 / RV32IM. E-posta: alibal@ogr.iu.edu.tr','## M1 parametreler','SID=1230006; d=6, D2=06, S=17, N=30, pass=56. Cache64B/direct/line16B/WB+WA. k6 I/O; f1.6GHz,T1=1,T2=30,Nc5. tag26,line2,offset4.','## 1.3 Program','```c',(ROOT/'main.c').read_text(),'```','## M2 kodlama verileri','```csv',(ROOT/'m2/machine_code.csv').read_text(encoding='utf-8-sig'),'```']
    for k,t in TEXT.items():parts += ['## '+k,t]
    for title,path in [('CPU tüm alanlar','kernel_trace.csv'),('İlk 30 cache','cache_first30.csv')]:parts += ['## '+title,'```csv',(F/path).read_text(encoding='utf-8-sig'),'```']
    parts += ['## Tam sayısal model ve çıktılar','```json',(F/'analysis.json').read_text(encoding='utf-8'),'```','## Architecture/organization',*[' | '.join(row) for row in ARCH],'## IAS register eşlemesi',*[' | '.join(row) for row in IAS],'## Kaynaklar',*[' - '.join(row) for row in SOURCES],'## YZ kaydı','ChatGPT/Codex: iz/model denetimi, hata düzeltimi ve tablo/rapor desteği; örnek istek: Final paketini M3 + M4 olarak tamamla. Tabloların hesabı araçlarla otomatikleştirildi.']
    (F/'Final_Tutanak_Duzenlenebilir.md').write_text('\n\n'.join(parts),encoding='utf-8')

def main():
    paths=appendices();writer=PdfWriter()
    reader=PdfReader(ROOT/'pdf/Ali_Bal_5001230006_M2_TESLIM_TUTANAGI.pdf')
    assert len(reader.pages)==26
    for i,page in enumerate(reader.pages):
        if 5<=i<=14:page.merge_page(overlay(i))
        writer.add_page(page)
    for path in paths:
        for page in PdfReader(path).pages:writer.add_page(page)
    writer.add_metadata({'/Title':'CMPE3209 Final Teslim Tutanagi - Ali Bal - 5001230006','/Author':'Ali Bal','/Subject':'G2 RV32IM - M1 M2 M3 M4 complete final'})
    with OUT.open('wb') as fp:writer.write(fp)
    editable();print(str(OUT));print('pages',len(writer.pages))
if __name__=='__main__':main()
