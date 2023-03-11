%% SPRAWOZDANIE LABORATORIUM 2
% Damian Jankowski s188597

%% Zadanie 2. PageRank

%% Przygotowanie środowiska
% Zamknięcie okien i usunięcie zmiennych
clear all
close all

%% Zadanie A
% Zdefiniowanie tablicy |Edges| dla sieci złożonej z siedmiu stron.
% Zmienna $N$ określa ilość wszystkich stron sieci

Edges = [ 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 7;
          4, 6, 3, 4, 5, 5, 6, 7, 5, 6, 4, 6, 4, 7, 6];

N = 7;
%% Zadanie B
% Skonstruowanie macierzy $B$, $A$, $I$, $M$ oraz wektora $\vec{b}$ dla 
% połączeń wygenerowanych w *Zadaniu A* oraz dla parametru $d = 0.85$.
% Wektor $L$ stanowi sumę elementów kolejnych kolumn macierzy $B$

d = 0.85;
B = sparse(Edges(2,:), Edges(1,:), ones(1, 15), N, N);

L = zeros(N,1);
for i = 1:N
    L(i) = sum(B(:,i));
end

A = spdiags(1./L, 0, N, N);
I = speye(N);

M = I - d*B*A;

b = zeros(N, 1) + (1 - d) / N;

%% Zadanie C
% Wykonanie polecenia |whos| i zapisanie wyniku do pliku |sparse_test.txt|

if (exist("sparse_test.txt","file"))
    delete("sparse_test.txt");
end

diary sparse_test.txt
whos A B I M b
diary off

%% Zadanie D
% Wykonanie polecenia |spy| i wygenerowanie wykresu do pliku |.png|

spy(B)
title("Niezerowe elementy macierzy B")
print -dpng spy_b

%% Zadanie E
% Rozwiązanie układu równań $Mr = b$ 

r = M\b;

%% Zadanie F
% Wygenerowanie wykresu słupkowego dla wektora $r$

bar(r)
title("Wartość PageRank dla poszczególnych stron")
ylabel("PageRank")
xlabel("nr strony")
print -dpng bar