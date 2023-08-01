This folder contains all the python scripts that compute the radial deformation of a rim for the dynamic drop test. These also have energy calculations.

If you do more testing you need to change a few things for it to run.

In readInDataFiles.py in the process_single_file function you need to change the number of '_' to fit your file format.
So if my file format looks like this "C:\Users\ethan\Test\Energy_Testing\Light_Flat\Dynamic_MOCAP_LightEN928_7-17-23_Energy_Height17_Trial2_Flat.csv" 
in this case if you want the Height17 it would be 7 underscores.
4 for LightEN928 and 9 for the drop head "Flat".
change accoringly if you want the graph labeling to work correctly.

We also used a rigid body of the wheel so we could name the markers for easier coding. I would suggest doing this and calling the rigidbody "RigidBody" and labeling the top of the rim marker "0deg" and "Hub". If you call it something else it will need to be added to dtypes.py.
The drop head marker should be the only marker in the system unlabeled.

The code also does not handle bad files. So if a file has too many columns or not correctly name files it will error out. Would be nice to add in the future.
