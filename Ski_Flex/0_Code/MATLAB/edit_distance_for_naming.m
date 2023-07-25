
disp(editDistance("test_name_1_9579234", "test_name_1_4619834"));
%%
clc;
global dic;
exist = {"test_name__4579234", "test_name__4579234777", "trest_name_3_94301924847ud0000000000000000000000000000000000000000000000000000000", "test_name_4_ fkjghjsdh354555555555555555555555555555555555555544454"};
name = "test_name__4579234";
arr = check_for_similar_test_names(name, exist);
disp(dic)

%%

% function closest_test_names = check_for_similar_test_names(inputed_test_name, existing_test_names)
%     %intialize dictionary d with key = string, value = double
%     %loop through each existing_name in exisiting_test_names
%         %dis = editDistance(inputed_test_name, existing_name)
%         %d[existing_name] = dis
%     %order dicitionary by value in desending order
%     %closest_test_names = get all dictionary keys that have a value greater than .7 
% end

function closest_test_names = check_for_similar_test_names(inputed_test_name, existing_test_names)
    % Initialize dictionary d with key = string, value = double
    d = dictionary;%containers.Map('KeyType', 'char', 'ValueType', 'double');%

    % Loop through each existing_name in existing_test_names
    for i = 1:length(existing_test_names)
        existing_name = existing_test_names{i};
        
        % Calculate the edit distance between inputed_test_name and existing_name
        dis = editDistance(inputed_test_name, existing_name);
        
        % Store the edit distance in the dictionary
        big = max(strlength(inputed_test_name), strlength(existing_name));
        dist = dis/big;
        d(existing_name) = dist;
    end
     
    % Order the dictionary by value in descending order
    global dic;
    sorted_d = sortDictByValue(d, 'ascend');
    dic = sorted_d;

  % Get all dictionary keys that have a value greater than 0.7
    closest_test_names = {};
    keys_sorted = keys(sorted_d);
    for i = 1:length(keys_sorted)
        key = keys_sorted{i};
        value = sorted_d(key);
        if value < 0.15
            closest_test_names{end+1} = key;
        end
    end
end


function sortedDict = sortDictByValue(dict, sortOrder)
    % Function to sort a dictionary by value in ascending or descending order
    dictKeys = keys(dict);
    dictValues = values(dict);
    
    % Sort the dictionary values and get the corresponding indices
    [~, sortedIndices] = sort([dictValues(:)], sortOrder);
    
    % Reorder the dictionary keys based on the sorted indices
    sortedDictKeys = dictKeys(sortedIndices);
    sortedDictValues = dictValues(sortedIndices);
    
    % Create a new dictionary with the sorted keys and values
    sortedDict = dictionary(sortedDictKeys, sortedDictValues);%containers.Map(sortedDictKeys, sortedDictValues);%
end

function distance = manhattan_distance(str1, str2)
   if numel(str1) ~= numel(str2)
        error('Input strings must have the same length.');
    end

    ascii_str1 = double(str1);
    disp(ascii_str1)
    ascii_str2 = double(str2);
    disp(ascii_str2)

    distance = sum(abs(ascii_str1 - ascii_str2));
end