% Mocap data processing function 

% Input: 
% filePath = the path to the .csv file containing the data
% collected by the mocap system.

% Output:
% mocap = matrix of the edited mocap data (trimmed to when the MTS test 
% begins, scaled values to match the MTS data, and reoriented values to 
% match MTS).
% RimTop = the matrix columns in mocap that represent the reflective dot
% at the top of the rim.
% Center = the matrix columns corresponding to the reflective dot on the 
% center of the rim.
% I = index of the matrix column corresponding to the MTS head reflective 
% dot.

function [mocap, RimTop, Center, I] = cleanMocapData(filePath)

    mocap = readmatrix(filePath);
    mocap = mocap(7:end,:);
    
    %need to find MTS head column
    [MAX,I] = max(mocap(8,1:end));
    Pert = [mocap(8,4:3:end)];
    
    %takes the max out of the array
    for i = 1:4
        if Pert(1,i) == MAX
            Pert(1,i) = 0;
        end
    end
    
    %Finds new max, which is the top of the rim and then sets it to zero.
    %Also scales it to the correct size
    [MidHigh,RimTop] = max(Pert);
    Pert(RimTop) = 0;
    RimTop = (RimTop-1)*3+4;
    
    %Newest max is now the center marker, which is then scaled.
    [MidLow,Center] = max(Pert);
    Center = (Center-1)*3+4;
    
    % Pull out the head marker height (y-axis), offset it to zero, and invert
    % to match MTS orientation
    mo_head_height = mocap(:,I);
    mo_head_height = mo_head_height - mo_head_height(1);
    mo_head_height = -mo_head_height;
    
    % Find where the height starts to move (this is when the MTS test begins)
    thresh = 0.05; % mm
    starting_index = find(mo_head_height > thresh, 1);
    
    % Find where compression ends
    peak_height = max(mo_head_height);
    thresh = .025;
    
    index_of_top_height = find(mo_head_height > peak_height-thresh, 1);
    
    % Now trim all of the mocap data based on these bounds
    mocap = mocap(starting_index:index_of_top_height,:);
end