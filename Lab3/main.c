#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void ex1()
{
    int count[] = { 0, 0, 0, 0 };
    double possibilityArr[] = { 0.15, 0.35, 0.25, 0.25 };

    for (int i = 0; i < 100000; i++)
    {
        double random = (double)rand() / RAND_MAX;
        double possibility = 0;
        for (int j = 0; j < 4; j++)
        {
            possibility += possibilityArr[j];
            if (random < possibility)
            {
                count[j]++;
                break;
            }
        }
    }

    for (int i = 0; i < 4; i++)
    {
        printf("%d: %d\n", i + 1, count[i]);
    }
}

void ex2()
{
    int count[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    for (int i = 0; i < 100000; i++)
    {
        double random = (double)rand() / RAND_MAX;
        random = random * 100.0 + 50.0;
        for (int j = 0; j < 10; j++)
        {
            if (random >= 50.0 + j * 10.0 && random < 50.0 + (j + 1.0) * 10.0)
            {
                count[j]++;
                break;
            }
        }
    }

    for (int i = 0; i < 10; i++)
    {
        printf("%d: %d\n", i + 1, count[i]);
    }
}

int main()
{
    srand(time(NULL));
    ex1();
    printf("\n");
    ex2();
    return 0;
}
