#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void ex1()
{
    int count[4][4] = { {0.0} };
    double possibilities[4][4] = { {0.0, 0.0, 0.4, 0.1}, {0.0, 0.0, 0.0, 0.15}, {0.2, 0.0, 0.0, 0.0}, {0.1, 0.0, 0.05, 0.0} };
    double possibilityX[4] = { 0.0 };
    double possibilityY[4][4] = { {0.0} };

    for (int i = 0; i < 4; i++)
    {
		double sum = 0;
        for (int j = 0; j < 4; j++)
        {
			sum += possibilities[i][j];
		}
		possibilityX[i] = sum;
	}

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
			possibilityY[i][j] = possibilities[i][j] / possibilityX[i];
		}
	}
      
    for (int i = 0; i < 100000; i++)
    {
        double randomX = (double)rand() / RAND_MAX;
        double randomY = (double)rand() / RAND_MAX;

        int x = -1, y = -1;
        double possibility = 0;

        for (int j = 0; j < 4; j++)
        {
            possibility += possibilityX[j];
            if (randomX < possibility || possibility > 1 - 1e-10)
            {
                x = j;
                break;
            }
        }

        possibility = 0;
        for (int j = 0; j < 4; j++)
        {
            possibility += possibilityY[x][j];
            if (randomY < possibility || possibility > 1 - 1e-10)
            {
                y = j;
                break;
            }
        }

        count[x][y]++;
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
