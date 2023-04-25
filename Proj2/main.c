#include "funkcje.h"
#include "metody.h"

int main() {
	srand(time(NULL));
	setbuf(stdout, NULL);

	system("del *.csv");

	zadanieB();
	zadanieC();
	zadanieD();
	zadanieE();

	return 0;
}