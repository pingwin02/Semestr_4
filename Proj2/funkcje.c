#include "funkcje.h"

void wypiszMacierz(double** M, int n) {

	printf("Macierz %d x %d:\n", n, n);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			printf("%e ", M[i][j]);
		}
		printf("\n");
	}
}

void wypiszWektor(double* v, int n) {

	printf("Wektor %d x 1:\n", n);
	for (int i = 0; i < n; i++) {
		printf("%e ", v[i]);
		if (i > 5) {
			printf("...");
			break;
		}
	}
	printf("\n");
}

void wypiszZadanie(Zadanie zad) {
	static int i = 1;
	printf("\nZadanie %d:\n", i);
	printf("\nWektor rozwiazania x:\n");
	wypiszWektor(zad.wynik.x, N);
	printf("\nResiduum:\n");
	wypiszWektor(zad.wynik.resHist, zad.wynik.iteracje);
	printf("\nCzas: %fs ", zad.wynik.czas);
	printf("Iteracje: %d\n\n", zad.wynik.iteracje);
	zapiszWynik(zad.wynik, i);
	i++;
}

double** zbudujMacierz(int n) {
	double** M = (double**)malloc(n * sizeof(double*));
	for (int i = 0; i < n; i++) {
		if (M != NULL) {
			M[i] = zbudujWektor(n);
		}
	}
	return M;
}

double* zbudujWektor(int n) {
	double* W = (double*)malloc(n * sizeof(double));
	for (int i = 0; i < n; i++) {
		if (W != NULL) {
			W[i] = 0;
		}
	}
	return W;
}

void zwolnijWektor(double* v) {
	free(v);
}

void zwolnijMacierz(double** A, int n) {
	for (int i = 0; i < n; i++) {
		zwolnijWektor(A[i]);
	}
	free(A);
}

void zwolnijLUD(LUD lud, int n) {
	zwolnijMacierz(lud.L, n);
	zwolnijMacierz(lud.U, n);
	zwolnijMacierz(lud.D, n);
}

void zwolnijZadanie(Zadanie zad) {
	zwolnijWektor(zad.wynik.x);
	zwolnijWektor(zad.wynik.resHist);
	zwolnijMacierz(zad.A, zad.n);
	zwolnijWektor(zad.b);
}

double** zbudujA(double a1, double a2, double a3, int n) {

	double** A = zbudujMacierz(n);

	for (int i = 0; i < n; i++) {
		A[i][i] = a1;
		if (i > 0) {
			A[i][i - 1] = a2;
		}
		if (i < n - 1) {
			A[i][i + 1] = a3;
		}
		if (i > 1) {
			A[i][i - 2] = a2;
		}
		if (i < n - 2) {
			A[i][i + 2] = a3;
		}
	}

	return A;
}

double* zbudujB(int n) {
	double* B = zbudujWektor(n);
	for (int i = 0; i < n; i++) {
		B[i] = sin((double)i * (F + 1));
	}
	return B;
}

void start(Zadanie zad, Zadanie (metoda)(Zadanie), int nr) {
	double czasStartu = clock();
	Zadanie zadanie = metoda(zad);
	zadanie.wynik.czas = (clock() - czasStartu) / CLOCKS_PER_SEC;
	if (nr == 0) {
		wypiszZadanie(zadanie);
	}
	else {
		zapiszCzas(zadanie, nr);
	}
	zwolnijZadanie(zadanie);
}

LUD wygenerujLUD(double** M, int n) {
	LUD lud;

	lud.L = zbudujMacierz(n);
	lud.U = zbudujMacierz(n);
	lud.D = zbudujMacierz(n);

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (i == j) {
				lud.D[i][j] = M[i][j];
			}
			if (i > j) {
				lud.L[i][j] = M[i][j];
			}
			if (i < j) {
				lud.U[i][j] = M[i][j];
			}
		}
	}

	return lud;
}

double* forwardSubstitution(double** L, double* y, int n) {
	double* x = zbudujWektor(n);

	for (int i = 0; i < n; i++) {
		x[i] = y[i];
		for (int j = 0; j < i; j++) {
			x[i] -= L[i][j] * x[j];
		}
		x[i] /= L[i][i];
	}

	return x;
}

double* backwardSubstitution(double** U, double* y, int n) {
	double* x = zbudujWektor(n);

	for (int i = n - 1; i >= 0; i--) {
		x[i] = y[i];
		for (int j = i + 1; j < n; j++) {
			x[i] -= U[i][j] * x[j];
		}
		x[i] /= U[i][i];
	}
	return x;
}

void zapiszWynik(Wynik wynik, int nr) {
	FILE* plik;
	char nazwa[20];
	sprintf(nazwa, "wynik%d.csv", nr);
	plik = fopen(nazwa, "w");

	if (plik != NULL) {
		for (int i = 0; i < wynik.iteracje; i++) {
			fprintf(plik, "%e\n", wynik.resHist[i]);
		}

		fclose(plik);
	}
}

void zapiszCzas(Zadanie zad, int nr) {
	FILE* plik;
	char nazwa[20];
	sprintf(nazwa, "wynikCzas%d.csv", nr);
	plik = fopen(nazwa, "a");

	if (plik != NULL) {
		fprintf(plik, "%d, %e\n", zad.n, zad.wynik.czas);
		fclose(plik);
	}
}

double norma(double* v, int n) {
	double suma = 0;
	for (int i = 0; i < n; i++) {
		suma += v[i] * v[i];
	}
	return sqrt(suma);
}

double** sumaMacierzy(double** A, double** B, int n) {
	double** C = zbudujMacierz(n);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			C[i][j] = A[i][j] + B[i][j];
		}
	}
	return C;
}

double** roznicaMacierzy(double** A, double** B, int n) {
	double** C = zbudujMacierz(n);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			C[i][j] = A[i][j] - B[i][j];
		}
	}
	return C;
}

double* sumaWektorow(double* v, double* w, int n) {
	double* m = zbudujWektor(n);
	for (int i = 0; i < n; i++) {
		m[i] = v[i] + w[i];
	}
	return m;
}

double* roznicaWektorow(double* v, double* w, int n) {
	double* m = zbudujWektor(n);
	for (int i = 0; i < n; i++) {
		m[i] = v[i] - w[i];
	}
	return m;
}

double* iloczynMacierzWektor(double** A, double* v, int n) {
	double* w = zbudujWektor(n);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			w[i] += A[i][j] * v[j];
		}
	}
	return w;
}

double** neg(double** A, int n) {
	double** B = zbudujMacierz(n);
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			B[i][j] = -A[i][j];
		}
	}
	return B;
}