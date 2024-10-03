clc, clearvars, close all;

R = input('Podaj wartość R: ');
K = 2;

a = input("Podaj wartość początkową x: ");
b = input("Podaj wartość końcową x: ");
c = input("Podaj skok x: ");

x = a:c:b;
y = x;
[X,Y] = meshgrid(x);

F = (Y.^2/ R+sqrt(R^2 - (K+1)*Y.^2));
figure;

% Wykres powierzchni 3D
subplot(2,2,1)
surf(X,Y,F)
title('Wykres powierzchni 3D');
grid on;

% Wykres konuturowy
subplot(2,2,2)
contour(X,Y,F,20)
title('Wykres konturowy');
grid on;

% Profil wzdłuż osi X (Y=0)
subplot(2,2,3)
plot(x, F(x==0, :))
title('Profil wzdłuż osi X przy Y=0');

% Profil wzdłuż osi Y (X=0)
subplot(2,2,4)
plot(y, F(:, y==0))
title('Profil wzdłuż osi Y przy X=0');