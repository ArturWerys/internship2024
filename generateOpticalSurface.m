function optical_surface = generateOpticalSurface(f, K, a, d, px_s, varargin)

    % INPUTS:
    %   f               - focal length
    %   K               - cone constant
    %   a               - aperture
    %   d               - thickness
    %   px_s            - pixel size
    %   shape           - round or square (0 or 1)
    %   coeffs_array    - asphericity coefficient table []
    % OUTPUT:
    %   optical_surface - A grayscale image of the optical surface structure.

    % TO DO:
    % - problem kształtu obówdki - zerowanie lub nie
    % - rozmieszczenie w zależności od parzystego/ nieparzystego a?

    % Call the function to calculate the optical surface
    
    if isempty(varargin)
        coeffs_array = 0; 
    else
        coeffs_array = cell2mat(varargin); 
    end
    [F_sum, x, y, X, Y] = calculateOpticalSurface(f, K, d, a, px_s, coeffs_array);
   
    % Grey structure map
    surface = mat2gray(F_sum);
    %surface = imresize(surface, [500,500]);
    imwrite(surface, 'surface_3D.png');
    
    % Illustrative charts
    figure;
    
    % 3D surface plot
    subplot(2,2,1)
    surf(X,Y,F_sum); shading flat
    title('3D Surface Plot');
    grid on;
    
    % Contour chart
    subplot(2,2,2)
    contour(X,Y,F_sum,20)
    title('Contour Plot');
    grid on;
    
    % Profile along the X axis (Y=0)
    index = abs(min(x));
    subplot(2,2,3)
    plot(x, F_sum(x == index, :))
    title('Profile along X-axis'); 

    
    % Profile along the Y axis (X=0)
    index = abs(min(y));
    subplot(2,2,4)
    plot(y, F_sum(:,y == index))
    title('Profile along Y-axis');

    optical_surface = surface;

end

function [F_sum, x, y, X, Y] = calculateOpticalSurface(f, K, d, a, px_s, coeffs_array)
    % Function to calculate the optical surface

    % Determine the number of coefficients
    num_coeffs = length(coeffs_array);
    
    % Generate coordinate arrays based on the numerical aperture

    x = (-a/2+0.5):px_s:(a/2-0.5);
    length(x)

    y = x;

    [X, Y] = meshgrid(x, y);
    length(X)
    length(Y)
    R = 2 * f;
    
    F = []; 
    
    % Calculations
    if num_coeffs == 1
        num_coeffs
        F_sum = (Y.^2 + X.^2) ./ R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2));
    else
        num_coeffs
        for i = 1:num_coeffs
            disp('Asferyczna')
            F = zeros(size(Y,1), size(Y,2), num_coeffs);  
            F(:,:,i) = ((Y.^2 + X.^2) / R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2))) + coeffs_array(i) * (Y.^(2*i + 2));
        end
        F_sum = sum(F, 3);
    end

   % Normalize the surface
   if d > max(max(F_sum))
        F_sum = F_sum - max(max(F_sum)) + d;
   end

   % Zerowanie obwodki - z równania okręgu X, Y, A
   % mask = (X.^2 + Y.^2 > (a/2)^2);
   % F_sum(mask) = d;

end
