from functions import *

starting_x = 0
starting_y = 0

def pre_autonomous():
    global starting_x, starting_y
    starting_x = 2
    starting_y = 4
    

    # Assuming drivetrain_gps_sensor has been initialized before calling this function

pre_autonomous()

print(determine_starting_point(starting_x, starting_y))
