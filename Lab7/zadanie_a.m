clc
clear all
close all

x = linspace(0, 20, 100);
y = gestosc_prawd(x);

figure
plot(x, y);
xlabel('Czas t używania urządzenia liczony w latach');
ylabel('Gęstość prawdopodobieństwa f(t)');
title(["Wykres gęstości prawdopodobieństwa", ...
    "wystąpienia awarii urządzenia elektronicznego"]);
saveas(gcf, "gestosc.png");

clear all

n = 5;
i = 1;

for N = 5:50:10^4
    wart_prost(i) = met_prostokatow(@gestosc_prawd, n, N);
    wart_trap(i) = met_trapezow(@gestosc_prawd, n, N);
    wart_Simp(i) = met_Simpsona(@gestosc_prawd, n, N);
    wart_Monte(i) = met_MonteCarlo(@gestosc_prawd, n, N);
    x(i) = N;
    i = i + 1;
end

load("P_ref.mat");

wart_prost = abs(wart_prost - P_ref);
wart_trap = abs(wart_trap - P_ref);
wart_Simp = abs(wart_Simp - P_ref);
wart_Monte = abs(wart_Monte - P_ref);

figure
loglog(x, wart_prost);
hold on
loglog(x, wart_trap);
loglog(x, wart_Simp);
loglog(x, wart_Monte);
hold off
xlabel('Dokładność całkowania N');
ylabel('Błąd względem wartości referencyjnej');
lgd = legend('Metoda prostokątów', 'Metoda trapezów', ...
    'Metoda Simpsona', 'Metoda Monte Carlo');
lgd.Location = "best";
title("Wykres błędu całkowania w zależności od metody");
xlim([5 10^4]);

saveas(gcf, "bledy.png")

clear all

n = 5;

tic
met_prostokatow(@gestosc_prawd, n, 10^7);
czas_prost = toc;

tic
met_trapezow(@gestosc_prawd, n, 10^7);
czas_trap = toc;

tic
met_Simpsona(@gestosc_prawd, n, 10^7);
czas_Simp = toc;

tic
met_MonteCarlo(@gestosc_prawd, n, 10^7);
czas_Monte = toc;

figure
bar([czas_prost, czas_trap, czas_Simp, czas_Monte]);
ylabel('Czas całkowania [s]');
set(gca, 'XTickLabel', {'Metoda prostokątów', 'Metoda trapezów', ...
    'Metoda Simpsona', 'Metoda Monte Carlo'});
title("Wykres czasu całkowania w zależności od metody dla N = 10^7");

saveas(gcf, "czasy.png");