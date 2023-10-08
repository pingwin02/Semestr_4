function [ calka ] = met_MonteCarlo(f,n,N)

a = n;
b = f(n);

counter = 0;

for i=1:N
    x = rand * a;
    y = rand * b;

    if y < f(x)
        counter = counter + 1;
    end

end

calka = counter / N * a * b;


end