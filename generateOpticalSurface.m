function optical_surface = generateOpticalSurface(f, K, a, d, px_s, coeffs_array)
    
    % INPUTS:
    %   f               - focal length
    %   K               - cone constant
    %   a               - numerical aperture
    %   d               - thickness
    %   px_s            - pixel size
    %   coeffs_array    - asphericity coefficient table []
    % OUTPUT:
    %   optical_surface - A grayscale image of the optical surface structure.

    % TO DO:
    % - problem grubość=ci?

    % Call the function to calculate the optical surface
    [F_sum, x, y, X, Y] = calculateOpticalSurface(f, K, d, a, px_s, coeffs_array);

    % Grey structure map
    surface = mat2gray(F_sum);
    surface = imresize(surface, [500,500]);
    imwrite(surface, 'surface_3D.png');
    
    % Illustrative charts
    figure;
    
    % 3D surface plot
    subplot(2,2,1)
    surf(X,Y,F_sum)
    title('3D Surface Plot');
    grid on;
    
    % Contour chart
    subplot(2,2,2)
    contour(X,Y,F_sum,20)
    title('Contour Plot');
    grid on;
    
    % Profile along the X axis (Y=0)
    subplot(2,2,3)
    plot(x, F_sum(x==0, :))
    title('Profile along X-axis (Y=0)');
    
    % Profile along the Y axis (X=0)
    subplot(2,2,4)
    plot(y, F_sum(:, y==0))
    title('Profile along Y-axis (X=0)');
    optical_surface = surface;

end

function [F_sum, x, y, X, Y] = calculateOpticalSurface(f, K, d, a, px_s, coeffs_array)
    % Function to calculate the optical surface
    
    % Determine the number of coefficients
    num_coeffs = length(coeffs_array);
  
    % Generate coordinate arrays based on the numerical aperture
    if mod(a, 2)
        x = linspace((-(a-1)/2), ((a-1)/2), a);
    else
        x = (-a/2):px_s:(a/2);
    end

    y = x;
    [X, Y] = meshgrid(x, y);

    R = 2 * f;
    
    F = []; 
    
    % Calculations
    if num_coeffs == 0
        F(:,:,1) = d * (Y.^2 + X.^2) / R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2));
        F_sum = F;
    else
        for i = 1:num_coeffs
            F(:,:,i) = d * ((Y.^2 + X.^2) / R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2))) + coeffs_array(i) * (Y.^(2*i + 2));
        end
        F_sum = sum(F, 3);
    end

    % Check if user doesn't enter d greater than the actual value
    if d > max(max(F_sum))
        d = max(max(F_sum));
        F_sum = calculateOpticalSurface(f, K, d, a, px_s, coeffs_array);
    end

    % Normalize the surface
    F_sum = F_sum - min(min(F_sum));
end