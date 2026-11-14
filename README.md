# CMPE3209 - G2 / RV32IM

Ali Bal | 5001230006 | Computer Organization

## Teslim sürümleri

- [Final teslim paketi](https://github.com/AliBal7/cmpe3209-proje/releases/tag/final): M3 + M4, bütün adımları içeren resmî tutanak ve teslim ZIP'i.
- [M2 teslim paketi](https://github.com/AliBal7/cmpe3209-proje/releases/tag/M2-teslim): güncel tam tutanak ve dijital ZIP.
- `M1`, `M1-teslim`: önceki aşamanın korunmuş Git etiketleri.
- `M2`: assembly, optimizasyon karşılaştırması ve 10 instruction kodlaması; `M2-teslim`: bağımsız ZIP'ten de çalışması doğrulanmış son teslim sürümü.

Depo herkese açıktır. Final PDF, özgün tutanağın tüm sayfalarını, M1/M2 verilerini ve M3/M4 alanlarını içerir.
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
M2 aşamasında simülatör alternatifi kullanıldı. Finalde ayrıca GNU RISC-V objdump 2.45 ile
211 O0 ve 109 O1 word'ünün tamamı ELF ile karşılaştırıldı; 10 encoding de eşleşti.
`objdump_O0.txt` ve `objdump_O1.txt` gerçek `objdump -d` çıktılarıdır.

## Final: M3 + M4

Onaylanan 20 komutluk kernel'in PC/IR/MAR/MBR/GPR/bus izi `final/kernel_trace.csv` içindedir.
20 fetch + 6 data read + 5 data write = 31 adet 32-bit word aktarımı; 16-bit bus için 62 aktarım.
k=6 store tamamlandıktan sonra devam adresi `0x00010014` olur.
Interrupt, RV32IM'e eklenen resmî Privileged M-mode mimari senaryosudur;
Unicorn'a gerçek haricî interrupt enjekte edildiği iddia edilmez. Program GPR'leri gerçek yürütmeden alınır.

Byte taşıyan cache simülatörü gerçek load değerlerini de denetler.
İlk30 sonucu ayrı dört-slot/bölüm-kalan modeliyle alan alan eşleşir: 27 hit, 3 miss.
Bütün mapping, line boyu, kapasite ve WB/WT replay'lerinde Y7 ve 30 dizi elemanı korunur.

| Ölçü | O0 | O1 | main_v2 / O0 |
|---|---:|---:|---:|
| Dinamik instruction | 3878 | 1030 | 3818 |
| Data referansı | 1490 | 193 | 1550 |
| Hit / miss | 1230 / 260 | 131 / 62 | 1291 / 259 |
| H (%) | 82.550336 | 67.875648 | 83.290323 |
| Ts (cycle) | 6.234899 | 10.637306 | 6.012903 |
| Cache'li model süre (ns) | 8881.25 | 2183.75 | 8862.50 |

T1=1, T2=30: Ts=1+30(1-H). CPI modeli ALU1/çarpma3/load1/store1/branch2;
instruction fetch base 1 cycle içinde varsayılır. Bunlar gerçek donanım süre ölçümleri değildir.
O0->O1 speedup 4.066972; Amdahl(5), üçüncü döngü için thread-local reduction
ve sıfır paralelleştirme ek maliyeti varsayımıyla 1.817786'dır.

main_v2.c yalnız C36'yı `if (v < mean)` yapar. H artar; toplam erişim ve WB trafiği de artar.
Bu nedenle büyük donanım hızlanması iddia edilmez; model süre kazancı %0.2111'dir.
Finalin tamamı `final/analysis.json` ve PDF'de açıklanır.

## Dosyalar

- `pdf/Ali_Bal_5001230006_FINAL_TESLIM_TUTANAGI.pdf`: güncel tam tutanak; bütün sayfalar basılmalıdır.
- `final/Final_Tutanak_Duzenlenebilir.md`: tutanağın düzenlenebilir içerik sürümü.
- `main_v2.c`, `trace.csv`, `final/*.csv`, `final/analysis.json`: değişiklik, tam data izi ve simülasyon sonuçları.
- `final/*.png`, `final/cache_register_verification.jpg`: grafikler ve gerçek araç ekran görüntüsü.
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
python tools/final_analysis.py
python tools/final_gui.py
```

Yeniden derleme için Zig 0.13.0 / Clang 18.1.6 kullanılır:

```powershell
python -m pip install ziglang==0.13.0
powershell -File tools/build.ps1 -Optimization all
powershell -File tools/build_v2.ps1
```

Derleme hedefi `-target riscv32-freestanding -mcpu=generic_rv32+m -mabi=ilp32`dir;
üretilen ELF yalnızca 32 bit RV32IM instruction'ları içerir. C uzantısı kapalıdır.
Tam seçenekler `tools/build.ps1` ve rapordadır.

Gerçek objdump kontrolünü yeniden çalıştırmak için `python tools/objdump_verify.py --objdump <riscv-none-elf-objdump yolu>`.
Grafikler için ayrıca matplotlib gerekir: `python tools/final_plots.py`.
YZ desteği: model/iz denetimi, hata düzeltme ve tablo/rapor hazırlanmasına destek için ChatGPT/Codex kullanıldı;
ayrıntılı beyan tutanakta bulunur. Tabloların hesaplanması araçlarla otomatikleştirildi.
