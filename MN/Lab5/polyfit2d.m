function [p] = polyfit2d(x,y,f)
%
%   A*p = f
%

M = sqrt(size(x,1))-1;
N=M;

xx = x * ones(1,M+1);
mm = ones(size(x,1),1)*(0:M);
yy = y * ones(1,N+1);
nn = ones(size(y,1),1)*(0:N);

xm=xx.^mm;
yn=yy.^nn;

MN = (M+1)*(N+1);
A = zeros(MN,MN);

for k = 1:MN
    xmk = xm(k,:);
    ynk = yn(k,:);
    A(k,:) = kron(xmk,ynk);
end

% warning('on','MATLAB:nearlySingularMatrix');
warning('off','MATLAB:nearlySingularMatrix');

p = A\f;

end

