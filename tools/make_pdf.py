import json, html
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'output/pdf'
TMP=ROOT.parent/'tmp/pdfs'
V=json.loads((ROOT/'evidence/verification.json').read_text())
CODE=(ROOT/'main.c').read_text().splitlines()
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Mono','C:/Windows/Fonts/CascadiaMono.ttf'))
style=ParagraphStyle('body',fontName='Arial',fontSize=9,leading=12)
W,H=612,792
def txt(c,t,y,size=9,font='Arial',x=38):
    c.setFont(font,size);c.setFillColor(HexColor('#18232d'));c.drawString(x,y,t)
def para(c,t,y,size=9):
    st=ParagraphStyle('p',parent=style,fontSize=size,leading=size+3)
    p=Paragraph(html.escape(t),st); _,h=p.wrap(536,700);p.drawOn(c,38,y-h);return y-h-7
def head(c,title,sub):
    txt(c,title,755,14,'ArialB');txt(c,sub,736,9);c.setStrokeColor(HexColor('#98aab7'));c.line(38,726,574,726)
def section(c,t,y):txt(c,t,y,10,'ArialB');return y-19
def row(c,a,b,y):
    txt(c,a,y,8.5,'ArialB');p=Paragraph(html.escape(b),style);_,h=p.wrap(360,100);p.drawOn(c,206,y+9-h);return y-max(19,h+5)
design=('Notları öğrenci numaramdan LCG ile üretip global grades dizisinde tutuyorum. '
         'İkinci geçişte notları beş aralıkta sayıp toplamı ve geçen kişi sayısını buluyorum. '
         'Tamsayı ortalamayı hesapladıktan sonra üçüncü geçişte mark_below fonksiyonuyla '
         'ortalamanın altındaki notları OR 0x100 ile işaretliyorum. Sonuçları simülatörde '
         'bellekten okuyabilmek için global değişkenlerde saklıyorum.')
params=[('d / D2 / S','d = 6; D2 = 06; S = 5+0+0+1+2+3+0+0+0+6 = 17'),
('N','24 + (6 mod 25) = 30 eleman; 30 × 4 = 120 byte'),
('Cache','d=6: 64 byte / 16 byte line / direct mapping / 4 line / set yok'),
('Write policy','6 çift: write-back; write miss için write-allocate (varsayım)'),
('k / Interrupt','(17 mod 7)+3 = 6; 17 tek: I/O'),
('f','1.0 + 0.1 × 6 = 1.6 GHz (varsayım)'),
('T1 / T2','T1=1 cycle; T2=20+5×(6 mod 4)=30 cycle (varsayım)'),
('Nc','2 + (17 mod 7) = 5 çekirdek (varsayım)'),
('Görev parametresi','P=50+(1230006 mod 10)=56; P ve üstü geçer'),
('Adres alanları','32 bit: word=log2(16)=4, line=log2(4)=2, tag=32-4-2=26 bit; s=28. Toplam=32 bit.')]
mapping=[('Y1','4, 18-21, 22-31, 33-37','Global int grades[30]; üretme, sayma ve işaretleme geçişleri.'),
('Y2','9, 25-30, 36','if ile ortalama, not aralığı ve geçme koşulları.'),
('Y3','7-12, 35','mark_below iki parametre alır, işaretli notu döndürür.'),
('Y4','19-20, 24, 10, 36','Toplama, çarpma, shift, OR ve AND kullanılır.'),
('Y5','20, 35','Üretilen ve işaretlenen değer grades[i] adresine yazılır.'),
('Y6','2, 16-17','const int SID; LCG başlangıcını ve geçme notunu etkiler.'),
('Y7','5, 25-32, 36','bucket, mean, below_count, pass_count global sonuçlardır.')]
def code(c,y,size=8.1,leading=10):
    for i,line in enumerate(CODE,1):txt(c,f'{i:02d}  {line}',y,size,'Mono');y-=leading
    return y-6
def maps(c,y,size=8):
    for k,lines,desc in mapping:
        y=para(c,f'{k} | {lines}: {desc}',y,size)
    return y
def outputs(c,y):
    y=section(c,'1.5 Program çıktıları - RV32IM bellekten okunan değerler',y)
    for k,val in V['outputs'].items():
        y=row(c,k,f"{V['addresses'][k]} : {val}",y)
    return para(c,'Kanıt: evidence/verification.json. Tüm sonuçlar ve 30 işaretli not, bağımsız Python hesabıyla aynı. evidence/rv32im_memory.png, bellek dökümünün görselidir; GUI ekran görüntüsü değildir.',y)
def kernel(c,y,full=False):
    y=section(c,'1.6 İzlenecek kernel',y)
    y=para(c,f"C satırları: 7-12 ve 35; üçüncü döngü, i=0; v=7, mean=51, dönüş=263 (0x107). Başlangıç {V['kernel_first']}, bitiş {V['kernel_last']}; 20 dinamik instruction. Çağrı hedefi 0x00010000, dönüş hedefi 0x000102D8. Adresler yürütme sırasındadır, artan bir aralık değildir.",y)
    y=para(c,'Load: lw; store: sw (stack); ALU: addi/ori; branch: blt; call/return: jalr/ret. Ana diziye store çağrıdan sonra C satır 35’te yapılır.',y)
    if full:
        for i,ins in enumerate(V['kernel'],1):
            txt(c,f"{i:02d}  0x{ins['address']:08X}  {ins['mnemonic']:<5} {ins['operands']}",y,8.3,'Mono');y-=12
    return y
def student(c,y):
    for a,b in [('Ad Soyad','Ali Bal'),('Öğrenci numarası','5001230006'),('E-posta','alibal@ogr.iu.edu.tr'),('Görev / ISA','G2 Sınav notu dağılımı / RISC-V RV32IM, ILP32'),('Derleyici','Clang 18.1.6 (Zig 0.13.0); C99, -O0, sanitizer kapalı'),('Simülatör / araçlar','Unicorn 2.1.4; Capstone 5.0.9; pyelftools 0.33'),('Git deposu','https://github.com/AliBal7/cmpe3209-proje (özel); etiket: M1')]:y=row(c,a,b,y)
    return y
def paramblock(c,y):
    y=section(c,'Adım 0 - Kişiye özel parametreler',y)
    y=para(c,'Tam numara 5001230006 > 2147483647. Yönergedeki son 9 hane kuralıyla 001230006 sayısal olarak SID=1230006 olur. d, D2 ve S tam öğrenci numarasından hesaplanır.',y)
    for a,b in params:y=row(c,a,b,y)
    return y
def footer(c,n):txt(c,f'Ali Bal | CMPE3209 | M1 | 2 Kasım 2026',24,8);txt(c,str(n),24,8,x=560)

# Three filled pages replace the M1 section; subsequent official pages are preserved.
c=canvas.Canvas(str(TMP/'filled_m1_pages.pdf'),pagesize=(W,H))
head(c,'CMPE3209 - Proje Teslim Tutanağı','M1 | Adım 0-1 | 2 Kasım 2026')
y=student(c,704);y=paramblock(c,y-8)
y=section(c,'1.1 Görev ve ISA seçimi',y-4)
y=para(c,'Seçimim G2: Sınav notu dağılımı. RV32IM seçtim; sabit 32 bit instruction formatları elle kodlamayı kolaylaştırıyor. M uzantısı tamsayı çarpma/bölme içeriyor. C99 unsigned int, bu hedefte 32 bittir.',y)
footer(c,1);c.showPage()
head(c,'Adım 1 - Görev seçimi ve C programı','Ali Bal | 5001230006 | G2 | RV32IM')
y=section(c,'1.2 Çözüm tasarımı',704);y=para(c,design,y)
y=section(c,'1.3 Satır numaralı C99 kodu (39 satır)',y);y=code(c,y,8,10)
y=section(c,'1.4 Zorunlu yapı eşlemesi',y);y=maps(c,y,7.6)
assert y>42,y
footer(c,2);c.showPage()
head(c,'Adım 1 - Çıktılar ve kernel seçimi','Sonuçlar gerçek RV32IM yürütmesinden alınmıştır.')
y=outputs(c,704);y=kernel(c,y-5,True)
y=para(c,'Öğretim üyesi M1: [ ] Onaylandı  [ ] Düzeltme istendi  [ ] Reddedildi\nTarih / Not: ______________________________',y-6)
y=section(c,'Adım 2 - Assembly ve machine code (M2: 9 Kasım)',y-7)
y=para(c,'Bu bölüm M2 tesliminde doldurulacak. M1 onayı bekleniyor. 2a C → assembly eşlemesi: C satır no | C ifadesi | assembly satırları | adres aralığı. .text başlangıcı / boyutu / içerik: M2’de doldurulacak.',y,8)
assert y>42,y
footer(c,3);c.save()

# Honest AI declaration; signature and instructor sections remain unsigned.
c=canvas.Canvas(str(TMP/'declaration.pdf'),pagesize=(W,H))
head(c,'Kilometre taşı ve YZ kullanım beyanı','Ali Bal | 5001230006 | M1 hazırlığı')
y=section(c,'Kilometre taşı kaydı',704)
y=para(c,'M1 son tarih: 2 Kasım 2026. Yerel Git etiketi: M1. Teslim tarihi ve öğretim üyesi parafı, gerçek teslim sırasında doldurulur. M2: 9 Kasım; final: 16 Kasım; sözlü savunma: 20 Kasım.',y)
y=section(c,'YZ kullanım beyanı',y-8)
y=para(c,'Araç: ChatGPT/Codex. Aşama: M1. Kodun denetlenmesi ve derleme hatalarının giderilmesinde YZ desteği kullanıldı. Doğrulama: RV32IM üzerinde çalıştırılan programın global sonuçları ve dizi elemanları bağımsız hesapla karşılaştırıldı.',y)
y=para(c,'İlgili istek: “M1 kısmını tamamlamamız lazım.” Kontroller: C99 derlemesi, zorunlu yapı eşlemesi, kişisel parametreler ve bellek çıktıları.',y)
y=section(c,'Öğrenci incelemesi ve imza',y-8)
y=para(c,'Kaynak kodu, parametre hesapları ve program çıktıları teslim öncesinde öğrenci tarafından incelenir. Öğrenci imzası ve öğretim üyesinin onayı bu belgede otomatik olarak doldurulmamıştır.',y)
y=para(c,'Ad Soyad: Ali Bal | Öğrenci numarası: 5001230006\nTarih: __________________ | İmza: __________________',y)
y=section(c,'Değerlendirme - öğretim üyesi doldurur',y-10)
for a,b in [('A1 Öneri ve parametre','5 puan | Puan: ____ | Not: __________________'),('A2 Assembly / machine code','15 puan | Puan: ____ | Not: __________________'),('A3 CPU, interrupt, bus','25 puan | Puan: ____ | Not: __________________'),('A4 Cache','25 puan | Puan: ____ | Not: __________________'),('A5 Performans','10 puan | Puan: ____ | Not: __________________')]:y=row(c,a,b,y)
footer(c,14);c.save()
w=PdfWriter();fill=PdfReader(TMP/'filled_m1_pages.pdf');original=PdfReader('C:/Users/HP/Desktop/CMPE3209_Proje_Teslim_Tutanagi.pdf')
for p in fill.pages:w.add_page(p)
for i in range(3,len(original.pages)):
    w.add_page(PdfReader(TMP/'declaration.pdf').pages[0] if i==13 else original.pages[i])
with (OUT/'Ali_Bal_CMPE3209_M1_Tutanak.pdf').open('wb') as f:w.write(f)

c=canvas.Canvas(str(OUT/'Ali_Bal_CMPE3209_M1_Oneri.pdf'),pagesize=(W,H))
head(c,'CMPE3209 - M1 Program Önerisi','Ali Bal | 5001230006 | alibal@ogr.iu.edu.tr | 2 Kasım 2026')
y=paramblock(c,704)
y=section(c,'Görev, tasarım ve ISA',y-8);y=para(c,'G2 Sınav notu dağılımı. '+design,y)
y=para(c,'ISA: RV32IM / ILP32. Sabit 32 bit instruction formatları elle kodlama için uygun; M uzantısı çarpma/bölme içeriyor. Clang 18.1.6 (Zig 0.13.0), C99 -O0; Unicorn 2.1.4. Git: https://github.com/AliBal7/cmpe3209-proje (özel), etiket M1.',y)
y=para(c,'YZ beyanı: Kodun denetlenmesi ve derleme hatalarının giderilmesinde ChatGPT/Codex desteği kullanıldı. Sonuçlar RV32IM belleği ve bağımsız hesapla karşılaştırıldı.',y)
footer(c,1);c.showPage()
head(c,'C99 kaynak kodu ve gereksinim eşlemesi','main.c | 39 satır | Kütüphane çağrısı, float ve dinamik bellek yok')
y=code(c,704,7.6,9.1);y=maps(c,y,7.1)
y=para(c,f"Kernel: C 7-12 ve 35; i=0, v=7. {V['kernel_first']} jalr çağrısından {V['kernel_last']} ret’e 20 dinamik instruction. lw, sw, ori/addi, blt ve call/return içerir. Ayrıntılı liste tutanakta.",y,7.6)
y=para(c,'Doğrulanan çıktılar: bucket={14,1,7,0,8}, mean=51, below_count=14, pass_count=15. Toplam=1553, tamsayı ortalama=1553/30=51. Kanıt: evidence/verification.json.',y,7.6)
assert y>42,y
footer(c,2);c.save()

# Plain editable content for future updates, without inventing an editable PDF form.
md='# Ali Bal - CMPE3209 M1\n\n5001230006 | alibal@ogr.iu.edu.tr\n\n'+design+'\n\n'
md+='\n'.join(f'- {a}: {b}' for a,b in params)+'\n\n```c\n'+'\n'.join(CODE)+'\n```\n\n'
md+='\n'.join(f'- {k} | {lines}: {desc}' for k,lines,desc in mapping)
md+='\n\nDoğrulama: '+json.dumps(V,ensure_ascii=False,indent=2)+'\n\nYZ kullanım beyanı: README.md. Öğrenci imzası ve öğretim üyesi onayı eklenmemiştir.\n'
(ROOT/'M1_duzenlenebilir.md').write_text(md,encoding='utf-8')

font=ImageFont.truetype('C:/Windows/Fonts/CascadiaMono.ttf',21)
im=Image.new('RGB',(1120,380),'#f4f6f8');d=ImageDraw.Draw(im)
lines=['RV32IM / Unicorn 2.1.4 - GERCEK BELLEK DOKUMU','Ali Bal | SID=1230006 | C99 -O0','']
lines += [f"{V['addresses'][k]}  {k:12} = {value}" for k,value in V['outputs'].items()]
lines += ['', 'PASS: Tum ciktilar bagimsiz Python hesabiyla ayni.', 'Bu gorsel GUI ekran goruntusu degil, dogrulama dokumudur.']
for i,line in enumerate(lines):d.text((22,18+i*32),line,font=font,fill='#18232d')
im.save(ROOT/'evidence/rv32im_memory.png')
for name,pages in [('Ali_Bal_CMPE3209_M1_Oneri',[0,1]),('Ali_Bal_CMPE3209_M1_Tutanak',[0,1,2,13])]:
    pdf=pdfium.PdfDocument(OUT/(name+'.pdf'))
    for i in pages:pdf[i].render(scale=1.5).to_pil().save(TMP/f'{name}_{i+1}.png')
print('Created two PDFs; proposal pages:',len(PdfReader(OUT/'Ali_Bal_CMPE3209_M1_Oneri.pdf').pages))
