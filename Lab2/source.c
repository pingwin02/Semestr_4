#include <stdio.h>
#include <math.h>

unsigned int function(
	unsigned int, 
	unsigned int, 
	unsigned int);

//Generator liniowy x(n+1) = (a*x(n) + c) mod m

void linear_generator(unsigned int a, unsigned int c, unsigned int M, int count) {
	unsigned long long x = 15;

	unsigned int amount[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

	for (int i = 0; i < count; i++) {

		x = fmod(function(a, x, c), M);

		amount[10 * x / M]++;
	}

	for (int i = 0; i < 10; i++) {
		printf("%d %d\n", i , amount[i]);
	}
}


void rol(int tab[], int amount) {

	for (int i = 0; i < amount; i++) {
		int temp = tab[0];
		for (int j = 0; j < 31; j++) {
			tab[j] = tab[j + 1];
		}
		tab[30] = temp;
	}

}

double convert(int tab[]) {
	double x = 0;
	for (int i = 0; i < 31; i++) {
		x += tab[i] * pow(2, i);
	}

	return x;
}

//Generator oparty na rejestrach przesuwnych bi=bi-p xor bi-q

void shift_register_generator(int p, int q, int count) {
	int bytes[31] = { 1,0,0,1,1,0,1 };

	unsigned int amount[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	for (int k = 0; k < count; k++) {
		for (int i = p; i < 31; i++) {
			bytes[i] = bytes[i - p] ^ bytes[i - q];
		}
		double x = convert(bytes);
		amount[(int)(10 * x / pow(2, 31))]++;
		rol(bytes, 31 - p);
	}

	for (int i = 0; i < 10; i++) {
		printf("%d %d\n", i, amount[i]);
	}
}


int main() {

	unsigned int a = 69069;
	unsigned int c = 1;
	unsigned int M = pow(2, 31);

	linear_generator(a, c, M, 100000);

	int p = 7;
	int q = 3;

	shift_register_generator(p, q, 100000);

	return 0;
}