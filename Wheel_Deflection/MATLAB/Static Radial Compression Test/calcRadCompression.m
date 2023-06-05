% Calculate the radial compression of the rim using the change of the 
% difference between the top of the rim and the axel.

% Input: 
% m_axle = The y position values of the axle marker
% m_rim_top = The y position values of the top of the rim marker

% Output: 
% radial_compression = the smoothed values of radial compression throughout
% the test.

function radial_compression = calcRadCompression(m_axle, m_rim_top)

    radial_vector = m_axle - m_rim_top;
    radial_length = sqrt(sum(radial_vector.^2 , 2));
    radial_compression = radial_length - radial_length(1);
    
    % The data is pretty noisy, so I'm going to do a moving mean smoothing
    % filter
    radial_compression = movmean(radial_compression, 50);
    
    % TO DO: get slow mow vid of test and see why this is happening! 
    %   Ideas:
    %       Perhaps it is vibrating as we contact different knobs of the tread
    %       Vibrating from squishing into that mucked up pillow block
    %       Vibrations from the machine's feedback loop

end