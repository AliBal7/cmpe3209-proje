# CMPE3209 - G2 / RV32IM

Ali Bal | 5001230006 | Computer Organization

## Teslim sürümleri

- [M2 teslim paketi](https://github.com/AliBal7/cmpe3209-proje/releases/tag/M2-teslim): güncel tam tutanak ve dijital ZIP.
- `M1`, `M1-teslim`: önceki aşamanın korunmuş Git etiketleri.
- `M2`: assembly, optimizasyon karşılaştırması ve 10 instruction kodlaması; `M2-teslim`: bağımsız ZIP'ten de çalışması doğrulanmış son teslim sürümü.

Depo herkese açıktır. M2 PDF, özgün tutanağın tüm sayfalarını, M1 verilerini ve M2 eklerini içerir.
Hocanın M1 geri bildirimi uygulandı: 39 satırlık kod 1.3 bloğuna alındı ve aynı bölümün devam sayfasına taşındı.
Onaylanan `main.c` ve M1 kernel'i değiştirilmedi. İmza ve öğretim üyesi alanları kendiliğinden doldurulmadı.

## Program ve kişisel parametreler

G2: 30 not LCG ile üretilir; beş aralıkta sayılır. Tamsayı ortalama hesaplandıktan sonra,
ortalamanın altındaki notların 8. biti OR 0x100 ile işaretlenir.

Tam numara 5001230006 signed 32 bit sınırını aştığından kodda son 9 hanenin sayısal değeri
`SID=1230006` kullanılır. Tam numara üzerinden d=6, D2=06, S=17, N=30.
Cache: 64 B, line 16 B, direct, 4 line; write-back / write-allocate.
k=6, I/O; f=1.6 GHz, T1=1 cycle, T2=30 cycle, Nc=5 (model varsayımları).
Adres alanları tag/line/word = 26/2/4 bit.

## M2 doğrulaması

Clang 18.1.6 (Zig 0.13.0), RV32IM / ILP32, C99; -O0 ve -O1 derlemeleri.
Unicorn 2.1.4 üzerinde iki ELF de gerçek komutları yürütür. Her iki derleme:

`bucket={14,1,7,0,8}, mean=51, below_count=14, pass_count=15`

İşaretlenmiş 30 dizi elemanının tamamı eşittir.

| Ölçü | -O0 | -O1 |
|---|---:|---:|
| Tüm program dinamik instruction | 3878 | 1030 |
| Tüm program load | 988 | 70 |
| Tüm program store | 502 | 123 |
| Statik instruction | 211 | 109 |
| .text boyutu | 844 B | 436 B |
| Mantıksal kernel instruction | 20 | 3 |
| Kernel load / store | 6 / 5 | 0 / 0 |

Kernel karşılaştırması i=0, v=7, mean=51 için girişler hazır -> işaretli sonuç hazır sınırını kullanır.
O0 tarafı M1'in onaylı 20 instruction'lık penceresidir; jalr öncesindeki AUIPC hazırlığı bu sayının dışındadır
(o komut da eklenirse 21). O1, main içindeki inline `slt/slli/or` üçlüsüdür. Diziye load/store sınırın dışındadır.
Farkın nedenleri register allocation, inlining ve branch'in koşulsuz ALU işlemleriyle değiştirilmesidir.

10 instruction, semantik operandlardan yeniden encode edilip ELF byte'larıyla eşleştirildi.
R/I/S/B/U/J formatları kapsanır. SID yükleme, branch offset, load, store ve AUIPC/JALR çağrısı gösterilir.
Doğrulama için yönergenin izin verdiği simülatör alternatifi kullanılmıştır.
Disassembly dosyaları Capstone çıktısıdır; objdump çıktısı olarak sunulmamıştır.

## Dosyalar

- `pdf/Ali_Bal_5001230006_M2_TESLIM_TUTANAGI.pdf`: güncel tam tutanak; 26 sayfanın tamamı basılabilir.
- `main.c`, `link.ld`, `asm_O0.s`, `asm_O1.s`: kaynak, adres yerleşimi ve derleyici listeleri.
- `evidence/main_O0.elf`, `evidence/main_O1.elf`: çalıştırılan ELF'ler.
- `m2/c_to_assembly.csv`: 39 C satırının .s satırları ve gerçek ELF adresleri.
- `m2/machine_code.csv`, `m2/analysis.json`: kodlama alanları ve sayısal doğrulama.
- `m2/disassembly_O0.txt`, `m2/disassembly_O1.txt`: gerçek instruction listeleri.
- `m2/machine_code_verification.jpg`: gerçek doğrulama penceresinin ekran görüntüsü.

## Yeniden çalıştırma

```powershell
python -m pip install -r requirements-verify.txt
python tools/m2_analysis.py
python tools/m2_gui.py
```

Yeniden derleme için Zig 0.13.0 / Clang 18.1.6 kullanılır:

```powershell
python -m pip install ziglang==0.13.0
powershell -File tools/build.ps1 -Optimization all
```

Derleme hedefi `-target riscv32-freestanding -mcpu=generic_rv32+m -mabi=ilp32`dir;
üretilen ELF yalnızca 32 bit RV32IM instruction'ları içerir. C uzantısı kapalıdır.
Tam seçenekler `tools/build.ps1` ve rapordadır.

YZ desteği: kodlama/derleme denetimi, hata düzeltme ve doğrulama için ChatGPT/Codex kullanıldı.
M3, M4 ve final çalışmaları bu teslimde tamamlanmış olarak gösterilmemiştir.
