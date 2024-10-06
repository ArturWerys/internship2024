clc; clearvars; close all;

f = input('Podaj wartość ogniskowej: ');
K = input('Podaj wartość stałej stożkowej: ');
a = input('Podaj wartość apertury: ');

t = input('Podaj wartość grubości: '); % Grubość
pixel_size = input('Podaj rozmiar piksela: ');

num_coeffs = input('Podaj ile współczynników asferyczności chcesz podać: ');

% Tablica współczynników
A = [];
F = [];
index = 1;

% skok x
c = 0.5 * pixel_size; % Modyfikacja skoku na podstawie rozmiaru piksela
a_eq = a / 2;

x = (-a_eq):c:(a_eq);
y = x;

[X,Y] = meshgrid(x);
R = 2 * f;

if num_coeffs == 0
    % Uwzględnienie grubości w równaniu
    F(:,:,1) = t * (Y.^2 / R + sqrt(R^2 - (K + 1) * Y.^2)); 
    F_sum = F;
else
    for i = 1:num_coeffs
        A(index) = input(['Podaj wartość A', num2str(2*i + 2), ': ']);
        % Uwzględnienie grubości w równaniu
        F(:,:,index) = t * (Y.^2 / R + sqrt(R^2 - (K + 1) * Y.^2)) + A(index) * (Y.^(2*i + 2));
        index = index + 1; 
    end
    F_sum = sum(F, 3);
end

% Zapis powierzchni 3D do pliku
figure;
surf(X, Y, F_sum)
colormap(gray);
colorbar; 
title('Wykres powierzchni 3D w szarych kolorach');
grid on;

% Tworzenie pozostałych wykresów poglądowych w osobnym okienku
figure;

% Wykres powierzchni 3D
subplot(2,2,1)
surf(X,Y,F_sum)
title('Wykres powierzchni 3D');
grid on;

% Wykres konuturowy
subplot(2,2,2)
contour(X,Y,F_sum,20)
title('Wykres konturowy');
grid on;

% Profil wzdłuż osi X (Y=0)
subplot(2,2,3)
plot(x, F_sum(x==0, :))
title('Profil wzdłuż osi X przy Y=0');

% Profil wzdłuż osi Y (X=0)
subplot(2,2,4)
plot(y, F_sum(:, y==0))
title('Profil wzdłuż osi Y przy X=0');
