# CMPE3209 - M1

Ali Bal | 5001230006 | G2 Sınav notu dağılımı | RV32IM

## Ne yapıyor?

Program öğrenci numarasından 30 not üretiyor. Notları beş aralıkta sayıyor,
tamsayı ortalamayı buluyor ve 56 veya üstü alanları geçen olarak sayıyor.
Son geçişte ortalamanın altındaki notların 8. bitini OR 0x100 ile işaretliyor.
Notları gruplama ve geçme hesabı, işaretleme yapılmadan önce tamamlanıyor.

## Numara ve parametreler

Tam öğrenci numarası 5001230006, signed 32 bit sınırını aştığından C kodundaki
SID son 9 hanenin sayısal değeri olan 1230006'dır (001230006).
Kişisel parametreler tam numaradan hesaplanmıştır: d=6, D2=06, S=17, N=30.
Cache: 64 B / 16 B line / direct / 4 line; write-back, write-allocate.
k=6, I/O, Nc=5; f=1.6 GHz; T1=1 cycle, T2=30 cycle.
Bu donanım değerleri model varsayımlarıdır. Word/line/tag: 4/2/26 bit.

## Doğrulama

Zig 0.13.0 içindeki Clang 18.1.6 ile C99, -O0, RV32IM/ILP32 derlendi.
Unicorn 2.1.4 üzerinde ELF yüklendi; main girişinden başlatıldı, SP=0x00110000,
RA=0x0003FFF0 dönüş sentinel'i kullanıldı. Bellek sıfırdan başlatıldı.
Bağımsız Python hesabıyla tüm global sonuçlar ve işaretlenmiş 30 eleman karşılaştırıldı.

Sonuç: bucket={14,1,7,0,8}, mean=51, below_count=14, pass_count=15; toplam=1553.
Gerçek adresler ve yürütülen kernel evidence/verification.json dosyasındadır.
Kernel, i=0 çağrısındaki jalr ile başlar ve mark_below dönüşünde biter (20 instruction).
Store'ların kernel içinde stack'e, C satır 35'te ise ana diziye yapıldığına dikkat edilmelidir.

Kurulum: Python paketleri `unicorn==2.1.4 pyelftools==0.33 capstone==5.0.9 ziglang==0.13.0`.
Derleme: `powershell -File tools/build.ps1` (zig yolunu kurulumuna göre ayarla).
Doğrulama: `python tools/verify.py`.

## YZ kullanımı ve teslim durumu

Kodun denetlenmesi ve derleme hatalarının giderilmesinde ChatGPT/Codex desteği kullanıldı.
Programın sonuçları RV32IM belleği ve bağımsız hesapla karşılaştırıldı.

M2 ve final aşamaları tamamlanmış gibi gösterilmemiştir. Program çıktısının
kanıtı JSON bellek dökümüdür; üretilen görsel döküm bir GUI simülatör ekran görüntüsü değildir.
GitHub deposu: https://github.com/AliBal7/cmpe3209-proje (özel).
Yerel main dalında atomik commit'ler ve M1 etiketi bulunur.
