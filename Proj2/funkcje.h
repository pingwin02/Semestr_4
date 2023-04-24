#ifndef FUNKCJE_H
#define FUNKCJE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define N 997
#define F 8
#define E 5

struct LUD {
	double** L;
	double** U;
	double** D;
} typedef LUD;

struct Wynik {
	double* x;
	double* resHist;
	int iteracje;
	double czas;
} typedef Wynik;

struct Zadanie {
	double** A;
	double* b;
	int n;
	Wynik wynik;
} typedef Zadanie;

void wypiszMacierz(double** M, int n);
void wypiszWektor(double* v, int n);
void wypiszZadanie(Zadanie zad);

double** zbudujMacierz(int n);
double* zbudujWektor(int n);

double* kopiujWektor(double* v, int n);

void zwolnijWektor(double* v);
void zwolnijMacierz(double** A, int n);
void zwolnijLUD(LUD lud, int n);
void zwolnijZadanie(Zadanie zad);

double** zbudujA(double a, double b, double c, int n);
double* zbudujB(int n);

LUD wygenerujLUD(double** M, int n);
double* forwardSubstitution(double** L, double* y, int n);
double* backwardSubstitution(double** U, double* y, int n);

double norma(double* v, int n);

double** sumaMacierzy(double** A, double** B, int n);
double** roznicaMacierzy(double** A, double** B, int n);

double* iloczynMacierzWektor(double** A, double* v, int n);

double* sumaWektorow(double* v1, double* v2, int n);
double* roznicaWektorow(double* v1, double* v2, int n);

double* iloczynMacierzWektor(double** A, double* v, int n);
double** neg(double** A, int n);

#endif
