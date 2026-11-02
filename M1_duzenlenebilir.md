# Ali Bal - CMPE3209 M1

5001230006 | alibal@ogr.iu.edu.tr

Notları öğrenci numaramdan LCG ile üretip global grades dizisinde tutuyorum. İkinci geçişte notları beş aralıkta sayıp toplamı ve geçen kişi sayısını buluyorum. Tamsayı ortalamayı hesapladıktan sonra üçüncü geçişte mark_below fonksiyonuyla ortalamanın altındaki notları OR 0x100 ile işaretliyorum. Sonuçları simülatörde bellekten okuyabilmek için global değişkenlerde saklıyorum.

- d / D2 / S: d = 6; D2 = 06; S = 5+0+0+1+2+3+0+0+0+6 = 17
- N: 24 + (6 mod 25) = 30 eleman; 30 × 4 = 120 byte
- Cache: d=6: 64 byte / 16 byte line / direct mapping / 4 line / set yok
- Write policy: 6 çift: write-back; write miss için write-allocate (varsayım)
- k / Interrupt: (17 mod 7)+3 = 6; 17 tek: I/O
- f: 1.0 + 0.1 × 6 = 1.6 GHz (varsayım)
- T1 / T2: T1=1 cycle; T2=20+5×(6 mod 4)=30 cycle (varsayım)
- Nc: 2 + (17 mod 7) = 5 çekirdek (varsayım)
- Görev parametresi: P=50+(1230006 mod 10)=56; P ve üstü geçer
- Adres alanları: 32 bit: word=log2(16)=4, line=log2(4)=2, tag=32-4-2=26 bit; s=28. Toplam=32 bit.

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

- Y1 | 4, 18-21, 22-31, 33-37: Global int grades[30]; üretme, sayma ve işaretleme geçişleri.
- Y2 | 9, 25-30, 36: if ile ortalama, not aralığı ve geçme koşulları.
- Y3 | 7-12, 35: mark_below iki parametre alır, işaretli notu döndürür.
- Y4 | 19-20, 24, 10, 36: Toplama, çarpma, shift, OR ve AND kullanılır.
- Y5 | 20, 35: Üretilen ve işaretlenen değer grades[i] adresine yazılır.
- Y6 | 2, 16-17: const int SID; LCG başlangıcını ve geçme notunu etkiler.
- Y7 | 5, 25-32, 36: bucket, mean, below_count, pass_count global sonuçlardır.

Doğrulama: {
  "student_number": "5001230006",
  "SID": 1230006,
  "original": [
    7,
    55,
    68,
    100,
    97,
    95,
    23,
    65,
    1,
    16,
    18,
    99,
    45,
    41,
    86,
    66,
    70,
    6,
    35,
    13,
    74,
    4,
    68,
    96,
    96,
    91,
    66,
    20,
    3,
    29
  ],
  "sum": 1553,
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
  "addresses": {
    "bucket": "0x00020088",
    "mean": "0x00020008",
    "below_count": "0x0002000C",
    "pass_count": "0x00020004"
  },
  "instruction_count": 3878,
  "kernel": [
    {
      "address": 66260,
      "hex": "e78000d3",
      "mnemonic": "jalr",
      "operands": "ra, ra, -0x2d0"
    },
    {
      "address": 65536,
      "hex": "130101ff",
      "mnemonic": "addi",
      "operands": "sp, sp, -0x10"
    },
    {
      "address": 65540,
      "hex": "23261100",
      "mnemonic": "sw",
      "operands": "ra, 0xc(sp)"
    },
    {
      "address": 65544,
      "hex": "23248100",
      "mnemonic": "sw",
      "operands": "s0, 8(sp)"
    },
    {
      "address": 65548,
      "hex": "13040101",
      "mnemonic": "addi",
      "operands": "s0, sp, 0x10"
    },
    {
      "address": 65552,
      "hex": "232aa4fe",
      "mnemonic": "sw",
      "operands": "a0, -0xc(s0)"
    },
    {
      "address": 65556,
      "hex": "2328b4fe",
      "mnemonic": "sw",
      "operands": "a1, -0x10(s0)"
    },
    {
      "address": 65560,
      "hex": "032544ff",
      "mnemonic": "lw",
      "operands": "a0, -0xc(s0)"
    },
    {
      "address": 65564,
      "hex": "832504ff",
      "mnemonic": "lw",
      "operands": "a1, -0x10(s0)"
    },
    {
      "address": 65568,
      "hex": "6344b500",
      "mnemonic": "blt",
      "operands": "a0, a1, 8"
    },
    {
      "address": 65576,
      "hex": "6f004000",
      "mnemonic": "j",
      "operands": "4"
    },
    {
      "address": 65580,
      "hex": "032544ff",
      "mnemonic": "lw",
      "operands": "a0, -0xc(s0)"
    },
    {
      "address": 65584,
      "hex": "13650510",
      "mnemonic": "ori",
      "operands": "a0, a0, 0x100"
    },
    {
      "address": 65588,
      "hex": "232aa4fe",
      "mnemonic": "sw",
      "operands": "a0, -0xc(s0)"
    },
    {
      "address": 65592,
      "hex": "6f004000",
      "mnemonic": "j",
      "operands": "4"
    },
    {
      "address": 65596,
      "hex": "032544ff",
      "mnemonic": "lw",
      "operands": "a0, -0xc(s0)"
    },
    {
      "address": 65600,
      "hex": "8320c100",
      "mnemonic": "lw",
      "operands": "ra, 0xc(sp)"
    },
    {
      "address": 65604,
      "hex": "03248100",
      "mnemonic": "lw",
      "operands": "s0, 8(sp)"
    },
    {
      "address": 65608,
      "hex": "13010101",
      "mnemonic": "addi",
      "operands": "sp, sp, 0x10"
    },
    {
      "address": 65612,
      "hex": "67800000",
      "mnemonic": "ret",
      "operands": ""
    }
  ],
  "kernel_first": "0x000102D4",
  "kernel_last": "0x0001004C",
  "status": "PASS: RV32IM memory equals independent Python reference"
}

YZ kullanım beyanı: README.md. Öğrenci imzası ve öğretim üyesi onayı eklenmemiştir.
