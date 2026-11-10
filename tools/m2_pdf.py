"""Update original official form, expand its C-code block, and append M2 evidence."""
import copy, html, io, json, shutil
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
import pdfplumber, pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'output/CMPE3209_M2_SON_TESLIM';OUT.mkdir(parents=True,exist_ok=True)
TMP=ROOT.parent/'tmp/pdfs/m2';TMP.mkdir(parents=True,exist_ok=True)
A=json.loads((ROOT/'m2/analysis.json').read_text(encoding='utf-8'))
CODE=(ROOT/'main.c').read_text().splitlines();H=792;W=612
for name,path in [('M2Arial','arial.ttf'),('M2Bold','arialbd.ttf'),('M2Mono','CascadiaMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+path))
def para(c,text,x,top,width,size=7,leading=None):
    p=Paragraph(html.escape(text).replace('\n','<br/>'),ParagraphStyle('cell',fontName='M2Arial',fontSize=size,leading=leading or size+1))
    _,height=p.wrap(width,1000);p.drawOn(c,x,H-top-height);return height
def fresh():
    b=io.BytesIO();return b,canvas.Canvas(b,pagesize=(W,H))
def finish(b,c):c.save();b.seek(0);return PdfReader(b).pages[0]
def range4(addresses):
    nums=sorted(int(a,16) for a in addresses);groups=[]
    for n in nums:
        if not groups or n!=groups[-1][-1]+4:groups.append([n])
        else:groups[-1].append(n)
    return '; '.join(f'0x{g[0]:08X}' if len(g)==1 else f'0x{g[0]:08X}-0x{g[-1]:08X}' for g in groups)
def overlay(index):
    b,c=fresh()
    if index==0:
        c.setFillColor(colors.white);c.rect(68,H-743,478,28,stroke=0,fill=1);c.setFillColor(colors.black)
        para(c,'Kod sabiti SID=1230006 (son 9 hane). RV32IM seçimi: sabit 32 bit instruction formatları elle kodlamayı kolaylaştırır; M uzantısı tamsayı çarpma ve bölme içerir. ISA: RV32I 2.1 + M 2.0.',72,719,468,7.3,8.5)
    elif index==2:
        samples=[(16,'LCG başlangıcı'),(19,'LCG adımı'),(20,'grades[i] üretimi'),(35,'mark_below ve store')]
        for top,(line,short) in zip([523,545,567,589],samples):
            m=A['mapping'][line-1];para(c,str(line),72,top,80,8)
            para(c,short,159,top,75,7)
            para(c,m['asm_lines'],237,top,145,6.5)
            para(c,range4(m['addresses']),388,top,152,6.5)
        para(c,'Tüm 39 C satırının eşlemesi: Ek-M2.A / m2/c_to_assembly.csv.',72,636,468,7)
        para(c,'0x00010000',184,695,180,8);para(c,'844 byte',370,695,100,8);para(c,'Kod',475,695,65,8)
    elif index==3:
        para(c,'0x00020004 (.bss)',184,73,180,7.5);para(c,'152 byte',370,73,100,8);para(c,'Global veriler',475,73,65,7)
        para(c,'Kod (.text) ve veriler (.rodata/.bss) aynı 32 bit adres uzayındadır. .rodata: 0x00020000, 4 byte (SID). .data oluşmadı (0 byte); sıfır başlangıçlı global veriler .bss içindedir.',72,111,468,7,8)
        s0=A['kernel']['O0_stats'];s1=A['kernel']['O1_stats']
        rows=[(183,'instructions','Inline; çağrı kalktı'),(205,'loads','Stack okumaları kalktı'),(228,'stores','Stack yazmaları kalktı'),(250,'register_count','5 -> 3; Ek-M2.C')]
        for top,key,why in rows:para(c,str(s0[key]),316,top,42,9);para(c,str(s1[key]),367,top,42,9);para(c,why,418,top,122,6.7)
        for e in A['encodings']:
            top=330+(e['number']-1)*22.15
            para(c,e['address'],108,top,40,5.5)
            para(c,e['assembly'],151,top,56,5.6,6.3)
            para(c,e['format'],210,top,45,8)
            para(c,'Ek-M2.B\n#'+str(e['number']),259,top,65,6.2,7)
            para(c,e['word'],327,top,64,6.2)
            para(c,' '.join(e['bytes'].split()[:2])+'\n'+' '.join(e['bytes'].split()[2:]),393,top,70,6.5,7)
            para(c,'Simülatör:\nEvet',467,top,73,6.2,7)
        # Keep instructor's original checkboxes and fill their requested row numbers.
        originals=pdfplumber.open(ROOT/'templates/CMPE3209_Proje_Teslim_Tutanagi.pdf')
        words=originals.pages[3].extract_words()
        for top,value in [(575,'1, 2'),(591,'6'),(607,'4'),(623,'5'),(639,'8, 9')]:
            blanks=[w for w in words if abs(w['top']-top)<3 and '____' in w['text']]
            if blanks:para(c,value,blanks[-1]['x0']+1,top-1,55,8)
        originals.close()
        para(c,'SID=1230006=0x0012C4B6. Üst=(SID+0x800)>>12=0x12C; alt=SID-(0x12C<<12)=0x4B6=1206. Alt alanın işaret biti 0; bu SID için +1 düzeltmesi gerekmiyor. Alt 12 bit >=0x800 olsaydı üst +1, alt negatif olurdu (Ek-M2.C).',72,689,468,7,8)
    elif index==4:
        para(c,'blt adresi=0x00010020, hedef=0x00010028. Offset=hedef-PC=0x8=8 byte; PC+4 değil, instruction adresi esas alınır. imm[12|10:5|4:1|11]=0|000000|0100|0, imm[0]=0. Sonuç: 0x00B54463; little-endian: 63 44 B5 00.',72,88,468,7,8)
    elif index==13:
        para(c,'ChatGPT/\nCodex',72,404,89,6.5,6)
        para(c,'M2',164,404,40,8)
        para(c,'Kodlama ve\nderleme denetimi;\nhata düzeltme.',207,404,100,6.5,6)
        para(c,'“M2 deposunu da\ntamamlayıp…”',312,404,76,6.2,6)
        para(c,'ELF bit/byte eşlemesi;\nO0/O1 gerçek yürütmesi;\nbağımsız referans.',393,404,147,6.5,6)
    return finish(b,c)

# Appendices use tables at readable sizes; the official form itself is preserved.
styles={
    'h':ParagraphStyle('h',fontName='M2Bold',fontSize=14,leading=18,spaceAfter=10),
    'sub':ParagraphStyle('sub',fontName='M2Bold',fontSize=10,leading=13,spaceAfter=7),
    'p':ParagraphStyle('p',fontName='M2Arial',fontSize=9,leading=12,spaceAfter=7),
    'small':ParagraphStyle('small',fontName='M2Arial',fontSize=7.3,leading=9),
    'mono':ParagraphStyle('mono',fontName='M2Mono',fontSize=8,leading=11,spaceAfter=6),
}
def P(t,kind='p'):return Paragraph(html.escape(t).replace('\n','<br/>'),styles[kind])
def table(rows,widths,header=True):
    t=Table(rows,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#77818b')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]+([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf0f4'))] if header else [])))
    return t
story=[P('Ek-M2.A - C / assembly / ELF eşlemesi','h'),P('Tüm C satırları aşağıdadır. Assembly satır numaraları kökteki asm_O0.s dosyasına aittir. ELF adresleri .debug_line (DWARF) üzerinden gerçek 32 bit komutlara eşlenmiştir. Aynı C satırı birden fazla komut aralığı üretebilir.'),
P('Assembler sonrası bazı branch’ler ters koşul + jal olarak açılmıştır. Bu yüzden .s satır sayısı ile ELF instruction sayısı aynı değildir. Kesin makine komutları m2/disassembly_O0.txt içindedir; disassembler Capstone 5.0.9’dur.','p')]
rows=[[P('C no','small'),P('C ifadesi / açıklama','small'),P('asm_O0.s satırları','small'),P('ELF komut adresleri','small')]]
for m in A['mapping']:
    source=m['source'] or '(boş satır)'
    desc=source+ ('\n'+m['note'] if m['note'] else '')
    rows.append([P(str(m['c_line']),'small'),P(desc,'small'),P(m['asm_lines'] or '-','small'),P(range4(m['addresses']) or '-','small')])
story.append(table(rows,[30,175,105,226]));story.append(PageBreak())
for j in range(0,10,2):
    story.append(P(f'Ek-M2.B - Instruction kodlamaları {j+1}-{j+2}','h'))
    for e in A['encodings'][j:j+2]:
        story.append(P(f"#{e['number']} | {e['address']} | {e['assembly']} | {e['format']} formatı",'sub'))
        story.append(P(e['purpose']+'. Semantik girdiler: '+', '.join(f'{k}={v}' for k,v in e['arguments'].items()),'p'))
        rr=[[P('Instruction bitleri','small'),P('Alan','small'),P('Binary değer','small')]]
        rr += [[P(f['bits'],'p'),P(f['name'],'p'),P(f['binary'],'mono')] for f in e['fields']]
        story.append(table(rr,[100,135,301]));story.append(Spacer(1,6))
        story.append(P('32 bit word: '+e['binary'],'mono'))
        story.append(P('Hex: '+e['word']+' | Bellekte düşük adresten yükseğe: '+e['bytes']+' | ELF / simülatör: AYNI','p'))
        if e['number']==7:story.append(P('j +4 sözde komutunun gerçek biçimi jal x0,+4’tür. Dönüş adresi x0’a yazıldığı için saklanmaz.','p'))
        story.append(Spacer(1,12))
    story.append(PageBreak())
story += [P('Ek-M2.C - Optimizasyon, sabit ve branch hesabı','h'),
    P('Karşılaştırmanın sınırı','sub'),
    P('Aynı mantıksal işlem, i=0 için giriş notu 7 ve ortalama 51 hazırken başlar; işaretli sonuç 263 hazır olduğunda biter. -O0 tarafında M1’de onaylanan 20 instruction’lık pencere aynen kullanılmıştır. -O1 tarafında bu işlem main içine gömülen slt / slli / or üçlüsüdür. Ana diziye load/store her iki mantıksal pencerenin dışındadır.'),
    P('M1 penceresi jalr instruction’ıyla başlar; hemen önceki auipc hazırlığı bu 20 sayısına dahil değildir. Call çiftinin ikisi de sayılsaydı -O0 için 21 instruction olurdu. -O1’de call ve ret yürütülmez. Sayılar aynı C işleminin gerçek dinamik yürütmesidir; eşit uzunlukta fiziksel bloklar değildir.'),
    P('O0: 20 instruction, 6 load, 5 store, 5 register (a0, a1, ra, s0, sp). O1: 3 instruction, 0 load, 0 store, 3 register (a0, a5, a6). zero/x0 sayılmamıştır. Register allocation stack trafiğini kaldırır; inlining çağrı/epilogue maliyetini, if-conversion da branch’i kaldırır.'),
    P('O1 kernel adresleri: 0x00010178 slt a6,a5,a0; 0x0001017C slli a6,a6,8; 0x00010180 or a5,a5,a6. O0 kernel: 0x000102D4 jalr ile başlar, 0x0001004C ret ile biter.','p'),
    P('Tüm program sonuçları','sub'),
    P('O0: 3878 dinamik instruction, 988 load, 502 store; 211 statik instruction, .text 844 byte. O1: 1030 dinamik instruction, 70 load, 123 store; 109 statik instruction, .text 436 byte. Her iki programda bucket={14,1,7,0,8}, mean=51, below_count=14, pass_count=15. İşaretli 30 elemanın tamamı da aynıdır.'),
    P('SID ve sign extension','sub'),
    P('SID=1230006=0x0012C4B6. lui a0,0x12C üst kısmı 0x0012C000 yapar; addi a0,a0,0x4B6 buna 1206 ekler. U=(SID+0x800)>>12, L=SID-(U<<12). Bu SID’de L pozitif olduğundan +1 düzeltmesi yoktur. Genel örnek: 0x00123ABC için U=0x124, L=-1348; 0x00124000-1348=0x00123ABC. Üstü artırmak, alt 12 bitin işaret genişletmesini telafi eder.'),
    P('Branch ve fonksiyon çağrısı','sub'),
    P('blt PC=0x00010020, hedef=0x00010028; offset=8 byte. imm[12:0]=0000000001000; alan dağılımı 0 | 000000 | 0100 | 0, en düşük bit örtük 0’dır. Fall-through adresi 0x00010024’tür. Çağrı: 0x000102D0 auipc ra,0; 0x000102D4 jalr ra,ra,-720. Hedef=(0x000102D0-0x2D0)&~1=0x00010000; dönüş ra=0x000102D8.'),
    P('Kaynak: RISC-V Unprivileged ISA, RV32I 2.1, instruction formats / integer computational / control transfer bölümleri. https://docs.riscv.org/reference/isa/v20240411/unpriv/rv32.html (erişim: 10 Kasım 2026). RV32M 2.0 çarpma formatı: aynı referansın M bölümü.','small'),PageBreak(),
    P('Ek-M2.D - Machine code ve yürütme doğrulaması','h'),
    P('Alanlardan yeniden üretilen 10 word, bağlı ELF dosyasındaki komutlarla karşılaştırıldı. İki ELF de Unicorn üzerinde main girişinden normal dönüşe kadar çalıştırıldı. Ekran görüntüsü gerçek doğrulama penceresinden alınmıştır. Ödevin izin verdiği simülatör alternatifi kullanılmıştır; bu çıktı objdump olarak adlandırılmamıştır.'),
    Image(str(ROOT/'m2/machine_code_verification.jpg'),width=536,height=536*900/1402),
    Spacer(1,12),P('Doğrulama dosyaları: m2/analysis.json, m2/machine_code.csv, m2/disassembly_O0.txt, m2/disassembly_O1.txt. Yeniden çalıştırma: python tools/m2_analysis.py. Grafik arayüz: python tools/m2_gui.py.'),
    P('Model / çalışma koşulları','sub'),P('C99, RV32IM/ILP32, -O0 veya -O1; -g, -fno-sanitize=all, -ffreestanding, -fno-stack-protector, -fno-pic, -nostdlib. Linker: link.ld, giriş main. SP=0x00110000, RA dönüş sentinel’i=0x0003FFF0. BSS sıfırdan başlatılmıştır. Instruction’lar 32 bittir; C uzantısı kullanılmaz.','p')]

def page_footer(c,doc):
    c.setFont('M2Arial',8);c.drawString(38,22,'Ali Bal | 5001230006 | CMPE3209 M2 | 10 Kasım 2026');c.drawRightString(574,22,str(doc.page))
appendix_path=TMP/'m2_appendices.pdf'
SimpleDocTemplate(str(appendix_path),pagesize=(W,H),leftMargin=38,rightMargin=38,topMargin=36,bottomMargin=38).build(story,onFirstPage=page_footer,onLaterPages=page_footer)

base=PdfReader(ROOT/'pdf/Ali_Bal_CMPE3209_M1_Tutanak.pdf')
out=PdfWriter()
for index in range(15):
    page=copy.deepcopy(base.pages[index])
    if index in [0,2,3,4,13]:page.merge_page(overlay(index))
    if index!=1:out.add_page(page);continue
    # Expand the ORIGINAL 1.3 code area in-place and continue it before original 1.4.
    b,c=fresh();c.setFillColor(colors.white);c.rect(65,0,485,H-577,stroke=0,fill=1)
    c.setFillColor(colors.black);c.setFont('M2Mono',8.2)
    for n,line in enumerate(CODE[:14],1):c.drawString(72,H-584-(n-1)*10.3,f'{n:02}  {line}')
    page.merge_page(finish(b,c));out.add_page(page)
    continuation=PageObject.create_blank_page(width=W,height=H)
    b,c=fresh();para(c,'1.3 C kaynak kodu (devam)',72,65,468,12)
    c.setFont('M2Mono',8.2)
    for n,line in enumerate(CODE[14:],15):c.drawString(72,H-98-(n-15)*10.3,f'{n:02}  {line}')
    para(c,'M1 geri bildirimi uygulandı: 39 satırlık kod artık 1.3 bloğundadır. Onaylanan main.c ve M1 kernel’i değişmedi.',72,363,468,8)
    continuation.merge_page(finish(b,c))
    fragment=PdfReader(ROOT/'pdf/Ali_Bal_CMPE3209_M1_Tutanak.pdf').pages[1]
    fragment.cropbox.lower_left=(0,H-731);fragment.cropbox.upper_right=(612,H-594)
    continuation.merge_transformed_page(fragment,Transformation().translate(tx=0,ty=204))
    out.add_page(continuation)
out.add_page(PdfReader(ROOT/'pdf/Ali_Bal_CMPE3209_M1_Ek2.pdf').pages[0])
appendix=PdfReader(appendix_path)
for page in appendix.pages:out.add_page(page)
out.add_outline_item('M1 - Parametreler',0)
out.add_outline_item('1.3 - Kod devamı',2)
out.add_outline_item('M2 - Assembly ve machine code',3)
out.add_outline_item('M1 - Kernel ve çıktı kanıtı',16)
out.add_outline_item('M2 - Teknik ekler',17)
final=OUT/'Ali_Bal_5001230006_M2_TESLIM_TUTANAGI.pdf'
with final.open('wb') as f:out.write(f)
shutil.copy2(final,ROOT/'pdf'/final.name)
doc=pdfium.PdfDocument(final)
for i in list(range(6))+[14,16]+list(range(17,len(doc))):
    doc[i].render(scale=1.4).to_pil().save(TMP/f'page_{i+1:02}.png')
assert len(doc)==17+len(appendix.pages)
assert sum(1 for p in doc for _ in [0])==len(out.pages)
print('FINAL PAGES',len(out.pages),'M2 APPENDIX PAGES',len(appendix.pages))
