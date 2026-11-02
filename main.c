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
