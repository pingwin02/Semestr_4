#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <pthread.h>

#define KANAL 12345
#define FLAGI 0666

struct msgbuf
{
    long podkanal;
    int wielkosc;
} komunikat;

void usun_semafor()
{
    int kanal = msgget(KANAL, FLAGI);

    if (kanal == -1)
    {
        perror("Błąd uzyskania dostępu do kanału");
        exit(1);
    }

    if (msgctl(kanal, IPC_RMID, NULL) == -1)
    {
        perror("Błąd usuwania semafora");
        exit(1);
    }
}

void semafor_inicjalizuj()
{
    usun_semafor();

    int kanal = msgget(KANAL, IPC_CREAT | FLAGI);
    if (kanal == -1)
    {
        perror("Błąd tworzenia kanału");
        exit(1);
    }

    komunikat.podkanal = 1;
    komunikat.wielkosc = 10;

    if (msgsnd(kanal, (struct msgbuf *)&komunikat, sizeof(komunikat), IPC_NOWAIT) == -1)
    {
        perror("Błąd wysłania semafora");
        exit(1);
    }
}

void semafor_opusc()
{
    int kanal = msgget(KANAL, FLAGI);
    if (kanal == -1)
    {
        perror("Błąd uzyskania dostępu do kanału");
        exit(1);
    }

    if (msgrcv(kanal, (struct msgbuf *)&komunikat, sizeof(komunikat), komunikat.podkanal, 0) == -1)
    {
        perror("Błąd odebrania semafora");
        exit(1);
    }
}

void semafor_podnies()
{
    int kanal = msgget(KANAL, FLAGI);
    if (kanal == -1)
    {
        perror("Błąd uzyskania dostępu do kanału");
        exit(1);
    }

    if (msgsnd(kanal, (struct msgbuf *)&komunikat, sizeof(komunikat), IPC_NOWAIT) == -1)
    {
        perror("Błąd wysłania semafora");
        exit(1);
    }
}

void *producent(void *arg)
{

    int id = *(int *)arg;

    while (1)
    {
        semafor_opusc();
        printf("***Sekcja krytyczna producenta %d***\n\n", id);
        sleep(1);
        printf("Wyprodukowano towar: %d\n\n", ++komunikat.wielkosc);
        semafor_podnies();
        printf("***Koniec sekcji krytycznej producenta %d***\n", id);
    }

    pthread_exit(NULL);
}

void *konsument(void *arg)
{

    int id = *(int *)arg;

    while (1)
    {
        semafor_opusc();
        printf("---Sekcja krytyczna konsumenta %d---\n\n", id);
        sleep(2);
        printf("Skonsumowano towar: %d\n\n", komunikat.wielkosc--);
        semafor_podnies();
        printf("---Koniec sekcji krytycznej konsumenta %d---\n", id);
    }

    pthread_exit(NULL);
}

int main()
{
    semafor_inicjalizuj();

    pthread_t prod1, prod2, kons1, kons2;

    int id1 = 1, id2 = 2;

    pthread_create(&prod1, NULL, producent, (void *)&id1);
    pthread_create(&prod2, NULL, producent, (void *)&id2);
    pthread_create(&kons1, NULL, konsument, (void *)&id1);
    pthread_create(&kons2, NULL, konsument, (void *)&id2);

    pthread_join(prod1, NULL);
    pthread_join(prod2, NULL);
    pthread_join(kons1, NULL);
    pthread_join(kons2, NULL);

    return 0;
}
