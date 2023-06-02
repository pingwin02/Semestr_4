function [ calka ] = met_Simpsona(f,n,N)

calka = 0;
delta = n / N;

x = linspace(0, n, N);

for i=2:N
    calka = calka + f(x(i-1)) + 4 * f((x(i-1) + x(i))/ 2) + f(x(i));
end

calka = delta / 6 * calka;

end