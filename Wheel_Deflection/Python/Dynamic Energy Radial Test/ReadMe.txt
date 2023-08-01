This folder contains all the python scripts that compute the radial deformation of a rim for the dynamic drop test. These also have energy calculations.

You need to change a few things for it to run.

In readInDataFiles.py in the process_single_file function you need to change the number of '_' to fit your file format.
So if my file format looks like this "C:\Users\ethan\Test\Energy_Testing\Light_Flat\Dynamic_MOCAP_LightEN928_7-17-23_Energy_Height17_Trial2_Flat.csv" you need to 
count the number of '_' and change accoringly if you want the graph labeling to work correctly.

We also used a rigid body so we could name the markers for easier coding. I would suggest doing this and calling the rigidbody "RigidBody". If you call it something
else it will need to be added to dtypes.py.

The code also does not handle bad files. So if a file has too many columns or not correctly name files it will error out. Would be nice to add in the future.
