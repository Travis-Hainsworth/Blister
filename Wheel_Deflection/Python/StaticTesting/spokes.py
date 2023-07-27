from graphFunctions import *

lateral_deviation = spoke_data(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\lateral_deviation.csv")

lateral_deviation['Rim'] = ['ENVE AM30',
                            'Stans Flow MK4',
                            'Light EN928',
                            'Reserve 30HD',
                            'We Are One Union'
                            ]

lateral_deviation_plot(lateral_deviation, 6)

rims = ['ENVE AM30',
        'Stans Flow MK4',
        'Light EN928',
        'Reserve 30HD',
        'We Are One Union'
        ]
data_list = [
    pd.read_csv(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\spoke_tension_enve.csv"),
    pd.read_csv(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\spoke_tension_stans.csv"),
    pd.read_csv(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\spoke_tension_light.csv"),
    pd.read_csv(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\spoke_tension_r30.csv"),
    pd.read_csv(r"C:\Users\ethan\Test\Static_New_Data\spoke_data\spoke_tension_waou.csv"),
]

target_list = [100, 130, 120, 115, 115]
spoke_tension_plot(data_list, target_list, rims)

