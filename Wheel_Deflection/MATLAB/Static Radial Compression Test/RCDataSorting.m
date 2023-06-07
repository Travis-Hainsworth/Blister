clc
clear
close all

filePath = '/Users/jacobvogel/Desktop/Blister Labs/GitHub/Blister/Wheel_Deflection/0_Data/DTS 2-10-23 Tire On/';
filePathMocap = strcat(filePath, 'Optitrack Data/DTS700lbf.csv');
filePathMTS = strcat(filePath, 'MTS Data/0DTS700lbf_MTS_2-10.csv');

[mocap, RimTop, Center, I] = cleanMocapData(filePathMocap);
[MTS, MTS_time, MTS_height, MTS_load] = cleanMTSData(filePathMTS);

mocap_synced = syncData(mocap, MTS_time);

[mo_time, m_head, m_rim_top, m_axle] = getUsefulMarkers(mocap_synced, I, RimTop, Center);

radial_compression = calcRadCompression(m_axle, m_rim_top);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Plots %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure
subplot(1,2,1)
plot(MTS_time,radial_compression)
title('Radial Compression')
xlabel('Time')
ylabel('Compression (mm)')

subplot(1,2,2)
plot(MTS_load, radial_compression)
title('Load vs Deflection')
xlabel('Load (lbs)')
ylabel('Compression (mm)')



figure
subplot(1,2,1)
plot(MTS_time, radial_compression*0.0393701)
title('For Greg: Radial Compression')
xlabel('Time')
ylabel('Compression (in)')

subplot(1,2,2)
plot(MTS_load, radial_compression*0.0393701)
title('For Greg: Load vs Deflection')
xlabel('Load (lbs)')
ylabel('Compression (in)')