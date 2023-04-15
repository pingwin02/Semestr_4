#include <iostream>
#include <stdlib.h> /* srand, rand */
#include <time.h>   /* time */

using namespace std;

void zad1()
{
    int trafionePrzedzialy[] = { 0, 0, 0, 0 };
    double przedzialyPrawdopodobienstwo[] = { 0.2, 0.4, 0.3, 0.1 };

    for (int i = 0; i < 100000; i++)
    {
        double losowaLiczba = (double)rand() / (double)RAND_MAX;
        double prawdopodobienstwo = 0;
        for (int j = 0; j < 4; j++)
        {
            prawdopodobienstwo += przedzialyPrawdopodobienstwo[j];
            if (losowaLiczba < prawdopodobienstwo)
            {
                trafionePrzedzialy[j]++;
                break;
            }
        }
    }

    cout << "--- ZADANIE 1 ---" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << "Przedzial " << i + 1 << ": " << trafionePrzedzialy[i] << endl;
    }
}

void zad2()
{
    int przedzialy[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

    for (int i = 0; i < 100000; i++)
    {
        double losowaLiczba = (double)rand() / (double)RAND_MAX;
        losowaLiczba = losowaLiczba * 100 + 50;
        for (int j = 0; j < 10; j++)
        {
            if (losowaLiczba >= 50 + j * 10 && losowaLiczba < 50 + (j + 1) * 10)
            {
                przedzialy[j]++;
                break;
            }
        }
    }

    cout << "--- ZADANIE 2 ---" << endl;
    for (int i = 0; i < 10; i++)
    {
        cout << "Przedzial " << i + 1 << ": " << przedzialy[i] << endl;
    }
}

int main()
{
    srand(time(NULL));
    zad1();
    zad2();
    return 0;
}
