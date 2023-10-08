clc
clear all
close all

% odpowiednie fragmenty kodu mozna wykonac poprzez zaznaczenie i wcisniecie F9 w Matlabie
% komentowanie/odkomentowywanie: ctrl+r / ctrl+t

%% Zadanie A
%------------------
N = 10;
density = 3; % parametr decydujacy o gestosci polaczen miedzy stronami
[Edges] = generate_network(N, density);
%-----------------
%% Zadanie B

% generacja macierzy I, A, B i wektora b
% macierze A, B i I musza byc przechowywane w formacie sparse (rzadkim)

d = 0.85;
B = sparse(Edges(2,:), Edges(1,:), ones(1, length(Edges)), N, N);

L = sum(B);

A = spdiags(1./L', 0, N, N);
I = speye(N);

M = I - d*B*A;

b = zeros(N, 1) + (1 - d) / N;
%-----------------
%% Zadanie C
r = M\b;
%-----------------
%% Zadanie D
%-----------------
clc
clear all
close all

N = [500, 1000, 3000, 6000, 12000];

d = 0.85;
density = 10;

for i = 1:5
    [Edges] = generate_network(N(i), density);
    B = sparse(Edges(2,:), Edges(1,:), ones(1, length(Edges)), N(i), N(i));
    L = sum(B);
    A = spdiags(1./L', 0, N(i), N(i));
    I = speye(N(i));
    M = I - d*B*A;
    b = zeros(N(i), 1) + (1 - d) / N(i);
    tic
    % obliczenia start
    r = M\b;
    % obliczenia stop
    czas_Gauss(i) = toc;
end

plot(N, czas_Gauss)
xlabel("Ilość stron (N)")
ylabel("Czas [s]")
title(["Zależność czasu obliczeń od wartości N", "dla metody bezpośredniej"])
print -dpng zadanieD
%-----------------
%% Zadanie E
clc
clear all
close all

N = [500, 1000, 3000, 6000, 12000];

d = 0.85;
density = 10;

for i = 1:5
    [Edges] = generate_network(N(i), density);
    B = sparse(Edges(2,:), Edges(1,:), ones(1, length(Edges)), N(i), N(i));
    L = sum(B);
    A = spdiags(1./L', 0, N(i), N(i));
    I = speye(N(i));
    M = I - d*B*A;
    b = zeros(N(i), 1) + (1 - d) / N(i);
    k(i) = 1;
    r = ones(N(i), 1);
    L = tril(M,-1);
    U = triu(M,1);
    D = diag(diag(M));
    part1 = -D\(L+U);
    part2 = D\b;
    tic
    % obliczenia start
    while 1
        r = part1*r + part2;
        res = M*r-b;
        normRES(k(i), i) = norm(res);
        if normRES(k(i), i) < 10^-14
            break;
        end
        k(i) = k(i) + 1;
    end
    % obliczenia stop
    czas_Jacobi(i) = toc;
end
plot(N, czas_Jacobi)
xlabel("Ilość stron (N)")
ylabel("Czas [s]")
title(["Zależność czasu obliczeń od wartości N", "dla metody Jacobiego"])
print -dpng zadanieE_czas

plot(N, k)
xlabel("Ilość stron (N)")
ylabel("Liczba iteracji")
title(["Liczba iteracji wymagana do osiągnięcia","rozwiązania dla metody Jacobiego"])
print -dpng zadanieE_iteracje

semilogy(1:k(2), normRES(1:k(2),2))
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title(["Wartość normy błędu rezydualnego od iteracji","dla N=1000 dla metody Jacobiego"])
print -dpng zadanieE_norma
%------------------
%% Zadanie F
clc
clear all
close all

N = [500, 1000, 3000, 6000, 12000];

d = 0.85;
density = 10;

for i = 1:5
    [Edges] = generate_network(N(i), density);
    B = sparse(Edges(2,:), Edges(1,:), ones(1, length(Edges)), N(i), N(i));
    L = sum(B);
    A = spdiags(1./L', 0, N(i), N(i));
    I = speye(N(i));
    M = I - d*B*A;
    b = zeros(N(i), 1) + (1 - d) / N(i);
    k(i) = 1;
    r = ones(N(i), 1);
    L = tril(M,-1);
    U = triu(M,1);
    D = diag(diag(M));
    part1 = -(D+L);
    part2 = (D+L)\b;
    tic
    % obliczenia start
    while 1
        r = part1\(U*r) + part2;
        res = M*r-b;
        normRES(k(i), i) = norm(res);
        if normRES(k(i), i) < 10^-14
            break;
        end
        k(i) = k(i) + 1;
    end
    % obliczenia stop
    czas_GaussSeidl(i) = toc;
end
plot(N, czas_GaussSeidl)
xlabel("Ilość stron (N)")
ylabel("Czas [s]")
title(["Zależność czasu obliczeń od wartości N", "dla metody Gaussa-Seidla"])
print -dpng zadanieF_czas

plot(N, k)
xlabel("Ilość stron (N)")
ylabel("Liczba iteracji")
title(["Liczba iteracji wymagana do osiągnięcia", "rozwiązania dla metody Gaussa-Seidla"])
print -dpng zadanieF_iteracje

semilogy(1:k(2), normRES(1:k(2),2))
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title(["Wartość normy błędu rezydualnego od iteracji", "dla N=1000 dla metody Gaussa-Seidla"])
print -dpng zadanieF_norma
%------------------
%% Zadanie G
clc
clear all
close all
load('Dane_Filtr_Dielektryczny_lab3_MN.mat')

tic
r = M\b;
disp(['Metoda bezpośrednia: ', num2str(toc), 's'])

clc
clear all
close all
load('Dane_Filtr_Dielektryczny_lab3_MN.mat')

L = tril(M,-1);
U = triu(M,1);
D = diag(diag(M));
part1 = -D\(L+U);
part2 = D\b;
r = ones(length(b), 1);
tic
while 1
    r = part1*r + part2;
    res = M*r-b;
    if norm(res) < 10^-14
        break;
    end
end
disp(['Metoda Jacobiego: ', num2str(toc), 's'])

clc
clear all
close all
load('Dane_Filtr_Dielektryczny_lab3_MN.mat')

L = tril(M,-1);
U = triu(M,1);
D = diag(diag(M));
part1 = -(D+L);
part2 = (D+L)\b;
r = ones(length(b), 1);
tic
while 1
    r = part1\(U*r) + part2;
    res = M*r-b;
    if norm(res) < 10^-14
        break;
    end
end
disp(['Metoda Gaussa-Seidla: ', num2str(toc), 's'])
%------------------