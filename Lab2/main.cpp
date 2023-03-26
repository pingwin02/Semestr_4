#include <iostream>

using namespace std;

//Generator liniowy x(n+1) = (a*x(n) + c) mod m

void linear_generator(double a, double c, double M, int count) {
	double x = 1;
	for (int i = 0; i < count; i++) {
		x = fmod(a*x + c, M);
		cout << x/M << endl;
	}
}

void rol(bool tab[], int amount) {

	for (int i = 0; i < amount; i++) {
		bool temp = tab[0];
		for (int j = 0; j < 31; j++) {
			tab[j] = tab[j + 1];
		}
		tab[31] = temp;
	}

}

void disp(bool tab[]) {
	double x = 0;
	for (int i = 0; i < 32; i++) {
		x += tab[i] * pow(2, -i - 1);
	}

	cout << x << endl;
}

//Generator oparty na rejestrach przesuwnych bi=bi-p xor bi-q

void shift_register_generator(int p, int q, int count) {
	bool bytes[32] = { 1,0,1,0,1,1 };
	for (int k = 0; k < count; k++) {
		
		for (int i = p; i < 32; i++) {
			bytes[i] = bytes[i - p] ^ bytes[i - q];
		}
		disp(bytes);
		rol(bytes, 32-p);
	}
}

//Generator nieliniowy

void nonlinear_generator(double a, double c, double M, int count) {
	double x = 1;
	for (int i = 0; i < count; i++) {
		x = fmod(a * pow(x, -1) + c, M);
		cout << x / M << endl;
	}
}


int main() {

	double a = pow(2, 2) * pow(23, 7) + 1;
	double c = 0;
	double M = pow(2, 35);

	linear_generator(a, c, M, 10);

	cout << endl;

	int p = 10;
	int q = 3;

	shift_register_generator(p, q, 10);

	cout << endl;

	nonlinear_generator(a, c, M, 10);

	return 0;
}