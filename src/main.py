#region Configuration
from vex import LEFT, RIGHT, FORWARD, MM, PERCENT
from vex import *

# Initialize the robot brain
robot_brain = Brain()

# Robot configuration
left_wheel_front = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
left_wheel_back = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
left_wheel_group = MotorGroup(left_wheel_front, left_wheel_back)

right_wheel_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_wheel_back = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_wheel_group = MotorGroup(right_wheel_front, right_wheel_back)

drivetrain_inertial_sensor = Inertial(Ports.PORT12)
drivetrain_gps_sensor = Gps(Ports.PORT8, 13, 14)
robot_drivetrain = SmartDrive(left_wheel_group, right_wheel_group, drivetrain_inertial_sensor, 219.44, 320, 40, MM, 2)

user_controller = Controller(PRIMARY)
extra_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
shoulder_motor_group_a = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
shoulder_motor_group_b = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
shoulder_motor_group = MotorGroup(shoulder_motor_group_a, shoulder_motor_group_b)

# Wait for rotation sensor to fully initialize
wait(30, MSEC)

def calibrate_drivetrain_inertial_sensor():
    # Calibrate the Drivetrain Inertial Sensor
    sleep(200, MSEC)
    robot_brain.screen.print("Calibrating")
    robot_brain.screen.next_row()
    robot_brain.screen.print("Inertial Sensor")
    drivetrain_inertial_sensor.calibrate()
    while drivetrain_inertial_sensor.is_calibrating():
        sleep(25, MSEC)
    robot_brain.screen.clear_screen()
    robot_brain.screen.set_cursor(1, 1)

def play_robot_sound(sound_name):
    # Helper function to play sounds on the robot
    print("RobotPlaySound:" + sound_name)
    wait(5, MSEC)

# Add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# Clear the console to make sure we don't have the REPL in the console
print("\033[2J")

# Define variables used for controlling motors based on controller inputs
is_shoulder_control_stopped = True
should_stop_drivetrain = False

# Define a task that will handle monitoring inputs from the user controller
def user_controller_input_handler():
    global should_stop_drivetrain, is_shoulder_control_stopped, remote_control_enabled
    # Process the controller input every 20 milliseconds
    # Update the motors based on the input values
    while True:
        if remote_control_enabled:
            # Stop the motors if the brain is calibrating the drivetrain inertial sensor
            if drivetrain_inertial_sensor.is_calibrating():
                left_wheel_group.stop()
                right_wheel_group.stop()
                while drivetrain_inertial_sensor.is_calibrating():
                    sleep(25, MSEC)

            # Calculate the drivetrain motor velocities from the controller joystick axes
            # left = axis3 + axis4
            # right = axis3 - axis4
            left_wheel_speed = user_controller.axis3.position() + user_controller.axis4.position()
            right_wheel_speed = user_controller.axis3.position() - user_controller.axis4.position()

            # Check if the values are inside the deadband range
            if abs(left_wheel_speed) < 5 and abs(right_wheel_speed) < 5:
                # Check if the motors have already been stopped
                if should_stop_drivetrain:
                    # Stop the drive motors
                    left_wheel_group.stop()
                    right_wheel_group.stop()
                    # Set the flag to indicate that the motors have been stopped
                    should_stop_drivetrain = False
            else:
                # Reset the flag so that the deadband code knows to stop the motors next
                # time the input is in the deadband range
                should_stop_drivetrain = True

            # Only tell the left drive motor to spin if the values are not in the deadband range
            if should_stop_drivetrain:
                left_wheel_group.set_velocity(left_wheel_speed, PERCENT)
                left_wheel_group.spin(FORWARD)
            # Only tell the right drive motor to spin if the values are not in the deadband range
            if should_stop_drivetrain:
                right_wheel_group.set_velocity(right_wheel_speed, PERCENT)
                right_wheel_group.spin(FORWARD)

            # Check the buttonL1/buttonL2 status to control extra_motor
            if user_controller.buttonL1.pressing():
                extra_motor.spin(FORWARD)
                is_shoulder_control_stopped = False
            elif user_controller.buttonL2.pressing():
                extra_motor.spin(REVERSE)
                is_shoulder_control_stopped = False
            elif not is_shoulder_control_stopped:
                extra_motor.stop()
                # Set the flag so that we don't constantly tell the motor to stop when
                # the buttons are released
                is_shoulder_control_stopped = True

        # Wait before repeating the process
        wait(20, MSEC)

# Define variable for enabling/disabling remote controller control
remote_control_enabled = True

# Create a thread for handling user controller input
user_controller_input_thread = Thread(user_controller_input_handler)


#endregion Configuration

# ------------------------------------------
# 
# 	Project: 7882-z
#	Author: The 7882-Z Crew
#	Created: September ?, 2023
#	Configuration: Idk
# 
# ------------------------------------------

# Library imports
from vex import *

# Defines Methods
import math

def calculate_angle_between_points(x2: int, x1: int, y2: int, y1: int, starting_angle: float):

    delta_of_x = x2 - x1
    delta_of_y = y2 - y1

    angle_to_turn_in_radians = math.atan2(delta_of_y, delta_of_x) - math.radians(starting_angle)

    make_angle_to_turns_result_in_range = (angle_to_turn_in_radians + math.pi) % (2 * math.pi) - math.pi

    convert_in_range_angle_to_degrees = math.degrees(make_angle_to_turns_result_in_range)

    return convert_in_range_angle_to_degrees


def calculate_distance_between_points_in_meters(x2: int, x1: int, y2: int, y1: int):

    delta_of_x = x2 - x1
    delta_of_y = y2 - y1

    distance_between_points_in_ft = math.sqrt((delta_of_x**2) + (delta_of_y**2)) * 2

    return distance_between_points_in_ft


def determine_starting_point(x: int, y: int):

    starting_point = "err: Starting position unable to be determined"

    if x < 0 and y < 0 :
        starting_point = "blue_offensive_red_team"
        robot_brain.screen.print("blue_offensive_red_team")
    elif x > 0 and y < 0:
        starting_point = "red_offensive_red_team"
        robot_brain.screen.print("red_offensive_red_team")
    elif x < 0 and y > 0:
        starting_point = "blue_offensive_blue_team"
        robot_brain.screen.print("blue_offensive_blue_team")
    elif x > 0 and y > 0:
        starting_point = "red_offensive_blue_team"
        robot_brain.screen.print("red_offensive_blue_team")
    else:
        starting_point = "move_bot"
        robot_brain.screen.print("move_bot")
    return starting_point



# Initialize veriables
starting_pos_x = 0
starting_pos_y = 0
starting_angle = 0

def pre_autonomous():
    global starting_pos_x, starting_pos_y, starting_angle
    
    drivetrain_inertial_sensor.calibrate()
    # Assuming drivetrain_gps_sensor has been initialized before calling this function
    starting_pos_x = drivetrain_gps_sensor.x_position(MM) * 1000
    starting_pos_y = drivetrain_gps_sensor.y_position(MM) * 1000


pre_autonomous()

starting_pos = determine_starting_point(starting_pos_x, starting_pos_y)
    
#region Autonomous
def default_autonomous(*args):
    index = 0
    robot_drivetrain.set_drive_velocity(25, PERCENT)
    for array in args:
        target_angle = calculate_angle_between_points(x2=array[0], x1=starting_pos_x, y2=array[1], y1=starting_pos_y, starting_angle=starting_angle)
        target_distance = calculate_distance_between_points_in_meters(x2=array[0], x1=starting_pos_x, y2=array[1], y1=starting_pos_y)
        robot_brain.screen.print(target_angle)
        robot_brain.screen.new_line()
        robot_brain.screen.print(drivetrain_inertial_sensor.heading())
        robot_drivetrain.turn_to_heading(drivetrain_inertial_sensor.heading() + target_angle, DEGREES)
        robot_drivetrain.drive_for(FORWARD, target_distance / 1000, MM)
        index += 1

    
def red_offensive_red_team_autonomous():
    pass

def red_offensive_blue_team_autonomous():
    pass

def blue_offensive_red_team_autonomous():
    pass

def blue_offensive_blue_team_autonomous():
    pass

#endregion

def user_control(): 
    robot_brain.screen.new_line()
    robot_brain.screen.print("Driver control enabled")
    robot_drivetrain.set_drive_velocity(100, PERCENT)
    extra_motor.set_velocity(100, PERCENT)


# Competition Instances

# if starting_pos == "blue_offensive_red_team":
#     # comp = Competition(user_control, blue_offensive_red_team_autonomous)
#     comp = Competition(user_control, default_autonomous) 
# elif starting_pos == "blue_offensive_blue_team":
#     # comp = Competition(user_control, blue_offensive_blue_team_autonomous)
#     comp = Competition(user_control, default_autonomous)
# elif starting_pos == "red_offensive_red_team":
#     # comp = Competition(user_control, red_offensive_red_team_autonomous)
#     comp = Competition(user_control, default_autonomous)
# elif starting_pos == "red_offensive_blue_team":
#     # comp = Competition(user_control, red_offensive_blue_team_autonomous)
#     comp = Competition(user_control, default_autonomous)
# else:
#     comp = Competition(user_control, default_autonomous)

comp = Competition(user_control, default_autonomous([0, 0]))