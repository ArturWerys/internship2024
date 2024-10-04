clc, clearvars, close all;

f = input('Podaj wartość ogniskowej: ');
K = input('Podaj wartość stałej stożkowej: ');
a = input("Podaj wartość apertury: ");

% skok x
c = 0.5;

a_eq = a/2;

x = (-a_eq):c:(a_eq);
y = x;
[X,Y] = meshgrid(x);

R = 2*f;
F = (Y.^2/ R+sqrt(R^2 - (K+1)*Y.^2));


% Zapis powwierzchni 3D do pliku
figure;
surf(X,Y,F)

% Zmiana koloru
colormap(gray);
colorbar; 

title('Wykres powierzchni 3D w szarych kolorach');
grid on;
saveas(gcf, 'powierzchnia_3D.png');

% Tworzenie pozostałych wykresów poglądowych w osobnym okienku
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


