%% Zadanie B
clc
clear all
close all

a = 1;   
b = 60000;

[xvect, xdif, fx1, it_cnt1] = bisection(@compute_execution_time,a,b,1e-3);
[xvect2, xdif2, fx2, it_cnt2] = secant(@compute_execution_time,a,b,1e-3);

figure
plot(xvect)
hold on
plot(xvect2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Wartość przybliżonego rozwiązania funkcji A")
saveas(gcf, 'funA_a.png')


figure
semilogy(xdif)
hold on
semilogy(xdif2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Zmiana wartości przybliżonego rozwiązania funkcji A")
saveas(gcf, 'funA_b.png')

clear all

a = 0.1;   
b = 50;

[xvect, xdif, fx1, it_cnt1] = bisection(@compute_impedance,a,b,1e-12);
[xvect2, xdif2, fx2, it_cnt2] = secant(@compute_impedance,a,b,1e-12);
figure
plot(xvect)
hold on
plot(xvect2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Wartość przybliżonego rozwiązania funkcji B")
saveas(gcf, 'funB_a.png')


figure
semilogy(xdif)
hold on
semilogy(xdif2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Zmiana wartości przybliżonego rozwiązania funkcji B")
saveas(gcf, 'funB_b.png')

clear all

a = 0;   
b = 50;

[xvect, xdif, fx1, it_cnt1] = bisection(@compute_rocket_velocity,a,b,1e-12);
[xvect2, xdif2, fx2, it_cnt2] = secant(@compute_rocket_velocity,a,b,1e-12);

figure
plot(xvect)
hold on
plot(xvect2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Wartość przybliżonego rozwiązania funkcji C")
saveas(gcf, 'funC_a.png')


figure
semilogy(xdif)
hold on
semilogy(xdif2)
hold off
legend("Metoda bisekcji", "Metoda siecznych")
xlabel("nr iteracji")
ylabel("wartość")
title("Zmiana wartości przybliżonego rozwiązania funkcji C")
saveas(gcf, 'funC_b.png')

%% Zadanie C

clc
clear all
close all

options = optimset('Display','iter');
fzero(@tan,6, options)
fzero(@tan,4.5, options)