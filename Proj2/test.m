N = 997;

e = 5;
a1 = 3;
a2 = -1;
a3 = -1;
on = ones(N, 1);

A = spdiags([a3*on a2*on a1*on a2*on a3*on], -2:2, N, N);

b = zeros(N, 1);
for i=0:N-1
     b(i+1) = sin(i * 9);
end

b;

x = A\b;

disp(x(1:6));