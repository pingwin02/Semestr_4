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