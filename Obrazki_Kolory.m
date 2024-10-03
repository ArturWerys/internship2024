clc, clearvars, close all;

img = imread('peppers.png'); % Wbudowany obraz

figure;
set(gcf, 'Position', [150, 100, 1200, 400]); % Ustawienie wielkości okna

% Pierwszy podwykres: kolorowy obraz
subplot(1, 3, 1);
imshow(img);
title('Kolorowy obraz');
set(gca, 'Position', [0.05, 0.1, 0.25, 0.9]); % [left, bottom, width, height]

% Drugi podwykres: obraz w odcieniach szarości
gray_img = rgb2gray(img);
subplot(1, 3, 2);
imshow(gray_img);
title('Szary obraz');
set(gca, 'Position', [0.35, 0.1, 0.25, 0.9]);

% Trzeci podwykres: obraz binarny
bw_img = imbinarize(gray_img, 'adaptive');
subplot(1, 3, 3);
imshow(bw_img);
title('Obraz binarny');
set(gca, 'Position', [0.65, 0.1, 0.25, 0.9]);
