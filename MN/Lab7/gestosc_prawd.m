function [ f ] = gestosc_prawd(t)
    sigma = 3;
    mikro = 10;

    f = 1/(sigma*sqrt(2*pi))*exp(-((t-mikro).^2)/(2*sigma^2));
end