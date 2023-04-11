clc
clear all
close all


a = 0;   
b = 50;

[xvect, xdif, fx, it_cnt] = bisect(a,b,1e-12,@compute_impedance);