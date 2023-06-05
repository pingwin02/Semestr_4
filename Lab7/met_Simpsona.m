function [ calka ] = met_Simpsona(f,n,N)

calka = 0;
delta = n / N;

x = linspace(0, n, N + 1);

for i=1:N
    calka = calka + f(x(i)) + 4 * f((x(i) + x(i+1))/ 2) + f(x(i+1));
end

calka = delta / 6 * calka;

end