#include <unistd.h>
#include <stdio.h>
#include <ctype.h>

#define ODCZYT 0
#define ZAPIS 1

int main()
{
    int potok[2];
    int potok2[2];
    char x[100];
    pipe(potok);
    pipe(potok2);
    if (fork())
    {
        puts("Proces pisania na ekran");
        close(potok[ZAPIS]);
        puts("Czekam...");
        read(potok[ODCZYT], &x, sizeof(x));
        printf("Wiadomosc odczytana %s \n", x);
        close(potok[ODCZYT]);
    }
    else
    {
        if (fork())
        {
            puts("Proces zamiana na duze");
            puts("Czekam...");
            close(potok2[ZAPIS]);
            close(potok[ODCZYT]);
            read(potok2[ODCZYT], &x, sizeof(x));

            for (int i = 0; i < sizeof(x); i++)
            {
                x[i] = toupper(x[i]);
            }

            write(potok[ZAPIS], &x, sizeof(x));
            close(potok[ZAPIS]);
            close(potok2[ODCZYT]);
        }
        else
        {
            puts("Proces wczytania z konsoli");
            close(potok2[ODCZYT]);
            fgets(x, sizeof(x), stdin);
            write(potok2[ZAPIS], &x, sizeof(x));
            puts("Proces wczytania z konsoli koniec");
            close(potok2[ZAPIS]);
        }
    }
}