from functions import calculate_angle_between_points, calculate_distance_between_points_in_meters

def default_autonomous(starting_pos_x, starting_pos_y, starting_angle, *args):
    index = 0
    robot_x = starting_pos_x
    robot_y = starting_pos_y
    robot_heading = starting_angle

    for array in args:
        # Calculate the angle and distance to the target point
        target_angle = calculate_angle_between_points(x2=array[0], x1=robot_x, y2=array[1], y1=robot_y, starting_angle=robot_heading)
        target_distance = calculate_distance_between_points_in_meters(x2=array[0], x1=robot_x, y2=array[1], y1=robot_y)
        
        # Print information for debugging or simulation
        print(f"Move {index + 1}:")
        print(f"  Target Angle: {target_angle} degrees")
        print(f"  Target Distance: {target_distance} meters")

        # Update the robot's position and heading
        robot_x = array[0]
        robot_y = array[1]
        robot_heading += target_angle

        index += 1

# Example usage:
# Replace the following values with your actual starting position and angles
starting_pos_x = 0
starting_pos_y = 0
starting_angle = 0

# Call the autonomous function with multiple target points
default_autonomous(
    (1, 0),  # Target point 1
    (0, 1),  # Target point 2
    (-1, 0)  # Target point 3
)

