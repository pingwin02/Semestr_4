function [ calka ] = met_prostokatow(f,n,N)


calka = 0;
delta = n / N;

x = linspace(0, n, N + 1);

for i=1:N
    calka = calka + f((x(i) + x(i+1))/2) * delta;
end

end