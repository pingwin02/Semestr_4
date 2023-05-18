clc
clear all
close all

warning('off','all')

load trajektoria1

N = 60;
xa = aproksymacjaWielomianowa(n, x, N);  % aproksymacja wspolrzednej x
ya = aproksymacjaWielomianowa(n, y, N);  % aproksymacja wspolrzednej y
za = aproksymacjaWielomianowa(n, z, N);  % aproksymacja wspolrzednej z

plot3(x,y,z,'o');
grid on
axis equal
hold on
plot3(xa,ya,za,'g','lineWidth', 4);
title('Aproksymacja wielomianowa trajektorii (1) drona (N = 60)');
xlabel('x (m)');
ylabel('y (m)');
zlabel('z (m)');
hold off

saveas(gcf,'zadanie4.png');