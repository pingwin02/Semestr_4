#include "metody.h"

void Jacobi(Zadanie* zad) {
	int n = zad->n;
	int maxIter = zad->maxIter;
	double eps = zad->eps;

	double** A = zad->A;
	double* b = zad->b;

	LUD lud = wygenerujLUD(zad->A, n);
	//czesc1 = L+U
	double** czesc1 = sumaMacierzy(lud.L, lud.U, n);
	//czesc2 = D^-1b
	double* czesc2 = forwardSubstitution(lud.D, zad->b, n);
	//negD = -D
	double** negD = neg(lud.D, n);

	double* x = zbudujWektor(n);

	double* resHist = zbudujWektor(maxIter);
	int iteracje = 0;
	double czas = clock();

	//x' = -D^-1(L+U)x + D^-1b
	for (int i = 0; i < maxIter; i++) {
		iteracje++;
		//ilo1 = (L+U)x
		double* ilo1 = iloczynMacierzWektor(czesc1, x, n);
		//frwSub = -D^-1(ilo1)
		double* frwSub = forwardSubstitution(negD, ilo1, n);
		//nowyX = frwSub + D^-1b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(A, nowyX, n);
		//y = ilo2 - b
		double* y = roznicaWektorow(ilo2, b, n);
		resHist[i] = norma(y, n);
		zwolnijWektor(x);
		zwolnijWektor(ilo1);
		zwolnijWektor(frwSub);
		zwolnijWektor(ilo2);
		zwolnijWektor(y);
		x = nowyX;
		if (resHist[i] < eps || resHist[i] == INFINITY) {
			break;
		}
	}

	zad->wynik.czas = wyznaczCzas(czas);
	zad->wynik.x = x;
	zad->wynik.resHist = resHist;
	zad->wynik.iteracje = iteracje;

	zwolnijMacierz(czesc1, n);
	zwolnijWektor(czesc2);
	zwolnijLUD(lud, n);
	zwolnijMacierz(negD, n);
}

void GaussSeidel(Zadanie* zad) {
	int n = zad->n;
	int maxIter = zad->maxIter;
	double eps = zad->eps;

	double** A = zad->A;
	double* b = zad->b;

	LUD lud = wygenerujLUD(zad->A, n);
	//czesc1 = D+L
	double** czesc1 = sumaMacierzy(lud.D, lud.L, n);
	//czesc2 = (D+L)^-1*b
	double* czesc2 = forwardSubstitution(czesc1, b, n);
	//negsum(D+L) = -(D+L)
	double** negDL = neg(czesc1, n);

	double* x = zbudujWektor(n);

	double* resHist = zbudujWektor(maxIter);
	int iteracje = 0;
	double czas = clock();

	//x' = -(D+L)^-1*(Ux) + (D+L)^-1*b
	for (int i = 0; i < maxIter; i++) {
		iteracje++;
		//ilo1 = Ux
		double* ilo1 = iloczynMacierzWektor(lud.U, x, n);
		//frwSub = -(D+L)^-1*(Ux)
		double* frwSub = forwardSubstitution(negDL, ilo1, n);
		//nowyX = frwSub + (D+L)^-1*b
		double* nowyX = sumaWektorow(frwSub, czesc2, n);
		//ilo2 = Ax
		double* ilo2 = iloczynMacierzWektor(A, nowyX, n);
		//y = ilo2 - b
		double* y = roznicaWektorow(ilo2, b, n);
		resHist[i] = norma(y, n);
		zwolnijWektor(x);
		zwolnijWektor(ilo1);
		zwolnijWektor(frwSub);
		zwolnijWektor(ilo2);
		zwolnijWektor(y);
		x = nowyX;
		if (resHist[i] < eps || resHist[i] == INFINITY) {
			break;
		}
	}

	zad->wynik.czas = wyznaczCzas(czas);
	zad->wynik.x = x;
	zad->wynik.resHist = resHist;
	zad->wynik.iteracje = iteracje;

	zwolnijMacierz(czesc1, n);
	zwolnijWektor(czesc2);
	zwolnijLUD(lud, n);
	zwolnijMacierz(negDL, n);
}

void faktoryzacjaLU(Zadanie* zad) {
	int n = zad->n;
	double eps = zad->eps;

	double** A = zad->A;
	double* b = zad->b;

	double** L = zbudujMacierzJednostkowa(n);
	double** U = kopiujMacierz(A, zad->n);

	double czas = clock();

	for (int k = 0; k < n - 1; k++) {
		for (int j = k + 1; j < n; j++) {
			L[j][k] = U[j][k] / U[k][k];
			for (int i = k; i < n; i++) {
				U[j][i] = U[j][i] - L[j][k] * U[k][i];
			}
		}
	}

	double* y = forwardSubstitution(L, b, n);
	double* x = backwardSubstitution(U, y, n);
	double* resHist = zbudujWektor(1);

	zad->wynik.czas = wyznaczCzas(czas);
	zad->wynik.x = x;

	double* Ax = iloczynMacierzWektor(A, x, n);
	double* roznica = roznicaWektorow(Ax, b, n);

	resHist[0] = norma(roznica, n);

	zad->wynik.resHist = resHist;
	zad->wynik.iteracje = 1;

	zwolnijMacierz(L, n);
	zwolnijMacierz(U, n);
	zwolnijWektor(Ax);
	zwolnijWektor(roznica);
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

	start(stworzZadanieA(N), Jacobi, "Jacobi");
	start(stworzZadanieA(N), GaussSeidel, "GaussSiedl");

}

void zadanieC() {

	start(stworzZadanieC(N), Jacobi, "Jacobi");
	start(stworzZadanieC(N), GaussSeidel, "GaussSiedl");

}

void zadanieD() {
	start(stworzZadanieC(N), faktoryzacjaLU, "LU");
}

void zadanieE() {
	int n[] = { 100, 500, 1000, 2000, 3000, 5000, 8000, 10000, 12000 };

	for (int i = 0; i < 9; i++) {
		startSeria(stworzZadanieA(n[i]), Jacobi, "Jacobi");
		startSeria(stworzZadanieA(n[i]), GaussSeidel, "GaussSiedl");

		if (n[i] <= 5000)
			startSeria(stworzZadanieA(n[i]), faktoryzacjaLU, "LU");
	}

}