"""Fill the original official form without replacing its wording; make print packet."""
import io, json, html, shutil
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'output/CMPE3209_M1_TESLIM'
TMP=ROOT.parent/'tmp/pdfs/submission'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('FormArial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('FormBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('FormMono','C:/Windows/Fonts/CascadiaMono.ttf'))
H=792
V=json.loads((ROOT/'evidence/verification.json').read_text())
def draw(c,text,x,top,width=100,size=7,leading=None):
    p=Paragraph(html.escape(text).replace('\n','<br/>'),ParagraphStyle('f',fontName='FormArial',fontSize=size,leading=leading or size+1))
    _,height=p.wrap(width,700);p.drawOn(c,x,H-top-height)
    return top+height
def overlay(page_index):
    b=io.BytesIO();c=canvas.Canvas(b,pagesize=(612,792))
    if page_index==0:
        entries=[(310,'Ali Bal'),(332,'5001230006'),(354,'alibal@ogr.iu.edu.tr'),(376,'G2 - Not dağılımı'),(398,'RV32IM / ILP32'),(420,'Clang 18.1.6\n(Zig 0.13.0)'),(442,'Unicorn 2.1.4\nCapstone 5.0.9'),(464,'github.com/AliBal7/\ncmpe3209-proje')]
        for top,text in entries:draw(c,text,461,top,79,7,8)
        for top,calc,res in [(591,'Son hane','6'),(614,'Son iki hane','06'),(636,'5+0+0+1+2+3+\n0+0+0+6','17'),(658,'24+(6 mod 25)','30'),(680,'64 B / 16 B\nDirect; 4 line','Set yok')]:
            draw(c,calc,411,top,80,6.5,7.5);draw(c,res,496,top,44,7)
        draw(c,'SID kod sabiti: 1230006 (son 9 hane). Tam hesap ve ISA gerekçesi: Ek-1, sayfa 1.',72,720,468,7.5)
    elif page_index==1:
        for top,calc,res in [(73,'6 çift','write-back'),(96,'(17 mod 7)+3','6'),(118,'17 tek','I/O'),(140,'1.0+0.1×6','1.6 GHz'),(162,'T1=1 cycle\nT2=20+5×2','1 / 30\ncycle'),(198,'2+(17 mod 7)','5'),(220,'50+(1230006\nmod 10)','P=56')]:
            draw(c,calc,411,top,80,6.5,7.5);draw(c,res,496,top,44,6.7,7.5)
        for top,bits,calc in [(286,'4','log2(16)'),(309,'2','log2(4)'),(331,'26','32-4-2'),(353,'32','26+2+4')]:
            draw(c,bits,328,top,70,8);draw(c,calc,458,top,82,7)
        draw(c,'RV32IM: 32 bit adres. s=28. Frekans, erişim süreleri ve çekirdek sayısı model varsayımıdır.',72,372,468,6.7)
        c.setLineWidth(1.1);c.line(109,792-452,112,792-456);c.line(112,792-456,116,792-448)
        design='Notları LCG ile grades dizisine üretiyorum. İkinci geçişte notları gruplandırıp toplamı ve geçenleri sayıyorum. Ortalamayı bulduktan sonra mark_below ile düşük notları işaretliyorum. Sonuçları global değişkenlerde tutuyorum.'
        draw(c,design,72,531,468,7,8)
        draw(c,'Satır numaralı 39 satır kod: Ek-1 sayfa 2 ve main.c.',236,583,304,7)
        for top,lines,desc in [(639,'4,18-37','3 dizi geçişi'),(661,'9,25-30,36','if koşulları'),(683,'7-12,35','mark_below'),(705,'10,19-24,36','ALU/OR/AND')]:
            draw(c,lines,400,top,61,6.4);draw(c,desc,464,top,76,6.8)
    elif page_index==2:
        for top,lines,desc in [(79,'20,35','Diziye store'),(102,'2,16-17','SID hesapta'),(124,'5,25-32,36','Global sonuçlar')]:
            draw(c,lines,400,top,61,6.4);draw(c,desc,464,top,76,6.8)
        for top,key,value in [(193,'bucket','{14,1,7,0,8}'),(215,'mean','51'),(237,'below_count','14'),(259,'pass_count','15')]:
            draw(c,key,72,top,120,8);draw(c,V['addresses'][key],199,top,90,7.7);draw(c,value,294,top,52,6.8)
            draw(c,'evidence/rv32im_simulator_screenshot.jpg (Ek-2)',349,top,191,6.8)
        for top,text in [(337,'7-12 ve 35; Ek-2'),(359,V['kernel_first']+' →\n'+V['kernel_last']),(381,'20'),(403,'3. döngü; i=0')]:draw(c,text,454,top,86,7,8)
    elif page_index==13:
        draw(c,'ChatGPT/\nCodex',72,381,89,6.5,6)
        draw(c,'M1',164,381,40,8)
        draw(c,'Kod denetimi;\nderleme hatalarının\ngiderilmesi.',207,381,100,6.5,6)
        draw(c,'“M1 kısmını\ntamamlamamız\nlazım.”',312,381,76,6.5,6)
        draw(c,'RV32IM yürütmesi ve\nbağımsız hesap\nkarşılaştırıldı.',393,381,147,6.5,6)
        draw(c,'Ali Bal',72,536,111,9);draw(c,'5001230006',187,536,160,9)
    c.save();b.seek(0);return PdfReader(b).pages[0]

source=ROOT/'templates/CMPE3209_Proje_Teslim_Tutanagi.pdf'
reader=PdfReader(source)
assert not reader.get_fields(),'Unexpected interactive fields; preserve their data explicitly'
for i in [0,1,2,13]:reader.pages[i].merge_page(overlay(i))
w=PdfWriter()
for p in reader.pages:w.add_page(p)
official=ROOT/'pdf/Ali_Bal_CMPE3209_M1_Tutanak.pdf'
with official.open('wb') as f:w.write(f)

# Printed evidence appendix: real GUI screenshot and actual dynamic kernel.
shot=ROOT/'evidence/rv32im_simulator_screenshot.jpg'
assert shot.exists(),'Actual simulator screenshot must be captured before final export'
b=io.BytesIO();c=canvas.Canvas(b,pagesize=(612,792))
draw(c,'Ek-2 - Simülatör çıktısı ve izlenecek kernel',38,32,536,14)
draw(c,'Ali Bal | 5001230006 | G2 | RV32IM | Unicorn 2.1.4',38,54,536,9)
img=ImageReader(str(shot));iw,ih=img.getSize();height=536*ih/iw
c.drawImage(img,38,792-78-height,width=536,height=height)
top=78+height+10
top=draw(c,'Gerçek simülatör penceresi: ELF yeniden çalıştırılarak global bellek değerleri okunmuştur. Sonuçlar bağımsız Python hesabıyla karşılaştırılmıştır.',38,top,536,8)+7
top=draw(c,'Kernel: C 7-12 ve 35, üçüncü döngü i=0. v=7, mean=51; dönüş 263 (0x107). Başlangıç '+V['kernel_first']+', bitiş '+V['kernel_last']+'. Adresler dinamik yürütme sırasındadır. Store’lar stack’e yapılır; ana diziye store çağrıdan sonra gelir.',38,top,536,8)+6
c.setFont('FormMono',7.7)
for i,ins in enumerate(V['kernel'],1):
    c.drawString(40,792-top-9,f"{i:02d}  0x{ins['address']:08X}  {ins['mnemonic']:<5} {ins['operands']}");top+=10
draw(c,'20 instruction: call/return, lw, sw, addi/ori ve blt içerir. Ayrıntılı veri: evidence/verification.json.',38,top+4,536,8)
assert top<740,(top,height)
c.save();b.seek(0);appendix=PdfReader(b).pages[0]
with (ROOT/'pdf/Ali_Bal_CMPE3209_M1_Ek2.pdf').open('wb') as f:
    a=PdfWriter();a.add_page(appendix);a.write(f)

proposal=PdfReader(ROOT/'pdf/Ali_Bal_CMPE3209_M1_Oneri.pdf')
# The deliverable is the user's original complete official form plus clearly separated appendices.
for p in proposal.pages:w.add_page(p)
w.add_page(appendix)
with official.open('wb') as f:w.write(f)
shutil.copy2(official,OUT/'Ali_Bal_5001230006_M1_TESLIM_TUTANAGI_DOLU.pdf')
printed=PdfWriter()
for i in [0,1,2]:
    printed.add_page(reader.pages[i])
    if i==2:
        # Only the M1 section is printed from page 3; M2 stays intact in the full form.
        wipe=io.BytesIO();cc=canvas.Canvas(wipe,pagesize=(612,792));cc.setFillColorRGB(1,1,1);cc.rect(0,0,612,792-450,stroke=0,fill=1);cc.save();wipe.seek(0)
        printed.pages[-1].merge_page(PdfReader(wipe).pages[0])
for p in proposal.pages:printed.add_page(p)
printed.add_page(appendix)
printed.add_page(reader.pages[13])
wipe=io.BytesIO();cc=canvas.Canvas(wipe,pagesize=(612,792));cc.setFillColorRGB(1,1,1)
cc.rect(0,792-109,612,109,stroke=0,fill=1)
cc.rect(0,0,612,792-564,stroke=0,fill=1)
cc.save();wipe.seek(0);printed.pages[-1].merge_page(PdfReader(wipe).pages[0])
printfile=OUT/'Ali_Bal_5001230006_M1_YAZDIR.pdf'
with printfile.open('wb') as f:printed.write(f)
shutil.copy2(printfile,ROOT/'pdf'/printfile.name)
for i in range(len(printed.pages)):
    doc=pdfium.PdfDocument(printfile)
    doc[i].render(scale=1.5).to_pil().save(TMP/f'print_{i+1}.png')
print('PRINT PAGES:',len(printed.pages))
print('OFFICIAL FORM PAGES:',len(w.pages))
