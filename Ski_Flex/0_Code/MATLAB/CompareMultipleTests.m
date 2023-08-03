
%%
clc
clear
close all
%% Load Data
relative_dir_path = strcat('G:\.shortcut-targets-by-id\1jaXuO8culNZtbUZ1rrY8TEjG_TDjo2f5\Blister Labs Ski Flex\Ski_Data\');
contents = dir(relative_dir_path);

% Initialize an empty cell array to store the directories
directories = {};

% Loop through the contents and filter out only the directories
for i = 1:length(contents)
    if contents(i).isdir && ~strcmp(contents(i).name, '.') && ~strcmp(contents(i).name, '..')
        directories = [directories; contents(i).name];
    end
end

% Display the list of directories
disp(directories);
%% Select Data
ski_to_analyze = "line_sickday_2016_181cm_114mm";
relative_dir_path = strcat('G:\.shortcut-targets-by-id\1jaXuO8culNZtbUZ1rrY8TEjG_TDjo2f5\Blister Labs Ski Flex\Ski_Data\', ski_to_analyze);
data_to_retrieve = [6,7,8,9,10];
existing_dirs = check_subdirectories(relative_dir_path, data_to_retrieve)

%% load data
files = existing_dirs;
n = size(files,1);
for i = 1:n
    loadfile = importdata(files(i,:));
    testData(:,i) = loadfile.data(:,2);
end
N = length(testData);
 for i = 1:N
    testAvg(i,:) = mean(rmoutliers(testData(i,:)));
end
figure
hold on
plot(testAvg)
title('Average EI data');
hold off
%% put to 1-10 scale

binMat = zeros(1,5);
binMatScale = zeros(1,5);
%EI = importdata('EI_points.csv').data(:,2);
EI = testAvg;
n = (length(EI)/5);
BlisterSegments = zeros(1,5);
for i = 1:5
    start = round(1+(i-1)*n);
    stop = round(i*n);
    segment = EI(start:stop);
    binMat(i) = mean(segment);
    binMatScale(i) = scaleMe(binMat(i));
    BlisterSegments(i) = binMatScale(i);
end
Tip = BlisterSegments(1);
Shovel = BlisterSegments(2);
Underfoot = BlisterSegments(3);
Heel = BlisterSegments(4);
Tail = BlisterSegments(5);
BlisterRank = table(Tip,Shovel,Underfoot,Heel,Tail);
disp(BlisterRank)
function value = scaleMe(EI)
    value = floor(EI/44.575)*.5+4;
end



%%

function existing_dirs = check_subdirectories(parent_dir, numbers_list)
    % Initialize an empty cell array to store the existing directories
    existing_dirs = {};

    % Loop through the numbers_list and check for the existence of corresponding subdirectories
    for i = 1:length(numbers_list)
        sub_dir_name = fullfile(parent_dir, [num2str(numbers_list(i)), '_test']);
        
        % Use the isfolder function to check if the subdirectory exists
        if isfolder(sub_dir_name)
            existing_dirs = [existing_dirs; strcat(sub_dir_name,"\EI_points.csv")];
        else
            error(['Subdirectory "', sub_dir_name, '" does not exist. Please make sure the test numbers entered into data_to_retrieve all exist']);
        end
    end
end
