clc
clear all
close all

normJacobi = readmatrix("normaResA_Jacobi.csv");
normGauss = readmatrix("normaResA_GaussSeidel.csv");

semilogy(normJacobi, 'LineWidth', 2)
hold on
semilogy(normGauss, 'LineWidth', 2)
hold off
yline(1e-9, '--r')
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title("Wartość normy błędu rezydualnego dla zadania B")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadB.png")

normJacobi = readmatrix("normaResC_Jacobi.csv");
normGauss = readmatrix("normaResC_GaussSeidel.csv");

semilogy(normJacobi, 'LineWidth', 2)
hold on
semilogy(normGauss, 'LineWidth', 2)
hold off
yline(1e-9, '--r')
xlabel("Numer iteracji")
ylabel("Norma błędu rezydualnego")
title("Wartość normy błędu rezydualnego dla zadania C")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla')
saveas(gcf, "zadC.png")


czasJacobi = readmatrix("wynikA_Jacobi.csv");
czasGauss = readmatrix("wynikA_GaussSeidel.csv");
czasLU = readmatrix("wynikA_LU.csv");

plot(czasJacobi(:,1), czasJacobi(:,2), 'LineWidth', 2)
hold on
plot(czasGauss(:,1), czasGauss(:,2), 'LineWidth', 2)
hold off
hold on
plot(czasLU(:,1), czasLU(:,2), 'LineWidth', 2)
hold off
xlabel("Wielkość macierzy (N)")
ylabel("Czas (s)")
title("Czas wykonania algorytmów dla zadania E")
legend('Metoda Jacobiego', 'Metoda Gaussa-Seidla', ...
    'Metoda faktoryzacji LU')
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