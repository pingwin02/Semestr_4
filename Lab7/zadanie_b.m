clc
clear all


%------------------------------------------
load dane_jezioro   % dane XX, YY, FF sa potrzebne jedynie do wizualizacji problemu. 
surf(XX,YY,FF)
shading interp
axis equal
%------------------------------------------


%------------------------------------------
% Implementacja Monte Carlo dla f(x,y) w celu obliczenia objetosci wody w zbiorniku wodnym. 
% Calka = ?
% Nalezy skorzystac z nastepujacej funkcji:
% z = glebokosc(x,y); % wyznaczanie glebokosci jeziora w punkcie (x,y),
% gdzie x i y sa losowane
%------------------------------------------

X = 100;
Y = 100;
Z = 50;

N = 10^5;

counter = 0;

for i=1:N
    x = rand * X;
    y = rand * Y;
    z = - rand * Z;

    if z > glebokosc(x, y)
        counter = counter + 1;
    end

end

calka = counter / N * X * Y * Z;

fprintf("Objętość wody w zbiorniku wodnym: %0.1f m^3\n", calka);