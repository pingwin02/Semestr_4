#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif

#include "funkcje.h"


void Jacobi(Zadanie* zad) {
	int n = zad->n;
	int maxIter = zad->maxIter;
	double eps = zad->eps;
	LUD lud = wygenerujLUD(zad->A, n);
	//czesc1 = L+U
	double** czesc1 = sumaMacierzy(lud.L, lud.U, n);
	//czesc2 = D^-1b
	double* czesc2 = forwardSubstitution(lud.D, zad->b, n);
	//negD = -D
	double** negD = neg(lud.D, n);

	double* x = zbudujWektor(n);

	zad->wynik.resHist = zbudujWektor(maxIter);
	zad->wynik.iteracje = 0;

	zad->wynik.czas = clock();

	//x' = -D^-1(L+U)x + D^-1b
	for (int i = 0; i < maxIter; i++) {
		zad->wynik.iteracje++;
		//ilo1 = (L+U)x
		double* ilo1 = iloczynMacierzWektor(czesc1, x, n);
		//frwSub = -D^-1(ilo1)
		double* frwSub = forwardSubstitution(negD, ilo1, n);
		//nowyX = frwSub + D^-1b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(zad->A, nowyX, n);
		//y = ilo2 - b
		double* y = roznicaWektorow(ilo2, zad->b, n);
		zad->wynik.resHist[i] = norma(y, n);
		zwolnijWektor(x);
		zwolnijWektor(ilo1);
		zwolnijWektor(frwSub);
		zwolnijWektor(ilo2);
		zwolnijWektor(y);
		x = nowyX;
		if (zad->wynik.resHist[i] < eps) {
			break;
		}
	}

	zad->wynik.czas = wyznaczCzas(zad->wynik.czas);

	zad->wynik.x = x;
	zwolnijMacierz(czesc1, n);
	zwolnijWektor(czesc2);
	zwolnijLUD(lud, n);
	zwolnijMacierz(negD, n);
}

void GaussSiedl(Zadanie* zad) {
	int n = zad->n;
	int maxIter = zad->maxIter;
	double eps = zad->eps;
	LUD lud = wygenerujLUD(zad->A, n);
	//czesc1 = D+L
	double** czesc1 = sumaMacierzy(lud.D, lud.L, n);
	//czesc2 = (D+L)^-1*b
	double* czesc2 = forwardSubstitution(czesc1, zad->b, n);
	//negsum(D+L) = -(D+L)
	double** negDL = neg(czesc1, n);

	double* x = zbudujWektor(n);

	zad->wynik.resHist = zbudujWektor(maxIter);
	zad->wynik.iteracje = 0;

	zad->wynik.czas = clock();

	//x' = -(D+L)^-1*(Ux) + (D+L)^-1*b
	for (int i = 0; i < maxIter; i++) {
		zad->wynik.iteracje++;
		//ilo1 = Ux
		double* ilo1 = iloczynMacierzWektor(lud.U, x, n);
		//frwSub = -(D+L)^-1*(Ux)
		double* frwSub = forwardSubstitution(negDL, ilo1, n);
		//nowyX = frwSub + (D+L)^-1*b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(zad->A, nowyX, n);
		//y = ilo2 - b
		double* y = roznicaWektorow(ilo2, zad->b, n);
		zad->wynik.resHist[i] = norma(y, n);
		zwolnijWektor(x);
		zwolnijWektor(ilo1);
		zwolnijWektor(frwSub);
		zwolnijWektor(ilo2);
		zwolnijWektor(y);
		x = nowyX;
		if (zad->wynik.resHist[i] < eps) {
			break;
		}
	}

	zad->wynik.czas = wyznaczCzas(zad->wynik.czas);

	zad->wynik.x = x;
	zwolnijMacierz(czesc1, n);
	zwolnijWektor(czesc2);
	zwolnijLUD(lud, n);
	zwolnijMacierz(negDL, n);

}

void faktoryzacjaLU(Zadanie* zad) {
	int n = zad->n;
	double eps = zad->eps;

	double** L = zbudujMacierzJednostkowa(n);
	double** U = kopiujMacierz(zad->A, zad->n);

	zad->wynik.czas = clock();

	for (int k = 0; k < n - 1; k++) {
		for (int j = k + 1; j < n; j++) {
			L[j][k] = U[j][k] / U[k][k];
			for (int i = k; i < n; i++) {
				U[j][i] = U[j][i] - L[j][k] * U[k][i];
			}
		}
	}

	double* y = forwardSubstitution(L, zad->b, n);
	double* x = backwardSubstitution(U, y, n);

	zad->wynik.resHist = zbudujWektor(1);
	zad->wynik.iteracje = 1;
	zad->wynik.czas = wyznaczCzas(zad->wynik.czas);

	zad->wynik.x = x;

	zwolnijMacierz(L, n);
	zwolnijMacierz(U, n);
	zwolnijWektor(y);
	
}

Zadanie stworzZadanieA(int n) {
	Zadanie zadA;
	zadA.A = zbudujA(5 + E, -1, -1, n);
	zadA.b = zbudujB(n);
	zadA.n = n,
	zadA.eps = 1e-9;
	zadA.maxIter = 1000;
	zadA.litera = 'A';
	return zadA;
}

Zadanie stworzZadanieC(int n) {
	Zadanie zadC;
	zadC.A = zbudujA(3, -1, -1, n);
	zadC.b = zbudujB(n);
	zadC.n = n;
	zadC.eps = 1e-9;
	zadC.maxIter = 1000;
	zadC.litera = 'C';

	return zadC;
}

void zadanieB() {

	start(stworzZadanieA(N), Jacobi, 0);
	start(stworzZadanieA(N), GaussSiedl, 0);

}

void zadanieC() {

	start(stworzZadanieC(N), Jacobi, 0);
	start(stworzZadanieC(N), GaussSiedl, 0);

}

void zadanieD() {
	start(stworzZadanieC(N), faktoryzacjaLU, 0);
}

void zadanieE() {
	int n[] = {100, 500, 1000, 2000, 3000, 5000, 10000};

	for (int i = 0; i < 7; i++) {
		start(stworzZadanieA(n[i]), Jacobi, 1);
		start(stworzZadanieA(n[i]), GaussSiedl, 2);
	}

}

int main() {
	_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
	srand(time(NULL));
	system("del *.csv");
	zadanieB();
	zadanieC();
	zadanieD();
	zadanieE();
	return 0;
}