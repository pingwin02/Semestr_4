#define _CRT_SECURE_NO_WARNINGS
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif

#include <time.h>
#include "funkcje.h"


Zadanie Jacobi(Zadanie zad, double eps, int maxIter) {
	int n = zad.n;
	LUD lud = wygenerujLUD(zad.A, n);
	double** czesc1 = sumaMacierzy(lud.L, lud.U, n);
	double* czesc2 = forwardSubstitution(lud.D, zad.b, n);
	double* x = zbudujWektor(n);
	double** negD = neg(lud.D, n);

	zad.wynik.resHist = zbudujWektor(maxIter);
	zad.wynik.iteracje = 0;
	double czasStartu = clock();
	for (int i = 0; i < maxIter; i++) {
		zad.wynik.iteracje++;
		double* ilo1 = iloczynMacierzWektor(czesc1, x, n);
		double* frwSub = forwardSubstitution(negD, ilo1, n);
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		double* ilo2 = iloczynMacierzWektor(zad.A, nowyX, n);
		double* y = roznicaWektorow(ilo2, zad.b, n);
		zad.wynik.resHist[i] = norma(y, n);
		zwolnijWektor(x);
		zwolnijWektor(ilo1);
		zwolnijWektor(frwSub);
		zwolnijWektor(ilo2);
		zwolnijWektor(y);
		x = nowyX;
		if (zad.wynik.resHist[i] < eps) {
			break;
		}
	}

	zad.wynik.x = x;
	zwolnijMacierz(czesc1, n);
	zwolnijWektor(czesc2);
	zwolnijLUD(lud, n);
	zwolnijMacierz(negD, n);

	return zad;
}

Zadanie zadanieA() {
	Zadanie zadA;
	double** A = zbudujA(5 + E, -1, -1, N);
	double* b = zbudujB(N);

	zadA.A = A;
	zadA.b = b;
	zadA.n = N;

	return zadA;
}

void zadanieB() {

	double czasStartu = clock();
	Zadanie zadanieB1 = Jacobi(zadanieA(), 1e-9, 100);
	zadanieB1.wynik.czas = (clock() - czasStartu) / CLOCKS_PER_SEC;
	wypiszZadanie(zadanieB1);
	zwolnijZadanie(zadanieB1);

}

int main() {
	_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
	srand(time(NULL));
	zadanieB();
	return 0;
}