function [ calka ] = met_trapezow(f,n,N)

calka = 0;
delta = n / N;

x = linspace(0, n, N + 1);

for i=2:N
    calka = calka + f(x(i));
end

calka = (calka + (f(x(1)) + f(x(N+1))) / 2) * delta;

end