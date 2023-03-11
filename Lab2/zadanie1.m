%% SPRAWOZDANIE LABORATORIUM 2
% DAMIAN JANKOWSKI s188597

%% Przygotowanie środowiska
% Zamknięcie okien i usunięcie zmiennych
clear all
close all


%% Deklaracja zmiennych

a = 5; % Długość boku kwadratu
r_max = a/2; % Maksymalny promień każdego okręgu
n_max = 200; % Ilość okręgów

% Wektory do składowania informacji o wygenerowanych okręgach
x = zeros(n_max, 1);
y = zeros(n_max, 1);
r = zeros(n_max, 1);
areas = zeros(n_max, 1); % Pole okregów
tries = ones(n_max, 1); % Ilość prób wylosowania

n = 1; % Numer bieżącego okręgu

%% Generowanie okręgów
% Pętla |while| do generowania $n_{max}$ okręgów

while n <= n_max
    % Losowanie wartości $X, Y, R$
    X = rand(1)*a;
    Y = rand(1)*a;
    R = rand(1)*r_max;

    % Sprawdzenie czy okrąg o wylosowanych wartościach zmieści się w
    % kwadracie o boku $a$ 
    if (X - R) > 0 && (X + R) < a && ...
       (Y - R) > 0 && (Y + R) < a
        isCrossing = false;
        % Sprawdzenie czy okrąg nie przetnie żadnego innego narysowanego okręgu
       for i = 1:n-1
           if (X - x(i))^2 + (Y - y(i))^2 < (R + r(i))^2
              isCrossing = true;
              break;
           end
       end
        if ~isCrossing
            x(n) = X;
            y(n) = Y;
            r(n) = R;
            areas(n) = pi * r(n)^2;
            plot_circle(X,Y,R)
            % Dodanie tytułu i ustawienie osi po narysowaniu 1. okręgu
            if n == 1
                title("Pęcherzykowy kwadrat")
                xlabel("x")
                ylabel("y")
                axis equal
                axis([0 a 0 a])
            end
            hold on
            pause(0.01)
            n = n + 1;
        else
            % Jeśli wartości się nie zgadzają, 
            % zwiększ ilość prób i losuj ponownie
            tries(n) = tries(n) + 1; 
        end
    else
        tries(n) = tries(n) + 1;
    end

end

%% Zadanie A
% Wykres sumy powierzchni kół zawartych w rysowanych okręgach
% w funkcji liczby dotychczas narysowanych okregów

figure
plot(cumsum(areas))
xlabel("Liczba narysowanych okręgów")
ylabel("Powierzchnia")
title("Powierzchnia całkowita kół")

%% Zadanie B
% Wykres przedstawiajacy historię średniej liczby losowań wymaganych
% do narysowania pierwszych $n$ okregów
figure
plot(cumsum(tries)./(1:n_max)')
xlabel("Liczba narysowanych okręgów")
ylabel("Liczba losowań")
title("Średnia liczba losowań")
