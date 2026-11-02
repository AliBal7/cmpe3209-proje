# M1 - Kısa anlatım

Bu projede sınav notlarını işleyen küçük bir C programı var.

1. Öğrenci numarandan 30 not üretiliyor; her çalıştırmada aynı notlar geliyor.
2. Notlar 0-49, 50-64, 65-74, 75-84 ve 85-100 aralıklarında sayılıyor.
3. Toplam 1553; tamsayı ortalama 51 oluyor. 56 ve üstü alan 15 kişi geçiyor.
4. Ortalamanın altındaki 14 not, 0x100 ile OR yapılarak işaretleniyor.
   Örneğin 7 sayısı 263 oluyor: 7 | 256 = 263. Alt 8 bitte asıl not korunuyor.
5. Sonuçlar ekrana yazılmıyor; global değişkenlerden bellek üzerinden okunuyor.

## Numarada neden 1230006 yazıyor?

5001230006, signed 32 bit int sınırından büyük. Ödevin kuralı gereği son 9 haneyi
alıyoruz: 001230006 = 1230006. Kişisel parametrelerde tam numara kullanılıyor.

## Parametreler

- Hane toplamı 17, dizi boyu 30.
- Cache 64 byte; her line 16 byte, toplam 4 line. Direct mapping ve write-back.
- 32 bit adres: tag 26 bit, line 2 bit, word/byte offset 4 bit.
- Interrupt: 6. instruction sırasında I/O.
- Saat 1.6 GHz, T1=1 cycle, T2=30 cycle, 5 çekirdek: model varsayımları.

## Hoca sorarsa

- Neden üç geçiş? Önce veriyi üretmek, sonra istatistiği çıkarmak, en son ortalamaya göre işaretlemek için.
- Neden önce işaretlemiyoruz? OR 0x100 sayıyı değiştirir; önce yaparsak toplam ve not aralıkları yanlış çıkar.
- mark_below ne yapar? Not ve ortalama alır; not düşükse 8. biti set eder ve sonucu döndürür.
- Neden RV32IM? 32 bit sabit instruction; M uzantısıyla çarpma ve bölme var.
- Kernel ne? Programın i=0 çağrısından seçilmiş 20 dinamik instruction. Load, store,
  ALU, koşullu branch ve fonksiyon çağrısı/dönüşü içeriyor. Başlangıç/bitiş adresleri
  sıralı bir bellek aralığı değil, gerçek yürütme akışındaki ilk ve son adres.

## Teslim

PDF klasöründeki Tutanak resmi belge; Oneri iki sayfalık özet.
main.c kaynak kod. GitHub deposu özel, M1 etiketi teslim sürümünü gösteriyor.
Öğretim üyesinin özel depoya erişmesi gerekiyorsa ayrıca erişim verilmelidir.
İmza ve öğretim üyesi onayı otomatik doldurulmadı.
