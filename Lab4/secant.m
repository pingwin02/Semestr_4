function [xvect,xdif,fx,it_cnt] = secant(fun,a,b,eps)
% fun - funkcja, ktorej miejsce zerowe bedzie poszukiwane
% [a,b] - przedzial poszukiwania miejsca zerowego
% eps - prog dokladnosci obliczen
% 
% xvect - wektor kolejnych wartosci przyblizonego rozwiazania
% xdif - wektor roznic pomiedzy kolejnymi wartosciami przyblizonego rozwiazania
% fx - wektor wartosci funkcji dla kolejnych elementow wektora xvect
% it_cnt - liczba iteracji wykonanych przy poszukiwaniu miejsca zerowego

    it_cnt = 1;

    xvect(1) = a;
    xvect(2) = b;

    fx(1) = fun(a);
    fx(2) = fun(b);
    
    for i = 2:1000
        xvect(i + 1) = xvect(i) - ...
            (fx(i) * (xvect(i) - xvect(i - 1))) / ...
            (fx(i) - fx(i - 1));

        fx(i + 1) = fun(xvect(i + 1));

        if abs(fx(i + 1)) < eps
            break
        end
    
        it_cnt = it_cnt + 1;
    end

    xdif = abs(diff(xvect));

end

