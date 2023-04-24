clc
clear all
close all

wynikJacobi = readmatrix("wynik1.csv");
wynikGauss = readmatrix("wynik2.csv");

semilogy(wynikJacobi, 'LineWidth', 2)
hold on
semilogy(wynikGauss, 'LineWidth', 2)
hold off
yline(1e-9, '--r')
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title("Wartość normy błędu rezydualnego dla zadania B")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadB.png")

wynikJacobi = readmatrix("wynik3.csv");
wynikGauss = readmatrix("wynik4.csv");

semilogy(wynikJacobi, 'LineWidth', 2)
hold on
semilogy(wynikGauss, 'LineWidth', 2)
hold off
yline(1e-9, '--r')
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title("Wartość normy błędu rezydualnego dla zadania C")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadC.png")


czasJacobi = readmatrix("wynikCzas1.csv");
czasGauss = readmatrix("wynikCzas2.csv");

plot(czasJacobi(:,1), czasJacobi(:,2), 'LineWidth', 2)
hold on
plot(czasGauss(:,1), czasGauss(:,2), 'LineWidth', 2)
hold off
xlabel("Wielkość macierzy (N)")
ylabel("Czas (s)")
title("Czas wykonania algorytmów dla zadania E")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadE.png")