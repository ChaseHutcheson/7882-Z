import math

def calculate_angle_between_points(x2: int, x1: int, y2: int, y1: int, starting_angle: int):

    delta_of_x = x2 - x1
    delta_of_y = y2 - y1

    angle_to_turn_in_radians = math.atan2(delta_of_y, delta_of_x) - math.radians(starting_angle)

    make_angle_to_turns_result_in_range = (angle_to_turn_in_radians + math.pi) % (2 * math.pi) - math.pi

    convert_in_range_angle_to_degrees = math.degrees(make_angle_to_turns_result_in_range)

    return convert_in_range_angle_to_degrees


def calculate_distance_between_points_in_ft(x2: int, x1: int, y2: int, y1: int):

    delta_of_x = x2 - x1
    delta_of_y = y2 - y1

    distance_between_points_in_ft = math.sqrt((delta_of_x**2) + (delta_of_y**2)) * 2

    return distance_between_points_in_ft


def determine_starting_point(x, y):

    starting_point = "err: Starting position unable to be determined"

    if x < 3 and y < 3:
        starting_point = "blue_offensive_red_team"
    elif x > 3 and y < 3:
        starting_point = "red_offensive_red_team"
    elif x < 3 and y > 3:
        starting_point = "blue_offensive_blue_team"
    elif x < 3 and y > 3:
        starting_point = "red_offensive_blue_team"
    else:
        starting_point = "move_bot"
    return starting_point

