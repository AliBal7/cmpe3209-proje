# CMPE3209 Final - Ali Bal / 5001230006

M3 + M4; G2 / RV32IM. E-posta: alibal@ogr.iu.edu.tr

## M1 parametreler

SID=1230006; d=6, D2=06, S=17, N=30, pass=56. Cache64B/direct/line16B/WB+WA. k6 I/O; f1.6GHz,T1=1,T2=30,Nc5. tag26,line2,offset4.

## 1.3 Program

```c

/* Ali Bal, 5001230006, G2 */
const int SID = 1230006;
enum { N = 30 };
int grades[N];
int bucket[5], mean, below_count, pass_count;

int mark_below(int value, int average)
{
    if (value < average)
        value = value | 0x100;
    return value;
}

int main(void)
{
    unsigned int x = (unsigned int)SID;
    int i, sum = 0, pass = 50 + SID % 10;
    for (i = 0; i < N; i++) {
        x = 1664525u * x + 1013904223u;
        grades[i] = (int)((x >> 16) % 101u);
    }
    for (i = 0; i < N; i++) {
        int v = grades[i];
        sum = sum + v;
        if (v < 50) bucket[0]++;
        else if (v < 65) bucket[1]++;
        else if (v < 75) bucket[2]++;
        else if (v < 85) bucket[3]++;
        else bucket[4]++;
        if (v >= pass) pass_count++;
    }
    mean = sum / N;
    for (i = 0; i < N; i++) {
        int v = grades[i];
        grades[i] = mark_below(v, mean);
        if (grades[i] & 0x100) below_count++;
    }
    return 0;
}


```

## M2 kodlama verileri

```csv

number,address,assembly,format,word,little_endian_bytes,verified
1,0x00010060,"lui a0, 0x12c",U,0x0012C537,37 c5 12 00,True
2,0x00010064,"addi a0, a0, 0x4b6",I,0x4B650513,13 05 65 4b,True
3,0x000100A4,"mul a0, a0, a1",R,0x02B50533,33 05 b5 02,True
4,0x00010018,"lw a0, -0xc(s0)",I,0xFF442503,03 25 44 ff,True
5,0x00010034,"sw a0, -0xc(s0)",S,0xFEA42A23,23 2a a4 fe,True
6,0x00010020,"blt a0, a1, 8",B,0x00B54463,63 44 b5 00,True
7,0x00010028,j 4,J,0x0040006F,6f 00 40 00,True
8,0x000102D0,"auipc ra, 0",U,0x00000097,97 00 00 00,True
9,0x000102D4,"jalr ra, ra, -0x2d0",I,0xD30080E7,e7 80 00 d3,True
10,0x00010030,"ori a0, a0, 0x100",I,0x10056513,13 65 05 10,True


```

## model

Pipeline yok, her an tek instruction yürütülür. PC, IR, MAR ve MBR Fig. 3.2’deki gibi kavramsal olarak vardır. Her bellek erişimi bir bus işlemidir; Adım 3’te cache yok sayılır. Data bus genişliği 32 bittir.

## real_model_difference

İzleme modelinde komutlar sırayla ve örtüşmeden yürütülür. Gerçek işlemciler pipeline, cache ve spekülatif yürütme kullanabilir. PC, IR, MAR ve MBR burada kavramsal durumlardır; birebir fiziksel register tasarımı iddia edilmez. Cache etkisi Adım 3 bus hesabına alınmaz, Adım 4 ve 5’te ayrı modellenir.

## states

iac: instruction adresi; if: instruction fetch; iod: decode; oac: bellek operand adresi; of: bellekten operand okuma; do: ALU/kontrol işlemi; os: belleğe operand yazma. Register okumaları ayrı bus/of işlemi sayılmaz. Store’da kaynak register MBR’ye alınır ve os yapılır. Load’un hedef GPR’sine aynı değer yazıldığında değer değişmemiş olsa da yazılan register ayrıca gösterilmiştir.

## kernel

M1’de onaylanan 20 dinamik instruction kullanıldı. Pencere 0x000102D4 jalr ile başlar, mark_below içinden geçer ve 0x0001004C ret ile biter. Başlangıç ve bitiş bir artan adres aralığı değildir. i=0 için giriş v=7, mean=51; sonuç a0=263=0x107’dir. Kategori PIO olan program instruction’ı yoktur; I/O interrupt ayrı senaryodur.

## ias

Fig. 3.4 aktarımı, gerçek kernel’de 0x0001002C lw / 0x00010030 ori / 0x00010034 sw üçlüsünün yerel v kopyasını güncellemesine karşılık gelir. Kernel ana diziye store yapmaz; bu store çağrıdan sonra 0x000102EC’dedir. v 0-100 aralığında olduğundan bit 8 başlangıçta 0’dır; v OR 256 ile v+256 bu seçilmiş dalda eşittir. Hipotetik makinede M[0x940]=7, M[0x941]=256 ve program 0x300’den başlar: 0x1940 (LOAD), 0x5941 (ADD), 0x2940 (STORE).

## ias_comparison

Her iki seçilmiş parça da 3 instruction cycle kullanır; fetch ve execute ayrı satırlara açıldığında hipotetik tabloda 6 adım vardır. Hipotetik parçada 3 instruction read + 2 operand read + 1 store; RV32IM üçlüsünde 3 instruction read + 1 load + 1 store olur. Sabit, RV32IM’de immediate alanında taşınır. Tek accumulator, sonucu AC üzerinden geçirip ayrıca store etmeyi gerektirir. PDP-11 ADD B,A tek instruction ile iki bellek operandı kullanabildiği için instruction sayısı ile bellek erişimi sayısının aynı şey olmadığı görülür.

## io_opcodes

Problem 3.1’de opcode 3, I/O’dan AC’ye yüklemedir; opcode 7, AC’den I/O’ya yazmadır. Branch opcode’u değildirler. 0x3005, aygıt 5’ten AC’ye örneğin 7 alır; 0x7006, AC’deki 7’yi aygıt 6’ya yollar. Bu iki I/O örneği ana kernel’in 3 instruction’lık eşdeğer parçasına dahil edilmez; kernel’de I/O instruction’ı bulunmaz.

## interrupt

S=17 olduğundan tür I/O ve k=(17 mod 7)+3=6’dır. İstek 0x00010010 adresindeki sw a0,-12(s0) execute edilirken gelir. Store, 0x0010FFC4 adresine 7 yazmayı tamamlar; ardından interrupt tanınır. Devam adresi ve mepc=0x00010014’tür; handler dönüşünde 7. dinamik instruction çalışır. k+1=7 seçilseydi ortalama 51’in stack store’u da tamamlanır, mepc=0x00010018 olurdu.

## privileged

Gerçek mekanizma, RV32IM programına eklenen bir Privileged M-mode senaryosudur. Başlangıçta mstatus.MIE=1, mie.MEIE=1 ve uygun haricî interrupt kaynağının etkin olduğu varsayılır. mtvec=0x00030000, MODE=Direct seçilir. Donanım mepc=0x00010014 ve mcause=0x8000000B (machine external interrupt) yazar; MPIE eski MIE’yi, MPP önceki M-mode’u alır, MIE=0 olur. Donanım bütün GPR’leri otomatik stack’e yazmaz. Handler kullandığı GPR’leri ve nested işlem olacaksa mepc/mstatus’u yazılımla saklar. MRET, PC’yi mepc’den ve interrupt enable durumunu önceki değerden geri alır.

## privileged_scope

Bu CSR/handler akışı resmi ISA’ya dayanan mimari senaryodur; Unicorn’a gerçek bir haricî interrupt enjekte edildiği ileri sürülmez. Unicorn’dan alınan 6. instruction sonrası GPR’ler ra=0x000102D8, sp=0x0010FFC0, s0=0x0010FFD0, a0=7, a1=51’dir. ISR’nin uygulama verisine dokunmadığı ve kullandığı context’i geri yüklediği varsayımı altında devam durumu aynıdır. Cache ve performans izleri ISR trafiği içermeyen özgün C programına aittir.

## call_interrupt

Fonksiyon çağrısını programdaki jalr başlatır; dönüş adresi ra=0x000102D8 olur ve prologue onu stack’e yazar. Interrupt’ı dış olay başlatır; dönüş PC’sini donanım mepc’ye yazar, GPR saklama görevini handler üstlenir. Normal çağrı programın bilinçli kontrol akışıdır; şeffaf ISR, uygulama algoritmasının açık çağrısı değildir.

## nested

A ilk I/O kaynağı, B ise daha yüksek öncelikli ikinci I/O kaynağıdır. Sequential durumda A boyunca interrupt maskelenir; B pending kalır, A bittikten sonra B çalışır. Nested durumda A context ve CSR’lerini saklar, yalnız yüksek öncelikli B’ye izin verecek controller eşiğini ayarlar ve MIE’yi açar. B bitince A kaldığı instruction’dan, A bitince program 0x00010014’ten devam eder. İkinci trap mepc’yi değiştireceği için A’nın ilk mepc/mstatus kopyasını saklaması gerekir. Zaman çizelgesi gerçek cycle ölçümü değil, sembolik olay sırasıdır.

## bus

Cache yokken kernel 20 instruction read, 6 data read ve 5 data write üretir; toplam 31 word aktarımıdır. Read işlemlerinde Memory read, store’da Memory write; tamamlanma sırasında Transfer ACK ve senkron modelde Clock kullanılır. Address bus 32 bit ve byte adresleme varsayımıyla 2^32 byte = 4 GiB doğrudan adreslenir. Data bus 16 bit olduğunda her 32 bit instruction ve operand iki yarım aktarılır: 40+12+10=62 transfer. Mevcut/16-bit oranı 31/62=0.5; 16-bit düzen 2 kat transfer ister.

## pcie

N×4=120 byte payload için Fig. 3.25’in alan modeli kullanılır. Baş framing 1, sequence number 2, LCRC 4, son framing 1 octet’tir. 12-byte header ve ECRC yoksa toplam 140 octet, verim 120/140=%85.7143’tür. 16-byte header ve 4-byte ECRC ile toplam 148 octet, verim %81.0811’dir. Yönergedeki 128b/130b çarpanı eklendiğinde sırasıyla %84.3956 ve %79.8337 bulunur. Bu teorik hesap ACK, flow-control, SKP ve yeniden iletim gibi ek trafiği kapsamaz.

## path

Fig. 3.17/3.21 topolojisi için veri DRAM/bellek denetleyicisi ve çekirdek/cache tarafından I/O yoluna taşınır. QPI Protocol katmanı packet, Routing katmanı rota, Link katmanı flit, Physical katmanı phit düzeyinde çalışır. Intel’in tam genişlik örneğinde flit 80 bit, phit 20 bittir. IOH/root complex QPI semantiğini PCIe işlemine çevirir. PCIe Transaction katmanında TLP; Data Link katmanında sıra/LCRC ile ACK/NAK/flow-control DLLP’leri; Physical katmanında lane ve kodlanmış bit akışı bulunur. QPI flit’i doğrudan PCIe TLP’si değildir. Bu kitap topolojisi örneği RV32IM ISA’nın gerçek bir QPI portunu zorunlu kıldığı anlamına gelmez.

## trace

trace.csv ve final/trace_O0.csv, -O0 programının baştan sona yalnız data erişimlerini içerir. İlk altı sütun sira,RW,adres_hex,boyut,c_satiri,stack_mi biçimindedir; PC, instruction sıra numarası ve veri değeri de eklenmiştir. Instruction fetch’leri cache izine dahil edilmez. Stack aralığı 0x00100000-0x0010FFFF olarak ayrı işaretlenir. 1490 referansın 988’i load, 502’si store; 1191’i stack, 150’si ana dizidir. Diğer erişimler global sonuçlara aittir.

## cache_model

Data cache başlangıçta boştur; kapasite 64 B, line 16 B, direct mapping, write-back ve write-allocate uygulanır. Byte adreslemede word(w)=4 bit blok içi offset, line(r)=2 bit ve tag=26 bittir; s=28. Buradaki word alanı, dokümanın adlandırmasıyla byte offset’i de kapsar: 2 bit int-word indeksi ve 2 bit byte offset. Associative deneylerde LRU kullanılır. Referanslar 1 veya 4 byte’tır ve test edilen line sınırlarını aşmaz.

## first30

İlk 30 referans hem dört slot ve bölüm/kalan hesabı kullanan bağımsız adım tablosuyla hem byte taşıyan cache simülatörüyle işlendi. Tag, line, offset, hit/miss, evicted blok, daha önce görülme ve dirty eviction alanları birebir eşleşti. Sonuç 27 hit, 3 miss, H=0.9 ve 0 dirty eviction yazmasıdır. İlk 30 sonunda line 0 invalid, line 1 tag=0x800, line 2 ve 3 tag=0x43FF ve bu üç line dirty’dir.

## writeback

Tam -O0 izinde 1230 hit, 260 miss, H=%82.5503 ve 157 dirty eviction yazması vardır. Program sonunda dört dirty line kalır: 0x00020000, 0x0010FFD0, 0x0010FFE0, 0x0010FFF0. Zorunlu son flush yapılırsa 4 ek yazma, toplam 161 line yazması olur; raporlanan 157’ye flush dahil değildir. WT deneyinde her store ana belleğe gider: 502 yazma. Sonuçlar cache-coherent peek ile denetlenmiştir; salt DRAM dökümünden önce WB line’ların flush edilmesi gerekir.

## design

Aynı 1490 erişim ve 64 B kapasiteyle H: direct %82.5503, 2-way %83.6913, 4-way ve fully associative LRU %81.0067. Dört line bulunduğu için 4-way ve fully associative aynıdır. Direct’in hit olup FA’nın miss olduğu 104 erişim, tersinin olduğu 81 erişim vardır; fark FA’nın 23 ek miss’ini açıklar. Örneğin erişim #294, 0x0010FFF0 için direct hit, FA miss’tir. Sabit yerleşim bazı sıcak stack line’larını korurken ortak LRU havuzu onları evirebilir; daha çok associativity her izde daha iyi sonucu garanti etmez.

## line_design

Direct mapping’de line 8/16/32/64 B seçildiğinde H sırasıyla %86.1745 / %82.5503 / %77.8523 / %68.9933 olur. Büyük line spatial locality kazandırabilir; fakat burada line sayısını 8’den 1’e indirerek sıcak stack/global blokların yerinden çıkarılmasını artırır. 120 B dizi tek başına 64 B cache’i aşar. Tekrar kullanılan stack erişimleri temporal locality üretir; komşu grades elemanları spatial locality sağlar. Bu -O0 izinde toplam erişimin çoğunun stack olması sonucu belirgin biçimde etkiler.

## conflict

En sık çatışmalardan biri line 0’da 0x00020000 global bloğu ile 0x0010FFC0 callee-stack bloğudur; biri diğerini 30, ters yön 23 kez çıkarır. Line 3’te 0x0010FFF0 stack bloğu ile 0x00020030 ve 0x00020070 dizi blokları da dönüşümlü çıkarılır. Bu adreslerin düşük line bitleri aynıdır. Bütün mapping, line boyu, ek kapasite ve write-policy replay’lerinde dört global çıktı ve 30 dizi elemanı aynı kalmıştır.

## access_time

T1=1 ve T2=30 cycle model varsayımıdır. Ts=H×1+(1-H)×31=1+30(1-H). -O0 için Ts=6.234899 cycle; cache’siz her erişim 30 cycle olduğundan yalnız bellek erişimi speedup’ı 30/Ts=4.811625’tir. Dirty write-back için ek gecikme veya değişen line boyunun aktarım süresi bu basit Ts formülüne ayrıca katılmamıştır; yazma trafiği ayrı raporlanır.

## change

main_v2.c’de tek kaynak satırı değişti: C36 if (grades[i] & 0x100) yerine if (v < mean). v özgün 0-100 notudur; işaretleme koşulu tam olarak v<mean olduğundan bütün Y7 ve 30 işaretli eleman korunur. Array referansları 150’den 120’ye iner; fakat -O0 backend’i stack referanslarını 1191’den 1251’e çıkarır. Toplam referans 1490->1550, miss 260->259, H %82.5503->%83.2903, Ts 6.234899->6.012903 olur. H artışının bir kısmı ek stack hit’leridir; model program süresi yalnız 8881.25->8862.50 ns (%0.2111) azalır. Write-back sayısı 157->165 yükseldiği için gerçek donanımda büyük bir hızlanma iddia edilmez.

## performance

CPI tablosu varsayımsaldır: ALU=1, çarpma=3, load=1, store=1, branch/jump=2 cycle. MUL, MULH ve MULHU çarpma sınıfındadır; ret/j/jalr branch/jump sayılır. f=1.6 GHz, tau=0.625 ns. Dinamik Ic -O0=3878, -O1=1030’dur. Base CPU cycle toplamı 4920 ve 1441; ortalama CPI 1.268695 ve 1.399029’dur. Instruction fetch’in 1 cycle’da karşılandığı, base modele dahil olduğu ve m’nin yalnız data referanslarını saydığı varsayılır.

## time

T=Ic×CPI×tau ile bellek etkisiz süreler 3075 ve 900.625 ns; MIPS rate 1261.138 ve 1143.650 olur. m=1490/3878=0.384219 ve 193/1030=0.187379. T=Ic×[p+m×k]×tau için cache yok: 31012.5 / 4519.375 ns; cache var: 8881.25 / 2183.75 ns. Her sürüm kendi trace’inden elde edilen Ts ile hesaplanır (-O1 Ts=10.637306). -O0->-O1 speedup=4.066972; -O0 için cache yok->var speedup=3.491907. Bunlar donanım ölçümü değil, model tahminleridir.

## mips

-O0 MIPS rate’i 1261.138, -O1’inki 1143.650 olduğu halde -O1 model süresi 2183.75 ns ile -O0’ın 8881.25 ns süresinden kısadır. Optimizasyon daha az instruction ve daha az data erişimi yürütür; instruction karışımı değiştiği için MIPS tek başına iki farklı derlemenin hızını karşılaştırmaz. -O1’in hit oranı daha düşük olsa da tekrarlı stack erişimlerini büyük ölçüde kaldırması toplam süreyi azaltır.

## amdahl

LCG üretimi önceki x’e bağımlıdır; bu haliyle ardışıldır. Son döngüde C33-37 ve helper C7-12, mean hesaplandıktan sonra farklı grades[i] hücreleri üzerinde bağımsız işlenebilir. below_count++ ortak değişken olduğundan program doğrudan thread-safe değildir; thread-local sayım ve sonunda reduction gerekir. -O0 cache’li modelde bu fazın maliyeti 7991 / 14210 cycle olduğundan f=0.562350’dir. Nc=5 için speedup=1/[(1-f)+f/5]=1.817786; sonsuz çekirdek limiti 1/(1-f)=2.284933. Thread başlatma/reduction ve bellek paylaşımı ek maliyetleri yok sayılan ideal üst sınırdır.

## CPU tüm alanlar

```csv

number,pc_before,pc_after,assembly,IR,states,MAR,MBR,ALU,written,category,bus,cache
1,66260,65536,"jalr ra, ra, -0x2d0",3540025575,"iac, if, iod, do",[66260],[3540025575],PC=0x00010000,"{""ra"": 66264}",C,"[{""type"": ""IF"", ""address"": 66260, ""data"": 3540025575, ""control"": ""Memory read; ACK; Clock""}]",[]
2,65536,65540,"addi sp, sp, -0x10",4278255891,"iac, if, iod, do",[65536],[4278255891],"sp, sp, -0x10 => 0x0010FFC0","{""sp"": 1114048}",DP,"[{""type"": ""IF"", ""address"": 65536, ""data"": 4278255891, ""control"": ""Memory read; ACK; Clock""}]",[]
3,65540,65544,"sw ra, 0xc(sp)",1123875,"iac, if, iod, oac, os","[65540, 1114060]","[1123875, 66264]",EA=0x0010FFCC,{},PM,"[{""type"": ""IF"", ""address"": 65540, ""data"": 1123875, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""W"", ""address"": 1114060, ""data"": 66264, ""control"": ""Memory write; ACK; Clock""}]","[{""number"": 749, ""hit"": false}]"
4,65544,65548,"sw s0, 8(sp)",8463395,"iac, if, iod, oac, os","[65544, 1114056]","[8463395, 1114112]",EA=0x0010FFC8,{},PM,"[{""type"": ""IF"", ""address"": 65544, ""data"": 8463395, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""W"", ""address"": 1114056, ""data"": 1114112, ""control"": ""Memory write; ACK; Clock""}]","[{""number"": 750, ""hit"": true}]"
5,65548,65552,"addi s0, sp, 0x10",16843795,"iac, if, iod, do",[65548],[16843795],"s0, sp, 0x10 => 0x0010FFD0","{""s0"": 1114064}",DP,"[{""type"": ""IF"", ""address"": 65548, ""data"": 16843795, ""control"": ""Memory read; ACK; Clock""}]",[]
6,65552,65556,"sw a0, -0xc(s0)",4272171555,"iac, if, iod, oac, os","[65552, 1114052]","[4272171555, 7]",EA=0x0010FFC4,{},PM,"[{""type"": ""IF"", ""address"": 65552, ""data"": 4272171555, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""W"", ""address"": 1114052, ""data"": 7, ""control"": ""Memory write; ACK; Clock""}]","[{""number"": 751, ""hit"": true}]"
7,65556,65560,"sw a1, -0x10(s0)",4273219619,"iac, if, iod, oac, os","[65556, 1114048]","[4273219619, 51]",EA=0x0010FFC0,{},PM,"[{""type"": ""IF"", ""address"": 65556, ""data"": 4273219619, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""W"", ""address"": 1114048, ""data"": 51, ""control"": ""Memory write; ACK; Clock""}]","[{""number"": 752, ""hit"": true}]"
8,65560,65564,"lw a0, -0xc(s0)",4282656003,"iac, if, iod, oac, of","[65560, 1114052]","[4282656003, 7]",EA=0x0010FFC4,"{""a0"": 7}",PM,"[{""type"": ""IF"", ""address"": 65560, ""data"": 4282656003, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114052, ""data"": 7, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 753, ""hit"": true}]"
9,65564,65568,"lw a1, -0x10(s0)",4278461827,"iac, if, iod, oac, of","[65564, 1114048]","[4278461827, 51]",EA=0x0010FFC0,"{""a1"": 51}",PM,"[{""type"": ""IF"", ""address"": 65564, ""data"": 4278461827, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114048, ""data"": 51, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 754, ""hit"": true}]"
10,65568,65576,"blt a0, a1, 8",11879523,"iac, if, iod, do",[65568],[11879523],7 < 51: true; PC=0x00010028,{},C,"[{""type"": ""IF"", ""address"": 65568, ""data"": 11879523, ""control"": ""Memory read; ACK; Clock""}]",[]
11,65576,65580,j 4,4194415,"iac, if, iod, do",[65576],[4194415],PC=0x0001002C,{},C,"[{""type"": ""IF"", ""address"": 65576, ""data"": 4194415, ""control"": ""Memory read; ACK; Clock""}]",[]
12,65580,65584,"lw a0, -0xc(s0)",4282656003,"iac, if, iod, oac, of","[65580, 1114052]","[4282656003, 7]",EA=0x0010FFC4,"{""a0"": 7}",PM,"[{""type"": ""IF"", ""address"": 65580, ""data"": 4282656003, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114052, ""data"": 7, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 755, ""hit"": true}]"
13,65584,65588,"ori a0, a0, 0x100",268789011,"iac, if, iod, do",[65584],[268789011],7 OR 256 = 263,"{""a0"": 263}",DP,"[{""type"": ""IF"", ""address"": 65584, ""data"": 268789011, ""control"": ""Memory read; ACK; Clock""}]",[]
14,65588,65592,"sw a0, -0xc(s0)",4272171555,"iac, if, iod, oac, os","[65588, 1114052]","[4272171555, 263]",EA=0x0010FFC4,{},PM,"[{""type"": ""IF"", ""address"": 65588, ""data"": 4272171555, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""W"", ""address"": 1114052, ""data"": 263, ""control"": ""Memory write; ACK; Clock""}]","[{""number"": 756, ""hit"": true}]"
15,65592,65596,j 4,4194415,"iac, if, iod, do",[65592],[4194415],PC=0x0001003C,{},C,"[{""type"": ""IF"", ""address"": 65592, ""data"": 4194415, ""control"": ""Memory read; ACK; Clock""}]",[]
16,65596,65600,"lw a0, -0xc(s0)",4282656003,"iac, if, iod, oac, of","[65596, 1114052]","[4282656003, 263]",EA=0x0010FFC4,"{""a0"": 263}",PM,"[{""type"": ""IF"", ""address"": 65596, ""data"": 4282656003, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114052, ""data"": 263, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 757, ""hit"": true}]"
17,65600,65604,"lw ra, 0xc(sp)",12656771,"iac, if, iod, oac, of","[65600, 1114060]","[12656771, 66264]",EA=0x0010FFCC,"{""ra"": 66264}",PM,"[{""type"": ""IF"", ""address"": 65600, ""data"": 12656771, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114060, ""data"": 66264, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 758, ""hit"": true}]"
18,65604,65608,"lw s0, 8(sp)",8463363,"iac, if, iod, oac, of","[65604, 1114056]","[8463363, 1114112]",EA=0x0010FFC8,"{""s0"": 1114112}",PM,"[{""type"": ""IF"", ""address"": 65604, ""data"": 8463363, ""control"": ""Memory read; ACK; Clock""}, {""type"": ""R"", ""address"": 1114056, ""data"": 1114112, ""control"": ""Memory read; ACK; Clock""}]","[{""number"": 759, ""hit"": true}]"
19,65608,65612,"addi sp, sp, 0x10",16843027,"iac, if, iod, do",[65608],[16843027],"sp, sp, 0x10 => 0x0010FFD0","{""sp"": 1114064}",DP,"[{""type"": ""IF"", ""address"": 65608, ""data"": 16843027, ""control"": ""Memory read; ACK; Clock""}]",[]
20,65612,66264,ret ,32871,"iac, if, iod, do",[65612],[32871],PC=0x000102D8,{},C,"[{""type"": ""IF"", ""address"": 65612, ""data"": 32871, ""control"": ""Memory read; ACK; Clock""}]",[]


```

## İlk 30 cache

```csv

number,rw,address,tag,set,way,offset,hit,evicted,seen_before,dirty_eviction
1,W,0x0010FFFC,0x000043FF,3,0,12,False,,False,False
2,W,0x0010FFF8,0x000043FF,3,0,8,True,,True,False
3,W,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
4,W,0x0010FFEC,0x000043FF,2,0,12,False,,False,False
5,W,0x0010FFE8,0x000043FF,2,0,8,True,,True,False
6,W,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
7,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
8,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
9,W,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
10,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
11,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
12,W,0x00020010,0x00000800,1,0,0,False,,False,False
13,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
14,W,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
15,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
16,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
17,W,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
18,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
19,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
20,W,0x00020014,0x00000800,1,0,4,True,,True,False
21,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
22,W,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
23,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
24,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
25,W,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
26,R,0x0010FFF4,0x000043FF,3,0,4,True,,True,False
27,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
28,W,0x00020018,0x00000800,1,0,8,True,,True,False
29,R,0x0010FFF0,0x000043FF,3,0,0,True,,True,False
30,W,0x0010FFF0,0x000043FF,3,0,0,True,,True,False


```

## Tam sayısal model ve çıktılar

```json

{
  "outputs": {
    "bucket": [
      14,
      1,
      7,
      0,
      8
    ],
    "mean": 51,
    "below_count": 14,
    "pass_count": 15
  },
  "kernel": [
    {
      "number": 1,
      "pc_before": 66260,
      "pc_fetch_next": 66264,
      "pc_after": 65536,
      "assembly": "jalr ra, ra, -0x2d0",
      "IR": 3540025575,
      "states": "iac, if, iod, do",
      "MAR": [
        66260
      ],
      "MBR": [
        3540025575
      ],
      "ALU": "PC=0x00010000",
      "changed": {
        "ra": 66264
      },
      "before": {
        "zero": 0,
        "ra": 66256,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 66260,
          "data": 3540025575,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "C",
      "data_refs": [],
      "cache": [],
      "written": {
        "ra": 66264
      }
    },
    {
      "number": 2,
      "pc_before": 65536,
      "pc_fetch_next": 65540,
      "pc_after": 65540,
      "assembly": "addi sp, sp, -0x10",
      "IR": 4278255891,
      "states": "iac, if, iod, do",
      "MAR": [
        65536
      ],
      "MBR": [
        4278255891
      ],
      "ALU": "sp, sp, -0x10 => 0x0010FFC0",
      "changed": {
        "sp": 1114048
      },
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65536,
          "data": 4278255891,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "DP",
      "data_refs": [],
      "cache": [],
      "written": {
        "sp": 1114048
      }
    },
    {
      "number": 3,
      "pc_before": 65540,
      "pc_fetch_next": 65544,
      "pc_after": 65544,
      "assembly": "sw ra, 0xc(sp)",
      "IR": 1123875,
      "states": "iac, if, iod, oac, os",
      "MAR": [
        65540,
        1114060
      ],
      "MBR": [
        1123875,
        66264
      ],
      "ALU": "EA=0x0010FFCC",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65540,
          "data": 1123875,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "W",
          "address": 1114060,
          "data": 66264,
          "control": "Memory write; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 749,
          "rw": "W",
          "address": 1114060,
          "size": 4,
          "value": 66264,
          "c_line": 8,
          "stack": true,
          "pc": 65540,
          "instruction": 2262
        }
      ],
      "cache": [
        {
          "number": 749,
          "hit": false
        }
      ],
      "written": {}
    },
    {
      "number": 4,
      "pc_before": 65544,
      "pc_fetch_next": 65548,
      "pc_after": 65548,
      "assembly": "sw s0, 8(sp)",
      "IR": 8463395,
      "states": "iac, if, iod, oac, os",
      "MAR": [
        65544,
        1114056
      ],
      "MBR": [
        8463395,
        1114112
      ],
      "ALU": "EA=0x0010FFC8",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65544,
          "data": 8463395,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "W",
          "address": 1114056,
          "data": 1114112,
          "control": "Memory write; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 750,
          "rw": "W",
          "address": 1114056,
          "size": 4,
          "value": 1114112,
          "c_line": 8,
          "stack": true,
          "pc": 65544,
          "instruction": 2263
        }
      ],
      "cache": [
        {
          "number": 750,
          "hit": true
        }
      ],
      "written": {}
    },
    {
      "number": 5,
      "pc_before": 65548,
      "pc_fetch_next": 65552,
      "pc_after": 65552,
      "assembly": "addi s0, sp, 0x10",
      "IR": 16843795,
      "states": "iac, if, iod, do",
      "MAR": [
        65548
      ],
      "MBR": [
        16843795
      ],
      "ALU": "s0, sp, 0x10 => 0x0010FFD0",
      "changed": {
        "s0": 1114064
      },
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65548,
          "data": 16843795,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "DP",
      "data_refs": [],
      "cache": [],
      "written": {
        "s0": 1114064
      }
    },
    {
      "number": 6,
      "pc_before": 65552,
      "pc_fetch_next": 65556,
      "pc_after": 65556,
      "assembly": "sw a0, -0xc(s0)",
      "IR": 4272171555,
      "states": "iac, if, iod, oac, os",
      "MAR": [
        65552,
        1114052
      ],
      "MBR": [
        4272171555,
        7
      ],
      "ALU": "EA=0x0010FFC4",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65552,
          "data": 4272171555,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "W",
          "address": 1114052,
          "data": 7,
          "control": "Memory write; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 751,
          "rw": "W",
          "address": 1114052,
          "size": 4,
          "value": 7,
          "c_line": 8,
          "stack": true,
          "pc": 65552,
          "instruction": 2265
        }
      ],
      "cache": [
        {
          "number": 751,
          "hit": true
        }
      ],
      "written": {}
    },
    {
      "number": 7,
      "pc_before": 65556,
      "pc_fetch_next": 65560,
      "pc_after": 65560,
      "assembly": "sw a1, -0x10(s0)",
      "IR": 4273219619,
      "states": "iac, if, iod, oac, os",
      "MAR": [
        65556,
        1114048
      ],
      "MBR": [
        4273219619,
        51
      ],
      "ALU": "EA=0x0010FFC0",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65556,
          "data": 4273219619,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "W",
          "address": 1114048,
          "data": 51,
          "control": "Memory write; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 752,
          "rw": "W",
          "address": 1114048,
          "size": 4,
          "value": 51,
          "c_line": 8,
          "stack": true,
          "pc": 65556,
          "instruction": 2266
        }
      ],
      "cache": [
        {
          "number": 752,
          "hit": true
        }
      ],
      "written": {}
    },
    {
      "number": 8,
      "pc_before": 65560,
      "pc_fetch_next": 65564,
      "pc_after": 65564,
      "assembly": "lw a0, -0xc(s0)",
      "IR": 4282656003,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65560,
        1114052
      ],
      "MBR": [
        4282656003,
        7
      ],
      "ALU": "EA=0x0010FFC4",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65560,
          "data": 4282656003,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114052,
          "data": 7,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 753,
          "rw": "R",
          "address": 1114052,
          "size": 4,
          "value": 7,
          "c_line": 9,
          "stack": true,
          "pc": 65560,
          "instruction": 2267
        }
      ],
      "cache": [
        {
          "number": 753,
          "hit": true
        }
      ],
      "written": {
        "a0": 7
      }
    },
    {
      "number": 9,
      "pc_before": 65564,
      "pc_fetch_next": 65568,
      "pc_after": 65568,
      "assembly": "lw a1, -0x10(s0)",
      "IR": 4278461827,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65564,
        1114048
      ],
      "MBR": [
        4278461827,
        51
      ],
      "ALU": "EA=0x0010FFC0",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65564,
          "data": 4278461827,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114048,
          "data": 51,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 754,
          "rw": "R",
          "address": 1114048,
          "size": 4,
          "value": 51,
          "c_line": 9,
          "stack": true,
          "pc": 65564,
          "instruction": 2268
        }
      ],
      "cache": [
        {
          "number": 754,
          "hit": true
        }
      ],
      "written": {
        "a1": 51
      }
    },
    {
      "number": 10,
      "pc_before": 65568,
      "pc_fetch_next": 65572,
      "pc_after": 65576,
      "assembly": "blt a0, a1, 8",
      "IR": 11879523,
      "states": "iac, if, iod, do",
      "MAR": [
        65568
      ],
      "MBR": [
        11879523
      ],
      "ALU": "7 < 51: true; PC=0x00010028",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65568,
          "data": 11879523,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "C",
      "data_refs": [],
      "cache": [],
      "written": {}
    },
    {
      "number": 11,
      "pc_before": 65576,
      "pc_fetch_next": 65580,
      "pc_after": 65580,
      "assembly": "j 4",
      "IR": 4194415,
      "states": "iac, if, iod, do",
      "MAR": [
        65576
      ],
      "MBR": [
        4194415
      ],
      "ALU": "PC=0x0001002C",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65576,
          "data": 4194415,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "C",
      "data_refs": [],
      "cache": [],
      "written": {}
    },
    {
      "number": 12,
      "pc_before": 65580,
      "pc_fetch_next": 65584,
      "pc_after": 65584,
      "assembly": "lw a0, -0xc(s0)",
      "IR": 4282656003,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65580,
        1114052
      ],
      "MBR": [
        4282656003,
        7
      ],
      "ALU": "EA=0x0010FFC4",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65580,
          "data": 4282656003,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114052,
          "data": 7,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 755,
          "rw": "R",
          "address": 1114052,
          "size": 4,
          "value": 7,
          "c_line": 10,
          "stack": true,
          "pc": 65580,
          "instruction": 2271
        }
      ],
      "cache": [
        {
          "number": 755,
          "hit": true
        }
      ],
      "written": {
        "a0": 7
      }
    },
    {
      "number": 13,
      "pc_before": 65584,
      "pc_fetch_next": 65588,
      "pc_after": 65588,
      "assembly": "ori a0, a0, 0x100",
      "IR": 268789011,
      "states": "iac, if, iod, do",
      "MAR": [
        65584
      ],
      "MBR": [
        268789011
      ],
      "ALU": "7 OR 256 = 263",
      "changed": {
        "a0": 263
      },
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 7,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65584,
          "data": 268789011,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "DP",
      "data_refs": [],
      "cache": [],
      "written": {
        "a0": 263
      }
    },
    {
      "number": 14,
      "pc_before": 65588,
      "pc_fetch_next": 65592,
      "pc_after": 65592,
      "assembly": "sw a0, -0xc(s0)",
      "IR": 4272171555,
      "states": "iac, if, iod, oac, os",
      "MAR": [
        65588,
        1114052
      ],
      "MBR": [
        4272171555,
        263
      ],
      "ALU": "EA=0x0010FFC4",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65588,
          "data": 4272171555,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "W",
          "address": 1114052,
          "data": 263,
          "control": "Memory write; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 756,
          "rw": "W",
          "address": 1114052,
          "size": 4,
          "value": 263,
          "c_line": 10,
          "stack": true,
          "pc": 65588,
          "instruction": 2273
        }
      ],
      "cache": [
        {
          "number": 756,
          "hit": true
        }
      ],
      "written": {}
    },
    {
      "number": 15,
      "pc_before": 65592,
      "pc_fetch_next": 65596,
      "pc_after": 65596,
      "assembly": "j 4",
      "IR": 4194415,
      "states": "iac, if, iod, do",
      "MAR": [
        65592
      ],
      "MBR": [
        4194415
      ],
      "ALU": "PC=0x0001003C",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65592,
          "data": 4194415,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "C",
      "data_refs": [],
      "cache": [],
      "written": {}
    },
    {
      "number": 16,
      "pc_before": 65596,
      "pc_fetch_next": 65600,
      "pc_after": 65600,
      "assembly": "lw a0, -0xc(s0)",
      "IR": 4282656003,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65596,
        1114052
      ],
      "MBR": [
        4282656003,
        263
      ],
      "ALU": "EA=0x0010FFC4",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65596,
          "data": 4282656003,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114052,
          "data": 263,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 757,
          "rw": "R",
          "address": 1114052,
          "size": 4,
          "value": 263,
          "c_line": 11,
          "stack": true,
          "pc": 65596,
          "instruction": 2275
        }
      ],
      "cache": [
        {
          "number": 757,
          "hit": true
        }
      ],
      "written": {
        "a0": 263
      }
    },
    {
      "number": 17,
      "pc_before": 65600,
      "pc_fetch_next": 65604,
      "pc_after": 65604,
      "assembly": "lw ra, 0xc(sp)",
      "IR": 12656771,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65600,
        1114060
      ],
      "MBR": [
        12656771,
        66264
      ],
      "ALU": "EA=0x0010FFCC",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65600,
          "data": 12656771,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114060,
          "data": 66264,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 758,
          "rw": "R",
          "address": 1114060,
          "size": 4,
          "value": 66264,
          "c_line": 11,
          "stack": true,
          "pc": 65600,
          "instruction": 2276
        }
      ],
      "cache": [
        {
          "number": 758,
          "hit": true
        }
      ],
      "written": {
        "ra": 66264
      }
    },
    {
      "number": 18,
      "pc_before": 65604,
      "pc_fetch_next": 65608,
      "pc_after": 65608,
      "assembly": "lw s0, 8(sp)",
      "IR": 8463363,
      "states": "iac, if, iod, oac, of",
      "MAR": [
        65604,
        1114056
      ],
      "MBR": [
        8463363,
        1114112
      ],
      "ALU": "EA=0x0010FFC8",
      "changed": {
        "s0": 1114112
      },
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114064,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65604,
          "data": 8463363,
          "control": "Memory read; ACK; Clock"
        },
        {
          "type": "R",
          "address": 1114056,
          "data": 1114112,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "PM",
      "data_refs": [
        {
          "number": 759,
          "rw": "R",
          "address": 1114056,
          "size": 4,
          "value": 1114112,
          "c_line": 11,
          "stack": true,
          "pc": 65604,
          "instruction": 2277
        }
      ],
      "cache": [
        {
          "number": 759,
          "hit": true
        }
      ],
      "written": {
        "s0": 1114112
      }
    },
    {
      "number": 19,
      "pc_before": 65608,
      "pc_fetch_next": 65612,
      "pc_after": 65612,
      "assembly": "addi sp, sp, 0x10",
      "IR": 16843027,
      "states": "iac, if, iod, do",
      "MAR": [
        65608
      ],
      "MBR": [
        16843027
      ],
      "ALU": "sp, sp, 0x10 => 0x0010FFD0",
      "changed": {
        "sp": 1114064
      },
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114048,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65608,
          "data": 16843027,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "DP",
      "data_refs": [],
      "cache": [],
      "written": {
        "sp": 1114064
      }
    },
    {
      "number": 20,
      "pc_before": 65612,
      "pc_fetch_next": 65616,
      "pc_after": 66264,
      "assembly": "ret ",
      "IR": 32871,
      "states": "iac, if, iod, do",
      "MAR": [
        65612
      ],
      "MBR": [
        32871
      ],
      "ALU": "PC=0x000102D8",
      "changed": {},
      "before": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "after": {
        "zero": 0,
        "ra": 66264,
        "sp": 1114064,
        "gp": 0,
        "tp": 0,
        "t0": 0,
        "t1": 0,
        "t2": 0,
        "s0": 1114112,
        "s1": 0,
        "a0": 263,
        "a1": 51,
        "a2": 116,
        "a3": 0,
        "a4": 0,
        "a5": 0,
        "a6": 0,
        "a7": 0,
        "s2": 0,
        "s3": 0,
        "s4": 0,
        "s5": 0,
        "s6": 0,
        "s7": 0,
        "s8": 0,
        "s9": 0,
        "s10": 0,
        "s11": 0,
        "t3": 0,
        "t4": 0,
        "t5": 0,
        "t6": 0
      },
      "bus": [
        {
          "type": "IF",
          "address": 65612,
          "data": 32871,
          "control": "Memory read; ACK; Clock"
        }
      ],
      "category": "C",
      "data_refs": [],
      "cache": [],
      "written": {}
    }
  ],
  "kernel_totals": {
    "instruction_fetch": 20,
    "operand_fetch": 6,
    "operand_store": 5,
    "control": [
      1,
      10,
      11,
      15,
      20
    ],
    "nonsequential": [
      1,
      10,
      20
    ],
    "bus32": 31,
    "bus16": 62
  },
  "interrupt": {
    "k": 6,
    "kind": "I/O",
    "interrupted_pc": 65552,
    "instruction": "sw a0, -0xc(s0)",
    "resume_pc": 65556,
    "mepc": 65556,
    "mcause": 2147483659,
    "mtvec": 196608,
    "registers_to_preserve": {
      "zero": 0,
      "ra": 66264,
      "sp": 1114048,
      "gp": 0,
      "tp": 0,
      "t0": 0,
      "t1": 0,
      "t2": 0,
      "s0": 1114064,
      "s1": 0,
      "a0": 7,
      "a1": 51,
      "a2": 116,
      "a3": 0,
      "a4": 0,
      "a5": 0,
      "a6": 0,
      "a7": 0,
      "s2": 0,
      "s3": 0,
      "s4": 0,
      "s5": 0,
      "s6": 0,
      "s7": 0,
      "s8": 0,
      "s9": 0,
      "s10": 0,
      "s11": 0,
      "t3": 0,
      "t4": 0,
      "t5": 0,
      "t6": 0
    },
    "completed_store": {
      "number": 751,
      "rw": "W",
      "address": 1114052,
      "size": 4,
      "value": 7,
      "c_line": 8,
      "stack": true,
      "pc": 65552,
      "instruction": 2265
    },
    "handler_model": "Privileged M-mode scenario, not an injected Unicorn interrupt."
  },
  "first30": {
    "summary": {
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 30,
      "hits": 27,
      "misses": 3,
      "H": 0.9,
      "memory_writes": 0,
      "Ts": 3.999999999999999,
      "speedup": 7.500000000000002,
      "dirty_remaining": [
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131088,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ]
    },
    "snapshot": [
      {
        "line": 0,
        "set": 0,
        "way": 0,
        "valid": false,
        "tag": null,
        "dirty": false,
        "block": null,
        "lru": null
      },
      {
        "line": 1,
        "set": 1,
        "way": 0,
        "valid": true,
        "tag": 2048,
        "dirty": true,
        "block": 131088,
        "lru": 0
      },
      {
        "line": 2,
        "set": 2,
        "way": 0,
        "valid": true,
        "tag": 17407,
        "dirty": true,
        "block": 1114080,
        "lru": 0
      },
      {
        "line": 3,
        "set": 3,
        "way": 0,
        "valid": true,
        "tag": 17407,
        "dirty": true,
        "block": 1114096,
        "lru": 0
      }
    ],
    "rows": [
      {
        "number": 1,
        "rw": "W",
        "address": 1114108,
        "size": 4,
        "value": 262128,
        "c_line": 15,
        "stack": true,
        "pc": 65620,
        "instruction": 2,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 12,
        "hit": false,
        "evicted": null,
        "seen_before": false,
        "dirty_eviction": false
      },
      {
        "number": 2,
        "rw": "W",
        "address": 1114104,
        "size": 4,
        "value": 0,
        "c_line": 15,
        "stack": true,
        "pc": 65624,
        "instruction": 3,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 8,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 3,
        "rw": "W",
        "address": 1114100,
        "size": 4,
        "value": 1230006,
        "c_line": 16,
        "stack": true,
        "pc": 65640,
        "instruction": 7,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 4,
        "rw": "W",
        "address": 1114092,
        "size": 4,
        "value": 0,
        "c_line": 17,
        "stack": true,
        "pc": 65648,
        "instruction": 9,
        "tag": 17407,
        "set": 2,
        "way": 0,
        "offset": 12,
        "hit": false,
        "evicted": null,
        "seen_before": false,
        "dirty_eviction": false
      },
      {
        "number": 5,
        "rw": "W",
        "address": 1114088,
        "size": 4,
        "value": 56,
        "c_line": 17,
        "stack": true,
        "pc": 65656,
        "instruction": 11,
        "tag": 17407,
        "set": 2,
        "way": 0,
        "offset": 8,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 6,
        "rw": "W",
        "address": 1114096,
        "size": 4,
        "value": 0,
        "c_line": 18,
        "stack": true,
        "pc": 65660,
        "instruction": 12,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 7,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 0,
        "c_line": 18,
        "stack": true,
        "pc": 65668,
        "instruction": 14,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 8,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 1230006,
        "c_line": 19,
        "stack": true,
        "pc": 65688,
        "instruction": 18,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 9,
        "rw": "W",
        "address": 1114100,
        "size": 4,
        "value": 3985208477,
        "c_line": 19,
        "stack": true,
        "pc": 65716,
        "instruction": 25,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 10,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 3985208477,
        "c_line": 20,
        "stack": true,
        "pc": 65720,
        "instruction": 26,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 11,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 0,
        "c_line": 20,
        "stack": true,
        "pc": 65752,
        "instruction": 34,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 12,
        "rw": "W",
        "address": 131088,
        "size": 4,
        "value": 7,
        "c_line": 20,
        "stack": false,
        "pc": 65772,
        "instruction": 39,
        "tag": 2048,
        "set": 1,
        "way": 0,
        "offset": 0,
        "hit": false,
        "evicted": null,
        "seen_before": false,
        "dirty_eviction": false
      },
      {
        "number": 13,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 0,
        "c_line": 18,
        "stack": true,
        "pc": 65780,
        "instruction": 41,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 14,
        "rw": "W",
        "address": 1114096,
        "size": 4,
        "value": 1,
        "c_line": 18,
        "stack": true,
        "pc": 65788,
        "instruction": 43,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 15,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 1,
        "c_line": 18,
        "stack": true,
        "pc": 65668,
        "instruction": 45,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 16,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 3985208477,
        "c_line": 19,
        "stack": true,
        "pc": 65688,
        "instruction": 49,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 17,
        "rw": "W",
        "address": 1114100,
        "size": 4,
        "value": 1949658456,
        "c_line": 19,
        "stack": true,
        "pc": 65716,
        "instruction": 56,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 18,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 1949658456,
        "c_line": 20,
        "stack": true,
        "pc": 65720,
        "instruction": 57,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 19,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 1,
        "c_line": 20,
        "stack": true,
        "pc": 65752,
        "instruction": 65,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 20,
        "rw": "W",
        "address": 131092,
        "size": 4,
        "value": 55,
        "c_line": 20,
        "stack": false,
        "pc": 65772,
        "instruction": 70,
        "tag": 2048,
        "set": 1,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 21,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 1,
        "c_line": 18,
        "stack": true,
        "pc": 65780,
        "instruction": 72,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 22,
        "rw": "W",
        "address": 1114096,
        "size": 4,
        "value": 2,
        "c_line": 18,
        "stack": true,
        "pc": 65788,
        "instruction": 74,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 23,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 2,
        "c_line": 18,
        "stack": true,
        "pc": 65668,
        "instruction": 76,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 24,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 1949658456,
        "c_line": 19,
        "stack": true,
        "pc": 65688,
        "instruction": 80,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 25,
        "rw": "W",
        "address": 1114100,
        "size": 4,
        "value": 441356503,
        "c_line": 19,
        "stack": true,
        "pc": 65716,
        "instruction": 87,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 26,
        "rw": "R",
        "address": 1114100,
        "size": 4,
        "value": 441356503,
        "c_line": 20,
        "stack": true,
        "pc": 65720,
        "instruction": 88,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 4,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 27,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 2,
        "c_line": 20,
        "stack": true,
        "pc": 65752,
        "instruction": 96,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 28,
        "rw": "W",
        "address": 131096,
        "size": 4,
        "value": 68,
        "c_line": 20,
        "stack": false,
        "pc": 65772,
        "instruction": 101,
        "tag": 2048,
        "set": 1,
        "way": 0,
        "offset": 8,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 29,
        "rw": "R",
        "address": 1114096,
        "size": 4,
        "value": 2,
        "c_line": 18,
        "stack": true,
        "pc": 65780,
        "instruction": 103,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      },
      {
        "number": 30,
        "rw": "W",
        "address": 1114096,
        "size": 4,
        "value": 3,
        "c_line": 18,
        "stack": true,
        "pc": 65788,
        "instruction": 105,
        "tag": 17407,
        "set": 3,
        "way": 0,
        "offset": 0,
        "hit": true,
        "evicted": null,
        "seen_before": true,
        "dirty_eviction": false
      }
    ],
    "independent_match": true
  },
  "fields_first5": [
    {
      "address": 1114108,
      "binary": "00000000000100001111111111111100",
      "tag": 17407,
      "line": 3,
      "offset": 12
    },
    {
      "address": 1114104,
      "binary": "00000000000100001111111111111000",
      "tag": 17407,
      "line": 3,
      "offset": 8
    },
    {
      "address": 1114100,
      "binary": "00000000000100001111111111110100",
      "tag": 17407,
      "line": 3,
      "offset": 4
    },
    {
      "address": 1114092,
      "binary": "00000000000100001111111111101100",
      "tag": 17407,
      "line": 2,
      "offset": 12
    },
    {
      "address": 1114088,
      "binary": "00000000000100001111111111101000",
      "tag": 17407,
      "line": 2,
      "offset": 8
    }
  ],
  "mapping_sweep": [
    {
      "name": "Direct",
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 1490,
      "hits": 1230,
      "misses": 260,
      "H": 0.825503355704698,
      "memory_writes": 157,
      "Ts": 6.2348993288590595,
      "speedup": 4.81162540365985,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "2-way",
      "capacity": 64,
      "line_size": 16,
      "ways": 2,
      "sets": 2,
      "references": 1490,
      "hits": 1247,
      "misses": 243,
      "H": 0.8369127516778524,
      "memory_writes": 178,
      "Ts": 5.892617449664428,
      "speedup": 5.091116173120731,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 4096,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 0,
          "way": 1,
          "valid": true,
          "tag": 4100,
          "dirty": true,
          "block": 131200,
          "lru": 1
        },
        {
          "line": 2,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 34814,
          "dirty": true,
          "block": 1114064,
          "lru": 1
        },
        {
          "line": 3,
          "set": 1,
          "way": 1,
          "valid": true,
          "tag": 34815,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "4-way",
      "capacity": 64,
      "line_size": 16,
      "ways": 4,
      "sets": 1,
      "references": 1490,
      "hits": 1207,
      "misses": 283,
      "H": 0.8100671140939597,
      "memory_writes": 224,
      "Ts": 6.697986577181209,
      "speedup": 4.478957915831663,
      "dirty_remaining": [
        {
          "line": 1,
          "set": 0,
          "way": 1,
          "valid": true,
          "tag": 8192,
          "dirty": true,
          "block": 131072,
          "lru": 1
        },
        {
          "line": 2,
          "set": 0,
          "way": 2,
          "valid": true,
          "tag": 8200,
          "dirty": true,
          "block": 131200,
          "lru": 2
        },
        {
          "line": 3,
          "set": 0,
          "way": 3,
          "valid": true,
          "tag": 69631,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "Fully associative",
      "capacity": 64,
      "line_size": 16,
      "ways": 4,
      "sets": 1,
      "references": 1490,
      "hits": 1207,
      "misses": 283,
      "H": 0.8100671140939597,
      "memory_writes": 224,
      "Ts": 6.697986577181209,
      "speedup": 4.478957915831663,
      "dirty_remaining": [
        {
          "line": 1,
          "set": 0,
          "way": 1,
          "valid": true,
          "tag": 8192,
          "dirty": true,
          "block": 131072,
          "lru": 1
        },
        {
          "line": 2,
          "set": 0,
          "way": 2,
          "valid": true,
          "tag": 8200,
          "dirty": true,
          "block": 131200,
          "lru": 2
        },
        {
          "line": 3,
          "set": 0,
          "way": 3,
          "valid": true,
          "tag": 69631,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    }
  ],
  "line_sweep": [
    {
      "name": "8 B",
      "capacity": 64,
      "line_size": 8,
      "ways": 1,
      "sets": 8,
      "references": 1490,
      "hits": 1284,
      "misses": 206,
      "H": 0.8617449664429531,
      "memory_writes": 130,
      "Ts": 5.147651006711408,
      "speedup": 5.827900912646677,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2050,
          "dirty": true,
          "block": 131200,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131080,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 2049,
          "dirty": true,
          "block": 131152,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114072,
          "lru": 0
        },
        {
          "line": 4,
          "set": 4,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 5,
          "set": 5,
          "way": 0,
          "valid": true,
          "tag": 2049,
          "dirty": true,
          "block": 131176,
          "lru": 0
        },
        {
          "line": 6,
          "set": 6,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "16 B",
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 1490,
      "hits": 1230,
      "misses": 260,
      "H": 0.825503355704698,
      "memory_writes": 157,
      "Ts": 6.2348993288590595,
      "speedup": 4.81162540365985,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "32 B",
      "capacity": 64,
      "line_size": 32,
      "ways": 1,
      "sets": 2,
      "references": 1490,
      "hits": 1160,
      "misses": 330,
      "H": 0.7785234899328859,
      "memory_writes": 213,
      "Ts": 7.644295302013424,
      "speedup": 3.924495171202809,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "name": "64 B",
      "capacity": 64,
      "line_size": 64,
      "ways": 1,
      "sets": 1,
      "references": 1490,
      "hits": 1028,
      "misses": 462,
      "H": 0.6899328859060403,
      "memory_writes": 301,
      "Ts": 10.302013422818792,
      "speedup": 2.9120521172638436,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114048,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    }
  ],
  "extra_configurations": [
    {
      "policy": "WB",
      "capacity": 128,
      "line_size": 16,
      "ways": 1,
      "sets": 8,
      "references": 1490,
      "hits": 1369,
      "misses": 121,
      "H": 0.9187919463087248,
      "memory_writes": 74,
      "Ts": 3.4362416107382545,
      "speedup": 8.730468750000002,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 1024,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 1024,
          "dirty": true,
          "block": 131088,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 1024,
          "dirty": true,
          "block": 131104,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 1024,
          "dirty": true,
          "block": 131120,
          "lru": 0
        },
        {
          "line": 4,
          "set": 4,
          "way": 0,
          "valid": true,
          "tag": 8703,
          "dirty": true,
          "block": 1114048,
          "lru": 0
        },
        {
          "line": 5,
          "set": 5,
          "way": 0,
          "valid": true,
          "tag": 8703,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 6,
          "set": 6,
          "way": 0,
          "valid": true,
          "tag": 8703,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 7,
          "set": 7,
          "way": 0,
          "valid": true,
          "tag": 8703,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "policy": "WB",
      "capacity": 256,
      "line_size": 16,
      "ways": 1,
      "sets": 16,
      "references": 1490,
      "hits": 1476,
      "misses": 14,
      "H": 0.9906040268456375,
      "memory_writes": 0,
      "Ts": 1.281879194630874,
      "speedup": 23.403141361256516,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131088,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131104,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131120,
          "lru": 0
        },
        {
          "line": 4,
          "set": 4,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131136,
          "lru": 0
        },
        {
          "line": 5,
          "set": 5,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131152,
          "lru": 0
        },
        {
          "line": 6,
          "set": 6,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131168,
          "lru": 0
        },
        {
          "line": 7,
          "set": 7,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131184,
          "lru": 0
        },
        {
          "line": 8,
          "set": 8,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131200,
          "lru": 0
        },
        {
          "line": 9,
          "set": 9,
          "way": 0,
          "valid": true,
          "tag": 512,
          "dirty": true,
          "block": 131216,
          "lru": 0
        },
        {
          "line": 12,
          "set": 12,
          "way": 0,
          "valid": true,
          "tag": 4351,
          "dirty": true,
          "block": 1114048,
          "lru": 0
        },
        {
          "line": 13,
          "set": 13,
          "way": 0,
          "valid": true,
          "tag": 4351,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 14,
          "set": 14,
          "way": 0,
          "valid": true,
          "tag": 4351,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 15,
          "set": 15,
          "way": 0,
          "valid": true,
          "tag": 4351,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    },
    {
      "policy": "WT",
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 1490,
      "hits": 1230,
      "misses": 260,
      "H": 0.825503355704698,
      "memory_writes": 502,
      "Ts": 6.2348993288590595,
      "speedup": 4.81162540365985,
      "dirty_remaining": [],
      "outputs": {
        "bucket": [
          14,
          1,
          7,
          0,
          8
        ],
        "mean": 51,
        "below_count": 14,
        "pass_count": 15
      }
    }
  ],
  "cache": {
    "O0": {
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 1490,
      "hits": 1230,
      "misses": 260,
      "H": 0.825503355704698,
      "memory_writes": 157,
      "Ts": 6.2348993288590595,
      "speedup": 4.81162540365985,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ]
    },
    "O1": {
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 193,
      "hits": 131,
      "misses": 62,
      "H": 0.6787564766839378,
      "memory_writes": 43,
      "Ts": 10.637305699481866,
      "speedup": 2.8202630297126157,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 2049,
          "dirty": true,
          "block": 131152,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 2049,
          "dirty": true,
          "block": 131168,
          "lru": 0
        }
      ]
    },
    "V2": {
      "capacity": 64,
      "line_size": 16,
      "ways": 1,
      "sets": 4,
      "references": 1550,
      "hits": 1291,
      "misses": 259,
      "H": 0.8329032258064516,
      "memory_writes": 165,
      "Ts": 6.012903225806452,
      "speedup": 4.989270386266094,
      "dirty_remaining": [
        {
          "line": 0,
          "set": 0,
          "way": 0,
          "valid": true,
          "tag": 2048,
          "dirty": true,
          "block": 131072,
          "lru": 0
        },
        {
          "line": 1,
          "set": 1,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114064,
          "lru": 0
        },
        {
          "line": 2,
          "set": 2,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114080,
          "lru": 0
        },
        {
          "line": 3,
          "set": 3,
          "way": 0,
          "valid": true,
          "tag": 17407,
          "dirty": true,
          "block": 1114096,
          "lru": 0
        }
      ]
    }
  },
  "performance": {
    "O0": {
      "classes": {
        "ALU": 1437,
        "Store": 502,
        "Branch/jump": 860,
        "Load": 988,
        "Çarpma": 91
      },
      "Ic": 3878,
      "base_cycles": 4920,
      "CPI": 1.2686952037132542,
      "tau_ns": 0.625,
      "T_base_ns": 3075.0,
      "MIPS": 1261.138211382114,
      "m": 0.3842186694172254,
      "T_no_cache_ns": 31012.5,
      "T_cache_ns": 8881.25,
      "cache_cycles": 14210,
      "Ts": 6.2348993288590595,
      "H": 0.825503355704698,
      "data_references": 1490,
      "cache_speedup": 3.4919071076706545
    },
    "O1": {
      "classes": {
        "ALU": 517,
        "Store": 123,
        "Çarpma": 91,
        "Branch/jump": 229,
        "Load": 70
      },
      "Ic": 1030,
      "base_cycles": 1441,
      "CPI": 1.3990291262135923,
      "tau_ns": 0.625,
      "T_base_ns": 900.625,
      "MIPS": 1143.6502428868841,
      "m": 0.18737864077669902,
      "T_no_cache_ns": 4519.375,
      "T_cache_ns": 2183.75,
      "cache_cycles": 3494,
      "Ts": 10.637305699481866,
      "H": 0.6787564766839378,
      "data_references": 193,
      "cache_speedup": 2.069547796222095
    },
    "V2": {
      "classes": {
        "ALU": 1317,
        "Store": 532,
        "Branch/jump": 860,
        "Load": 1018,
        "Çarpma": 91
      },
      "Ic": 3818,
      "base_cycles": 4860,
      "CPI": 1.2729177579884756,
      "tau_ns": 0.625,
      "T_base_ns": 3037.5,
      "MIPS": 1256.954732510288,
      "m": 0.40597171293871137,
      "T_no_cache_ns": 32100.0,
      "T_cache_ns": 8862.5,
      "cache_cycles": 14180,
      "Ts": 6.012903225806452,
      "H": 0.8329032258064516,
      "data_references": 1550,
      "cache_speedup": 3.6220028208744712
    }
  },
  "amdahl": {
    "c_lines": "33-37 ve çağrılan 7-12",
    "phase_instructions": 1632,
    "phase_references": 748,
    "phase_cycles": 7991,
    "total_cycles": 14210,
    "f": 0.5623504574243491,
    "Nc": 5,
    "speedup": 1.8177864196899145,
    "limit": 2.284933269014311,
    "assumption": "Iterasyonlar farklı grades[i] hücrelerine yazar; mean salt okunur. below_count için thread-local sayım + reduction gerekir. Reduction ve iş parçacığı maliyeti yok sayılmış ideal üst sınırdır."
  },
  "conflicts": [
    {
      "old": 131072,
      "new": 1114048,
      "line": 0,
      "count": 30
    },
    {
      "old": 1114048,
      "new": 131072,
      "line": 0,
      "count": 23
    },
    {
      "old": 1114096,
      "new": 131120,
      "line": 3,
      "count": 20
    },
    {
      "old": 131120,
      "new": 1114096,
      "line": 3,
      "count": 20
    },
    {
      "old": 1114096,
      "new": 131184,
      "line": 3,
      "count": 20
    },
    {
      "old": 131184,
      "new": 1114096,
      "line": 3,
      "count": 20
    }
  ],
  "associativity_tradeoff": {
    "direct_hit_fa_miss": 104,
    "direct_miss_fa_hit": 81,
    "examples": [
      {
        "number": 294,
        "address": 1114096,
        "pc": 66124,
        "fa_evicted": 131088
      },
      {
        "number": 311,
        "address": 131076,
        "pc": 66104,
        "fa_evicted": 1114096
      },
      {
        "number": 313,
        "address": 1114096,
        "pc": 66124,
        "fa_evicted": 131088
      }
    ]
  },
  "all_cache_outputs_invariant": true,
  "trace_stats": {
    "O0": {
      "references": 1490,
      "loads": 988,
      "stores": 502,
      "stack": 1191,
      "array": 150
    },
    "O1": {
      "references": 193,
      "loads": 70,
      "stores": 123,
      "stack": 6,
      "array": 120
    },
    "V2": {
      "references": 1550,
      "loads": 1018,
      "stores": 532,
      "stack": 1251,
      "array": 120
    }
  },
  "symbols": {
    "O0": {
      "mark_below": 65536,
      "main": 65616,
      "grades": 131088,
      "bucket": 131208,
      "pass_count": 131076,
      "mean": 131080,
      "below_count": 131084
    },
    "O1": {
      "mark_below": 65536,
      "main": 65552,
      "grades": 131084,
      "bucket": 131204,
      "pass_count": 131072,
      "mean": 131076,
      "below_count": 131080
    },
    "V2": {
      "mark_below": 65536,
      "main": 65616,
      "grades": 131088,
      "bucket": 131208,
      "pass_count": 131076,
      "mean": 131080,
      "below_count": 131084
    }
  },
  "speedup_O0_O1": 4.066971951917573,
  "pcie": {
    "payload": 120,
    "header12": {
      "total": 140,
      "efficiency": 0.8571428571428571,
      "encoded": 0.843956043956044
    },
    "header16": {
      "total": 148,
      "efficiency": 0.8108108108108109,
      "encoded": 0.7983367983367984
    }
  }
}

```

## Architecture/organization

Instruction formatı | Architecture | 32 bit R/I/S/B/U/J kodlama sözleşmesi | M2’deki word/bit tabloları kanıttır. Format değişip binary aynı kalırsa çözümleme garanti edilmez.

32 görünür GPR | Architecture | Register numaraları ISA’nın alanlarında kodlanır | O1 x16 ve üstünü kullanır. Yalnız 16 GPR olan ISA aynı binary’yi çalıştıramaz; yeniden derleme gerekir.

Base+immediate adresleme | Architecture | lw/sw effective-address sözleşmesi | s0-12=0x0010FFC4. -12 sıfır genişletilse adres değişir; gerçek izde buradan 7 okunur.

Interrupt CSR mekanizması | Architecture | mepc/mcause/mtvec/mstatus yazılıma açık sözleşmedir | ISR veri ve context’i korursa devam durumu aynıdır; burada CSR geçişi ayrı mimari senaryo olarak gösterildi.

Cache kapasitesi | Organization | Aynı ISA’nın uygulanma tercihi | 64/128/256 B replay’lerinde bütün Y7 ve 30 eleman aynı; H ve trafik değişir.

Cache mapping | Organization | Direct / set-assoc. yerleşim tercihi | Direct, 2-way, 4-way, fully associative üzerinde tüm sonuçlar aynı; hit sayıları farklı.

Cache line boyu | Organization | Bloğun fiziksel aktarım / yerleşim boyu | 8/16/32/64 B replay’lerinde sonuçlar aynı; H %86.17’den %68.99’a değişir.

Write policy | Organization | WB / WT bellek trafiği kararı | WB ve WT aynı sonuçları verir; WB 157 dirty eviction, WT 502 bellek yazması üretir.

Data bus genişliği | Organization | 32 bit word’ün aktarım biçimi | Her word iki 16 bit yarımdan yeniden kurulunca aynı çıkar. Bus transferleri 31’den 62’ye çıkar; Y7 değişmez.

Saat frekansı | Organization | Aynı ISA’nın zamanlama tercihi | Bu modelde frekans yalnız tau’yu ölçekler; bit işlemleri değişmez. 1.6 -> 3.2 GHz aynı sonucu yarı model süresinde verir.

## IAS register eşlemesi

MBR | Bellekten gelen / belleğe giden word | Yazılımda görünmez; kavramsal veri tamponu | Hayır

MAR | Erişilen bellek adresi | Yazılımda görünmez; load/store adres hesabı | Hayır

IR | Yürütülen instruction | Kavramsal decode instruction durumu | Hayır

IBR | IAS word içindeki sağ instruction | RV32IM’de yazılıma görünür IBR yok | Hayır

PC | Sonraki instruction adresi | Kontrol akışının mimari PC durumu | Evet; GPR değildir

AC | Tek accumulator / ALU sonucu | Özel AC yok; örnekte x10/a0 kullanılıyor | a0 görünür; özel AC yok

MQ | Çarpım/bölümün diğer parçası | Özel MQ yok; MUL/MULH sonuçları seçilen GPR’ye yazılır | GPR görünür; özel MQ yok

## Kaynaklar

RISC-V Privileged Architecture, version 20240411 - https://docs.riscv.org/reference/isa/v20240411/_attachments/riscv-privileged.pdf - mstatus §3.1.6.1, basılı s.26/PDF s.32; mtvec §3.1.7 s.34/PDF40; mepc §3.1.14 s.41-42/PDF47-48; mcause §3.1.15 s.42-43/PDF48-49; MRET §3.3.2 s.51/PDF57.

Stallings, Computer Organization and Architecture, 10. baskı - https://os.ecci.ucr.ac.cr/ci0114/material/Stallings/Computer-Organization-and-Architecture-10th-William-Stallings.pdf - Ch.3 Fig.3.4-3.6 s.86-88; interrupt Fig.3.9/3.13 s.93/96; QPI Fig.3.17-3.18 s.103-104; PCIe Fig.3.25 s.114-115; I/O opcode 3/7 Problem3.1 s.116.

Intel X58 Express Chipset Datasheet - https://www.intel.com.au/content/dam/doc/datasheet/x58-express-chipset-datasheet.pdf - §3.1.1, s.29: tam genişlik QPI 20 bit phit / 80 bit flit örneği.

## YZ kaydı

ChatGPT/Codex: iz/model denetimi, hata düzeltimi ve tablo/rapor desteği; örnek istek: Final paketini M3 + M4 olarak tamamla. Tabloların hesabı araçlarla otomatikleştirildi.