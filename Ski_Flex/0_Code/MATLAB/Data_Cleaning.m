%% Average test data together, leaving outliers out of calculation

% Number of actual data points collected in each test
num_of_data_points = 11;

% Number of standard deviations data must be from mean to be outlier
tolerance = 4.5;

% Defining Matrix lists from data collected from Data Collection. 
unloaded_matrices = {data_matrix_unloaded1, data_matrix_unloaded2, data_matrix_unloaded3};
loaded_matrices = {data_matrix_loaded1, data_matrix_loaded2, data_matrix_loaded3};

averaged_unloaded_matrix = get_averaged_matrix(unloaded_matrices, num_of_data_points, tolerance);

averaged_loaded_matrix = get_averaged_matrix(loaded_matrices, num_of_data_points, tolerance);

%Show Matrices in Command window

averaged_unloaded_matrix
averaged_loaded_matrix


%% Average test data together, leaving outliers out of calculation

% Number of actual data points collected in each test
num_of_data_points = 11;

% Number of standard deviations data must be from mean to be outlier
tolerance = 4.5;

% Defining Matrix lists from data collected from Data Collection. 

averaged_unloaded_matrix = get_averaged_matrix(unloaded_matrices, num_of_data_points, tolerance);

averaged_loaded_matrix = get_averaged_matrix(loaded_matrices, num_of_data_points, tolerance);

%Show Matrices in Command window

averaged_unloaded_matrix
averaged_loaded_matrix





%% Save Raw Data to Excels files if needed.
% Auto Creates excel file named with model, loaded unloaded or torsion, and
% datetime.

% Data to be saved
matrix_to_save = averaged_loaded_matrix;

% Input model name
model_name = 'line_92';

% Test Type (string that is either loaded, unloaded, or torsion)
test_type = 'loaded';


% Auto Creates excel file named with model, loaded or unloaded, and
% datetime.
t = now;
dateTime = strrep(datestr(t),' ','_');
dateTime = strrep(dateTime,':','-');
fileName = strcat(model_name, '_',  test_type, '_', dateTime, '.xlsx');

save_data_to_excel(matrix_to_save, fileName);

%% Save Matrix Data to Excel File. 
%Pass in Matrix,and filename of excel file, and Matlab will automatically
%populate first four columns with pitch, roll, force1, and force2 data from
%matrix

writematrix("Pitch",fileName,'Sheet',1,'Range', 'A1');
writematrix("Roll",fileName,'Sheet',1,'Range', 'B1');
writematrix("Force1",fileName,'Sheet',1,'Range', 'C1');
writematrix("Force2",fileName,'Sheet',1,'Range', 'D1');

function save_data_to_excel(matrix,fileName)
    for i = 1:size(matrix,1)
        writematrix(matrix(i,1),fileName,'Sheet',1,'Range', strcat('A', num2str(i+1)));
        writematrix(matrix(i,2),fileName,'Sheet',1,'Range', strcat('B', num2str(i+1)));
        writematrix(matrix(i,3),fileName,'Sheet',1,'Range', strcat('C', num2str(i+1)));
        writematrix(matrix(i,4),fileName,'Sheet',1,'Range', strcat('D', num2str(i+1)));
    end
end


%% Averages Matrices together, without includeding outliers in average. 

function output = get_averaged_matrix(matrix_list, num_of_rows, tolerance)
    num_of_matrices = numel(matrix_list);
    counter = 1;
    outliers = {};

    % Find the indices of outliers for all the matrices. 
    for i = 1:num_of_matrices
        matrix = matrix_list{i};
        outliers{counter} = get_outlier_indices(matrix, tolerance);
        counter = counter +1;
    end

    return_matrix = zeros(num_of_rows, 4);

    for i = 1:num_of_rows
        % looping through empty return matrix
        for j = 1:4
            sum = 0;
            count = 0;
            index = [i , j];
            % looping through all matrices to be averaged. 
            for k = 1:num_of_matrices
                matrix = matrix_list{k};
                outlier_indices = outliers{k};
                isOutlier = checkOutliers(outlier_indices, index);
                % if outlier don't include in average. 
                if (isOutlier == true)
                    disp("did not include ");
                    disp(index);
                    disp(" from matrix ");
                    disp(k);
                % Otherwise add to sum. 
                else
                    row = index(1);
                    col = index(2);
                    value = matrix(row, col);
                    sum = sum + value(1);
                    count = count + 1;
                end
            end
            % Insert average into return matrix
            average = sum/count;
            row = index(1);
            col = index(2);
            return_matrix(row, col) = average;
        end
    end
    output = return_matrix;
end

%% Find Outliers, (any number that is more than 3 standard deviations awawy)

%Find the indices of the outliers in a matrix. A outlier is defined as
%anything more than 3 standard deviations away from the mean.

function output =  get_outlier_indices(Matrix, tolerance)
    counter = 1;
    outliers = {};
    for i = 1:2
    column = (Matrix(:, i));
    tolerance_range = std(column)*tolerance;
    m = mean(column);
        for k = 1:numel(column)
            if (abs(column(k) - m) > tolerance_range)
                outliers{counter} = [k,i];
                counter = counter + 1;
            end
        end
    end
    output = (outliers);
end

%% Returns True if tup is in tupleList, false otherwise

function output = checkOutliers(tupleList, tup)
    isInList = false;
    for i = 1:numel(tupleList)
        currentTuple = tupleList{i};
        % Compare each element of the current tuple with the tuple to find
        if all(currentTuple == tup)
            isInList = true;
            break;
        end
    end

    output = isInList;
end