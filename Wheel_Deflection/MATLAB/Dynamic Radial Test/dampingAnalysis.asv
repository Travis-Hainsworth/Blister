%Josh Priest
%V1
%06/26/2023
%Dynamic Test Analysis

data = readmatrix("/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/MATLAB/Dynamic Radial Test/Dynamic_MOCAP_StansFlowMK4_6-26-23_780kgf_Trial3.csv");

% Remove the top 5 rows which correspond to the CSV's header
data = data(8:end,:);
%finds original positions of stand and rim markers, save data into new
%arrays, if statements fins the correct marker index for rim and stand
[temp,m] = max(data(1,[4 7 10]));
if m == 1
    m = 4;
elseif m == 2
    m = 7;
else
    m = 10;
end
[~,o] = min(data(1,[4 7 10]));
if o == 1
    o = 4;
elseif o == 2
    o = 7;
else
    o = 10;
end

stand_0 = data(1,o-1:o+1);
stand = data(:,o-1:o+1);
rim_0 = data(1,m-1:m+1);
rim = data(:,m-1:m+1);

%finds original distance between the stand and rim markers
l_0 = rim_0 - stand_0;
[index, ~] = size(data);
realDisp = zeros(index,3);

%first finds the distance between the stand and rim for each point in time
%and subtracts the original distance to filter out noise from the stand
%moving due to the carrige and piston catch
for i = 1:index

    l = rim(i,:) - stand(i,:);
    realDisp(i,:) = l_0 - l;
    
end

%allows for quick indexing for later use
[maxDef,k] = max(realDisp(:,2));
[minDef,u] = min(abs(realDisp(k:end,2)));

%plots y displacement
figure(1)
hold on
plot(data(:,2),realDisp(:,2))
title('Y Displacement of Rim')
xlabel('Time (sec)')
ylabel('Displacement (mm)')
plot(data(k,2),realDisp(k,2),'r.','MarkerSize',18)
place = sprintf('Max: %fmm',maxDef);
legend('Deflection',place,'Location','northeast')
hold off

%FFT analysis, finds natural frequency of rim
L = index-k+1;
Y = fft(realDisp(k+1:end,2));
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
Fs = 500;
f = Fs*(0:(L/2))/L;
figure(2)
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of Displacement(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')

%solves for time from impact to oscilating within 2% of stationary value
timeToNormalize = settlingtime(realDisp(k:end,2),Fs,2);
disp('Setting Time For Rim:')
disp(timeToNormalize)