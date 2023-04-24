#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#ifdef _DEBUG
#define DEBUG_NEW new(_NORMAL_BLOCK, __FILE__, __LINE__)
#define new DEBUG_NEW
#endif

#include "funkcje.h"


Zadanie Jacobi(Zadanie zad) {
	int n = zad.n;
	int maxIter = zad.maxIter;
	double eps = zad.eps;
	LUD lud = wygenerujLUD(zad.A, n);
	//czesc1 = L+U
	double** czesc1 = sumaMacierzy(lud.L, lud.U, n);
	//czesc2 = D^-1b
	double* czesc2 = forwardSubstitution(lud.D, zad.b, n);
	//negD = -D
	double** negD = neg(lud.D, n);

	double* x = zbudujWektor(n);

	zad.wynik.resHist = zbudujWektor(maxIter);
	zad.wynik.iteracje = 0;
	double czasStartu = clock();
	//x' = -D^-1(L+U)x + D^-1b
	for (int i = 0; i < maxIter; i++) {
		zad.wynik.iteracje++;
		//ilo1 = (L+U)x
		double* ilo1 = iloczynMacierzWektor(czesc1, x, n);
		//frwSub = -D^-1(ilo1)
		double* frwSub = forwardSubstitution(negD, ilo1, n);
		//nowyX = frwSub + D^-1b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(zad.A, nowyX, n);
		//y = ilo2 - b
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

Zadanie GaussSiedl(Zadanie zad) {
	int n = zad.n;
	int maxIter = zad.maxIter;
	double eps = zad.eps;
	LUD lud = wygenerujLUD(zad.A, n);
	//czesc1 = D+L
	double** czesc1 = sumaMacierzy(lud.D, lud.L, n);
	//czesc2 = (D+L)^-1*b
	double* czesc2 = forwardSubstitution(czesc1, zad.b, n);
	//negsum(D+L) = -(D+L)
	double** negDL = neg(czesc1, n);

	double* x = zbudujWektor(n);

	zad.wynik.resHist = zbudujWektor(maxIter);
	zad.wynik.iteracje = 0;
	double czasStartu = clock();
	//x' = -(D+L)^-1*(Ux) + (D+L)^-1*b
	for (int i = 0; i < maxIter; i++) {
		zad.wynik.iteracje++;
		//ilo1 = Ux
		double* ilo1 = iloczynMacierzWektor(lud.U, x, n);
		//frwSub = -(D+L)^-1*(Ux)
		double* frwSub = forwardSubstitution(negDL, ilo1, n);
		//nowyX = frwSub + (D+L)^-1*b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(zad.A, nowyX, n);
		//y = ilo2 - b
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
	zwolnijMacierz(negDL, n);

	return zad;
}

Zadanie stworzZadanieA() {
	Zadanie zadA;
	zadA.A = zbudujA(5 + E, -1, -1, N);
	zadA.b = zbudujB(N);
	zadA.n = N;
	zadA.eps = 1e-9;
	zadA.maxIter = 1000;
	return zadA;
}

Zadanie stworzZadanieC() {
	Zadanie zadC;
	zadC.A = zbudujA(3, -1, -1, N);
	zadC.b = zbudujB(N);
	zadC.n = N;
	zadC.eps = 1e-9;
	zadC.maxIter = 1000;

	return zadC;
}

void zadanieB() {

	start(stworzZadanieA(), Jacobi);
	start(stworzZadanieA(), GaussSiedl);

}

void zadanieC() {

	start(stworzZadanieC(), Jacobi);
	start(stworzZadanieC(), GaussSiedl);

}

int main() {
	_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
	srand(time(NULL));
	zadanieB();
	zadanieC();
	return 0;
}