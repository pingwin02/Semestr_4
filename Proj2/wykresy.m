clc
clear all
close all

wynikJacobi = readmatrix("res1.csv");
wynikGauss = readmatrix("res2.csv");

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

wynikJacobi = readmatrix("res3.csv");
wynikGauss = readmatrix("res4.csv");

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


czasJacobi = readmatrix("wynik1.csv");
czasGauss = readmatrix("wynik2.csv");

plot(czasJacobi(:,1), czasJacobi(:,2), 'LineWidth', 2)
hold on
plot(czasGauss(:,1), czasGauss(:,2), 'LineWidth', 2)
hold off
xlabel("Wielkość macierzy (N)")
ylabel("Czas (s)")
title("Czas wykonania algorytmów dla zadania E")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadE.png")

plot(czasJacobi(:,1), czasJacobi(:,3), 'LineWidth', 2)
hold on
plot(czasGauss(:,1), czasGauss(:,3), 'LineWidth', 2)
hold off
xlabel("Wielkość macierzy (N)")
ylabel("Ilość")
title("Ilość iteracji dla zadania E")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadE_iter.png")