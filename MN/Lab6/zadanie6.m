clc
clear all
close all

warning('off','all')

load trajektoria2

N = 60;
xa = aproksymacjaTrygonometryczna(n, x, N);  % aproksymacja wspolrzednej x
ya = aproksymacjaTrygonometryczna(n, y, N);  % aproksymacja wspolrzednej y
za = aproksymacjaTrygonometryczna(n, z, N);  % aproksymacja wspolrzednej z

plot3(x,y,z,'o');
grid on
axis equal
hold on
plot3(xa,ya,za,'g','lineWidth', 4);
title('Aproksymacja trygometryczna trajektorii (2) drona (N = 60)');
xlabel('x (m)');
ylabel('y (m)');
zlabel('z (m)');
hold off

saveas(gcf,'zadanie6a.png');

M = 151;

for N = 1:71
    xa = aproksymacjaTrygonometryczna(n, x, N);  % aproksymacja wspolrzednej x
    ya = aproksymacjaTrygonometryczna(n, y, N);  % aproksymacja wspolrzednej y
    za = aproksymacjaTrygonometryczna(n, z, N);  % aproksymacja wspolrzednej z

    errx = sqrt(sum((x-xa).^2)/M);
    erry = sqrt(sum((y-ya).^2)/M);
    errz = sqrt(sum((z-za).^2)/M);

    err(N) = errx + erry + errz;
    
end

figure
semilogy(err);
title('Błąd aproksymacji trygonometrycznej trajektorii (2) drona');
xlabel('Rząd aproksymacji N');
ylabel('Wartość błędu');
saveas(gcf,'zadanie6b.png');

N = 150;
xa = aproksymacjaTrygonometryczna(n, x, N);  % aproksymacja wspolrzednej x
ya = aproksymacjaTrygonometryczna(n, y, N);  % aproksymacja wspolrzednej y
za = aproksymacjaTrygonometryczna(n, z, N);  % aproksymacja wspolrzednej z

figure
plot3(x,y,z,'o');
grid on
axis equal
hold on
plot3(xa,ya,za,'g','lineWidth', 4);
title('Aproksymacja trygometryczna trajektorii (2) drona (N = 150)');
xlabel('x (m)');
ylabel('y (m)');
zlabel('z (m)');
hold off

saveas(gcf,'zadanie6c.png');