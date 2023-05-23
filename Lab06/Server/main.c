#pragma comment(lib, "Ws2_32.lib")
#include <WinSock2.h>
#include <stdio.h>

int main()
{
    WSADATA wsas;
    int result;
    WORD wersja;
    wersja = MAKEWORD(1, 1);
    result = WSAStartup(wersja, &wsas);
    SOCKET s;
    s = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in sa;
    memset((void*)(&sa), 0, sizeof(sa));
    sa.sin_family = AF_INET;
    sa.sin_port = htons(10000);
    sa.sin_addr.s_addr = htonl(INADDR_ANY);

    result = bind(s, (struct sockaddr FAR*) & sa, sizeof(sa));

    result = listen(s, 5);

    struct sockaddr_in sc;
    int lenc;
    for (;;)
    {
        lenc = sizeof(sc);
        SOCKET si;
        si = accept(s, (struct sockaddr FAR*) & sc, &lenc);
        char buf[80];
        while (recv(si, buf, 80, 0))
        {
            if (strcmp(buf, " KONIEC ") == 0)
            {
                closesocket(si);
                WSACleanup();
                return;
            }
            printf("\n %s", buf);

            for (int i = 0; i < strlen(buf); i++)
            {
                if (buf[i] >= 'a' && buf[i] <= 'z')
                {
                    buf[i] = buf[i] - 32;
                }
            }
            send(si, buf, strlen(buf), 0);
        }
    }
}