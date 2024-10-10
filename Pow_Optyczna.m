clc; clearvars; close all;

f = input('Podaj wartość ogniskowej: ');
K = input('Podaj wartość stałej stożkowej: ');
a = input('Podaj wartość apertury: ');
t = input('Podaj wartość grubości: '); 

% Tablica współczynników asferyczności
coeffs_array = input('Podaj współczynniki asferyczności oddzielone spacjami w postaci [x1 x2 ....]: ');
num_coeffs = length(coeffs_array);

% pixel_size = input('Podaj rozmiar piksela: ');
pixel_size = 0.5;

% Pomocniczna tablica na funkcję
F = [];
index = 1;

% skok x
c = pixel_size;
a_eq = a / 2;

x = (-a_eq):c:(a_eq);
y = x;

[X,Y] = meshgrid(x);
R = 2 * f;

if num_coeffs == 0
    F(:,:,1) = t * (Y.^2+X.^2)/ R+sqrt(R^2 - (K+1).*(Y.^2+X.^2));
    F_sum = F;
else
    for i = 1:num_coeffs
        F(:,:,i) = t * ((Y.^2+X.^2)/ R+sqrt(R^2 - (K+1).*(Y.^2+X.^2))) + coeffs_array(i) * (Y.^(2*i + 2));
        index = index + 1; 
    end
    F_sum = sum(F, 3);
end

% Zapis szarej mapy struktury
wykres = mat2gray(F_sum);
wykres = imresize(wykres, [500,500]);
imwrite(wykres, 'powierzchnia_3D.png');

% Tworzenie pozostałych wykresów poglądowych
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
