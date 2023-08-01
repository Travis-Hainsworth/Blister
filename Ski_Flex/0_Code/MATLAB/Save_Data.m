x = [1,2,3,4,5,6];
y = [6,5,4,3,2,1];
tiledlayout(2,1);

nexttile;
plot(x,y);
title('EJ');

nexttile;
plot(x,x);
title('GJ');

data_matrix
%%
model_name = 'line_92';      % Input model name
year = 2020;                 % Input model yearclc
manufacturer = "K2";         % Input ski Manufacturer
model_length_cm = 197;       % Input Length of ski in cm
test_interval_mm = 25;       % Input the desired distance between data points in mm (multiples of 5 work best)
test_type = 'loaded';        % Test Type (string that is either loaded, unloaded, or torsion)

dir_name = "K2_Line93_2020_197cm";
%%

saveData(data_matrix, gcf, dir_name)

%%
function saveData(data_matrix, plot, dir_name)

    relative_dir_path = strcat('..\..\0_Data\',dir_name);

    if ~exist(relative_dir_path, 'dir')
       mkdir(relative_dir_path);
    end

    S = dir(relative_dir_path);
    N = nnz(~ismember({S.name},{'.','..'})&[S.isdir]);
    test_dir_name = strcat(num2str(N),"_test");
    relative_save_path = strcat(relative_dir_path,'\',test_dir_name);

    mkdir(relative_save_path);

    saveas(plot,strcat(relative_save_path, "\plots.png"));



    
end