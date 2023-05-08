%% Zadanie 1

clear all
close all
clc

K = [5, 15, 25, 35];
[XX,YY] = meshgrid(linspace(0,1,101),linspace(0,1,101));

for i = 1:4 

    [x,y,f,xp,yp] = lazik(K(i));

    % interpolacja wielomianowa
    [p] = polyfit2d(x,y,f);
    [FP] = polyval2d(XX,YY,p);

    % interpolacja trygonometryczna
    [t] = trygfit2d(x,y,f);
    [FT] = trygval2d(XX,YY,t);

    % wykresy
    figure
    subplot(2,2,1)
    plot(xp,yp,'-o','linewidth',1, 'MarkerSize', 2)
    xlabel("x")
    ylabel("y")
    title("Tor ruchu łazika")
    subplot(2,2,2)
    surf(reshape(x,K(i),K(i)), reshape(y,K(i),K(i)), reshape(f,K(i),K(i)))
    shading flat
    xlabel("x")
    ylabel("y")
    zlabel("f(x,y)")
    title("Wartości próbek")
    subplot(2,2,3)
    surf(XX,YY,FP)
    shading flat
    xlabel("x")
    ylabel("y")
    zlabel("f(x,y)")
    title("Interpolacja wielomianowa")
    subplot(2,2,4)
    surf(XX,YY,FT)
    shading flat
    xlabel("x")
    ylabel("y")
    zlabel("f(x,y)")
    title("Interpolacja trygonometryczna")

    sgtitle(['K=' num2str(K(i))])

    saveas(gcf, ['zad1_K' num2str(K(i)) '.png'])

end

%% Zadanie 2

clear all
clc

[XX,YY] = meshgrid(linspace(0,1,101),linspace(0,1,101));

[x,y,f,xp,yp] = lazik(4);
[p] = polyfit2d(x,y,f);
F2 = polyval2d(XX,YY,p);

% interpolacja wielomianowa
for i = 5:45
    [x,y,f,xp,yp] = lazik(i);
    [p] = polyfit2d(x,y,f);
    [F1] = polyval2d(XX,YY,p);
    Div(i) = max(max(abs(F1-F2)));
    F2 = F1;
end
figure
plot(Div)
xlabel("Liczba punktów pomiarowych K")
xlim([5 45])
ylabel("Wartość maksymalnej różnicy")
title("Zbieżność metody interpolacji wielomianowej")
saveas(gcf, "zad2_divK_wiel.png")

[x,y,f,xp,yp] = lazik(4);
[p] = trygfit2d(x,y,f);
F2 = trygval2d(XX,YY,p);

% interpolacja trygonometryczna
for i = 5:45
    [x,y,f,xp,yp] = lazik(i);
    [p] = trygfit2d(x,y,f);
    [F1] = trygval2d(XX,YY,p);
    Div(i) = max(max(abs(F1-F2)));
    F2 = F1;
end

plot(Div)
xlabel("Liczba punktów pomiarowych K")
xlim([5 45])
ylabel("Wartość maksymalnej różnicy")
title("Zbieżność metody interpolacji trygonometrycznej")
saveas(gcf, "zad2_divK_tryg.png")