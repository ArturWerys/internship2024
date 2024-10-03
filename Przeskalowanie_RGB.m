clc, clearvars, close all;

img = imread('peppers.png'); % Wbudowany obraz

% Zakres docelowy
new_min = 100;
new_max = 120;

% Przeskalowanie obrazu
img_scaled = double(img); % Zamiana na typ double dla operacji matematycznych
% Wartości pikseli w obrazach są zazwyczaj w formacie uint8, który ma zakres od 0 do 255, 
% przekształcenie do double umożliwia bardziej precyzyjne obliczenia.

% Obliczanie wartości minimalnych i maksymalnych
img_min = min(img_scaled(:));
img_max = max(img_scaled(:));

% Normalizacja obrazu do zakresu [0, 1]
img_normalized = (img_scaled - img_min) / (img_max - img_min);

% Przeskalowanie do nowego zakresu
img_scaled = img_normalized * (new_max - new_min) + new_min;

% Konwersja z powrotem na uint8, jeśli potrzebne
img_scaled = uint8(img_scaled);

% Wyświetlenie przeskalowanego obrazu
imshow(img_scaled);
title(['Obraz przeskalowany do zakresu [', num2str(new_min), ', ', num2str(new_max), ']']);