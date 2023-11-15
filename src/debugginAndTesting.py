from functions import calculate_angle_between_points, calculate_distance_between_points_in_meters

starting_pos_x = 1.0
starting_pos_y = 0.5
starting_angle = 0

def default_autonomous(*args):
    global starting_pos_x, starting_pos_y, starting_angle
    for index, array in enumerate(args, start=0):
        print(calculate_angle_between_points(x2=array[0], x1=starting_pos_x, y2=array[1], y1=starting_pos_y, starting_angle=starting_angle))
        print(calculate_distance_between_points_in_meters(x2=array[0], x1=starting_pos_x, y2=array[1], y1=starting_pos_y))

array1 = [0.1, -.8]
array2 = [.8, 1]
array3 = [1, 1]

default_autonomous(array1, array2, array3)

