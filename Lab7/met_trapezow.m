function [ calka ] = met_trapezow(f,n,N)

calka = 0;
delta = n / N;

x = linspace(0, n, N);

for i=2:N-1
    calka = calka + f(x(i));
end

calka = calka + (f(x(1)) + f(x(N))) / 2;
calka = delta * calka;

end