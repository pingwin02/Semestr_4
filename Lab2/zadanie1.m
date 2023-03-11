clc
clear all
close all

a = 5;
r_max = a/2;
n_max = 200;

x = zeros(n_max, 1);
y = zeros(n_max, 1);
r = zeros(n_max, 1);
areas = zeros(n_max, 1);
tries = ones(n_max, 1);

n = 1;

while n <= n_max
    X = rand(1)*a;
    Y = rand(1)*a;
    R = rand(1)*r_max;

    if (X - R) > 0 && (X + R) < a && ...
       (Y - R) > 0 && (Y + R) < a
        isCrossing = false;
       for i = 1:n-1
           if (X - x(i))^2 + (Y - y(i))^2 < (R + r(i))^2
              isCrossing = true;
              break;
           end
       end
        if ~isCrossing
            x(n) = X;
            y(n) = Y;
            r(n) = R;
            areas(n) = pi * r(n)^2;
            plot_circle(X,Y,R)
            axis equal
            axis([0 a 0 a])
            hold on
            pause(0.01)
            n = n + 1;
        else
            tries(n) = tries(n) + 1;
        end
    else
        tries(n) = tries(n) + 1;
    end

end