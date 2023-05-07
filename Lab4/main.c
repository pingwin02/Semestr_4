#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void ex1()
{
    int count[4][4] = { {0} };
    double possibilityX[] = { 0.1, 0.2, 0.3, 0.4 };
    double possibilityY[] = { 0.1, 0.2, 0.3, 0.4 };

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            printf("%0.2f\t", possibilityX[i] * possibilityY[j]);
        }
        printf("\n");
    }

    printf("\n");

    for (int i = 0; i < 100000; i++)
    {
        double randomX = (double)rand() / RAND_MAX;
        double randomY = (double)rand() / RAND_MAX;

        int x = 0, y = 0;
        double possibility = 0;

        for (int j = 0; j < 4; j++)
        {
            possibility += possibilityX[j];
            if (randomX < possibility)
            {
                x = j;
                break;
            }
        }

        possibility = 0;
        for (int j = 0; j < 4; j++)
        {
            possibility += possibilityY[j];
            if (randomY < possibility)
            {
                y = j;
                break;
            }
        }

        count[y][x]++;
    }

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            printf("%d\t", count[i][j]);
        }
        printf("\n");
    }
}

int main()
{
    srand(time(NULL));
    ex1();
    return 0;
}
