#include <windows.h>
#include <stdio.h>
#include <conio.h>

void gotoxy(int x, int y)
{
	COORD c;
	c.X = x - 1;
	c.Y = y - 1;
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), c);
}

//--------------------------------------------------------------------------
#pragma argsused
struct dane_dla_watku // tablica zawiera dane , ktore otrzymaja watki
{
	char nazwa[50];
	int parametr;
} dane[5] = { { "[1]" , 3 }, { "[2]" , 6 }, { "[3]" , 9 }, {"[4]", 12}, {"[5]", 15}};
// priorytety watkow
int priorytety[5] = { THREAD_PRIORITY_BELOW_NORMAL ,
THREAD_PRIORITY_NORMAL , THREAD_PRIORITY_ABOVE_NORMAL, THREAD_PRIORITY_HIGHEST, THREAD_PRIORITY_TIME_CRITICAL };
HANDLE watki[5]; // dojscia ( uchwyty ) watkow
// deklaracja funkcji watku
DWORD WINAPI funkcja_watku(void* argumenty);
//--------------------------------------------------------------------------
int main(int argc, char** argv)
{
	int i;
	DWORD id; // identyfikator watku
	system("cls");
	printf(" Uruchomienie programu \n");
	// tworzenie watkow
	for (i = 0; i < 5; i++)
	{
		watki[i] = CreateThread(
			0, // atrybuty bezpieczenstwa
			0, // inicjalna wielkosc stosu
			funkcja_watku, // funkcja watku
			(void*)&dane[i],// dane dla funkcji watku
			0, // flagi utworzenia
			&id);
		if (watki[i] != INVALID_HANDLE_VALUE)
		{
			Sleep(50);
			printf(" Utworzylem watek %s o id %x\n", dane[i].nazwa, id);
			// ustawienie priorytetu
			SetThreadPriority(watki[i], priorytety[i]);
		}
	}
	Sleep(3000); // uspienie watku glownego na 10 s
	// zaoñczenie w¹tku 2
	TerminateThread(watki[1], 0);

	Sleep(10000); // uspienie watku glownego na 20 s
	return 0;
}
//--------------------------------------------------------------------------
// trzy takie funkcje pracuja wspolbieznie w programie
DWORD WINAPI funkcja_watku(void* argumenty)
{
	unsigned int licznik = 0;
	// rzutowanie struktury na wlasny wskaznik
	struct dane_dla_watku* moje_dane = (struct dane_dla_watku*)argumenty;
	// wyswietlenie informacji o uruchomieniu
	gotoxy(1, moje_dane->parametr);
	printf("% s", moje_dane->nazwa);
	Sleep(1000);
	// praca , watki sa terminowane przez zakonczenie programu
// -funkcji main
	while (1)
	{
		gotoxy(licznik++ / 5000 + 5, moje_dane->parametr);
		printf(".");
	}
	return 0;
}