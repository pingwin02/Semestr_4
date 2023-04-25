#ifndef METODY_H
#define METODY_H

#include "funkcje.h"


void Jacobi(Zadanie* zad);
void GaussSeidel(Zadanie* zad);
void faktoryzacjaLU(Zadanie* zad);

Zadanie stworzZadanieA(int n);
Zadanie stworzZadanieC(int n);

void zadanieB();
void zadanieC();
void zadanieD();
void zadanieE();

#endif
