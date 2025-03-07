function optical_surface = generateOpticalSurface(f, K, a, d, px_s, varargin)

    % INPUTS:
    %   f               - focal length
    %   K               - cone constant
    %   a               - aperture
    %   d               - thickness
    %   px_s            - pixel size
    %   coeffs_array    - asphericity coefficient table []
    % OUTPUT:
    %   optical_surface - A grayscale image of the optical surface structure.

    % TO DO:
    % - problem kształtu obówdki - zerowanie lub nie
    % - rozmieszczenie w zależności od parzystego/ nieparzystego a?


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % previous version of variable argument number handling didn't support
    % multiple arguments
    % version below is shorter and works
    % NOT TESTED FOR ASPERIC COEFFICIENT
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if nargin < 7, coeffs_array = 0; else coeffs_array = varargin{2};  end
    if nargin < 6, shape = 0; else shape = varargin{1}; end
   
    % Determine the number of coefficients
    num_coeffs = length(coeffs_array);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % integrated calculation function into the main function. MATLAB doesn't
    % support calling nested functions from a file. If you really need to
    % separate calculation and generation, consider separate files
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % Generate coordinate arrays based on the numerical aperture

    x = (-a/2+0.5*px_s):px_s:(a/2-0.5*px_s); % now correctly generates arrays for pixels different than 1
    len = length(x) % store array length for later

    y = x;

    [X, Y] = meshgrid(x, y);
    length(X)
    length(Y)
    R = 2 * f;
    F = []; 
    
    % Calculations
    if num_coeffs == 1
        F_sum = (Y.^2 + X.^2) ./ R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2));
    else
        for i = 1:num_coeffs
            disp('Asferyczna')
            F = zeros(size(Y,1), size(Y,2), num_coeffs);  
            F(:,:,i) = ((Y.^2 + X.^2) / R + sqrt(R^2 - (K + 1) .* (Y.^2 + X.^2))) + coeffs_array(i) * (Y.^(2*i + 2));
        end
        F_sum = sum(F, 3);
    end

    F_sum = F_sum - min(min(F_sum)); % normalization

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% many changes below, basically a total overhaul
% what we need from this block is to:
% - separate two cases - positive and negative focal length
% - decide when to include thickness for each case
% - decide which pixel is the source of height for the non-zero mask (edge
% of the circle)
% - end up with circle of thickness equal or higher than d
% - end up with zeros around for negative f or max around for positive f
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %Zerowanie obwodki - z równania okręgu X, Y, A
    if shape ~= 0
        if f > 0
            F_sum(X.^2 + Y.^2 > (a/2)^2) = F_sum(round(len/2),1);
            if d > max(max(F_sum))
                F_sum = F_sum - max(max(F_sum)) + d;
            end
        else
            F_sum = F_sum - F_sum(round(len/2),1);
            if d > max(max(F_sum))
                F_sum = F_sum - max(max(F_sum)) + d;
            end
            F_sum(X.^2 + Y.^2 > X(len,len)^2 + Y(round(len/2),round(len/2))^2) = -(max(max(F_sum)) - min(min(F_sum)))/256;
        end
    end

    % Grey structure map
    optical_surface = mat2gray(F_sum);
    imwrite(optical_surface, 'lens1.png');
   
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
    
    % now generates correct values for different pixels and all cases

    % Profile along the X axis (Y=0)
    subplot(2,2,3)
    plot(F_sum(round(len/2),:));
    title('Profile along X-axis'); 

    
    % Profile along the Y axis (X=0)
    subplot(2,2,4)
    plot(F_sum(:,round(len/2)));
    title('Profile along Y-axis');

    end