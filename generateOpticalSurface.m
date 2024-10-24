function optical_surface = generateOpticalSurface(f, K, a, d, px_s, coeffs_array)
    
    % To do :
    %   - zamienić program na funkcję zwracającą obraz
    %   - problem grubości
    %   - zerowanie obwódki
    %   - poprawa rozmiaru pixela
    %   - zamienić program na język angielski 
    %
    % INPUTS:
    %   f               - focal length
    %   K               - cone constant
    %   a               - numerical aperture
    %   d               - thickness
    %   px_s            - pixel size
    %   coeffs_array    - asphericity coefficient table
    %
    %
    % OUTPUT:
    %   optical_surface - A grayscale image of the optical surface structure.



    % Tablica współczynników asferyczności
    num_coeffs = length(coeffs_array);
  
    % Pomocniczna tablica na funkcję
    F = [];
    index = 1;
    
    if mod(a, 2) ~= 0
        x = linspace((-(a-1)/2),((a-1)/2), a);
    else
        x = (-a/2):px_s:(a/2);
    end

    y = x;
    
    [X,Y] = meshgrid(x);
    R = 2 * f;
    
    if num_coeffs == 0
        F(:,:,1) = d * (Y.^2+X.^2)/ R+sqrt(R^2 - (K+1).*(Y.^2+X.^2));
        F_sum = F;
    else
        for i = 1:num_coeffs
            F(:,:,i) = d * ((Y.^2+X.^2)/ R+sqrt(R^2 - (K+1).*(Y.^2+X.^2))) + coeffs_array(i) * (Y.^(2*i + 2));
            index = index + 1; 
        end
        F_sum = sum(F, 3);
    end
    
    % Zapis szarej mapy struktury
    wykres = mat2gray(F_sum);
    wykres = imresize(wykres, [500,500]);
    imwrite(wykres, 'surface_3D.png');
    
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

    optical_surface = wykres;

end
