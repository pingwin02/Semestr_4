#define _WINSOCK_DEPRECATED_NO_WARNINGS
#pragma comment(lib, "Ws2_32.lib")

#include <stdio.h>
#include <WinSock2.h>

int main(int argc, char* argv[])
{
	SOCKET s;
	struct sockaddr_in sa;
	WSADATA wsas;
	WORD wersja;
	wersja = MAKEWORD(2, 0);
	WSAStartup(wersja, &wsas);
	s = socket(AF_INET, SOCK_STREAM, 0);
	memset((void*)(&sa), 0, sizeof(sa));
	sa.sin_family = AF_INET;
	sa.sin_port = htons(10000);
	sa.sin_addr.s_addr = inet_addr("127.0.0.1");

	int result;
	result = connect(s, (struct sockaddr FAR*) & sa, sizeof(sa));
	if (result == SOCKET_ERROR)
	{
		printf("\nBlad polaczenia!");
		return;
	}

	int dlug;
	char buf[80];
	for (;;)
	{
		fgets(buf, 80, stdin);
		dlug = strlen(buf); buf[dlug - 1] = '\0';
		send(s, buf, dlug, 0);
		if (strcmp(buf, " KONIEC ") == 0) break;

		dlug = recv(s, buf, 80, 0);
		buf[dlug] = '\0';
		printf("Otrzymano: %s\n", buf);

	}
	closesocket(s);
	WSACleanup();


	return 0;
}