function [value] = compute_rocket_velocity( time )

    m = 150000;
    q = 2700;
    u = 2000;
    g = 9.81;

    value = u * log(m/(m-q*time)) - g * time - 750;

end

