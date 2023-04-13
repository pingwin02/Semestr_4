clc
clear all
close all


a = 1;   
b = 60000;

[xvect, xdif, fx, it_cnt] = bisection(@compute_execution_time, a,b,1e-3);

figure
plot(xvect)
xlabel("nr iteracji")
ylabel("wartość")
title("Wartość przybliżonego rozwiązania funkcji A")

figure
semilogy(xdif)
xlabel("nr iteracji")
ylabel("wartość")
title("Zmiana wartości przybliżonego rozwiązania funkcji A")