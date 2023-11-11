#region Configuration
from vex import *
from functions import *

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
drivetrain_gps_sensor = Gps(Ports.PORT15, 13, 14)
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


#endregion VEXcode Generated Robot Configuration

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

# Begin project code

brain = Brain()

# Initialize veriables
starting_pos_x = 0
starting_pos_y = 0

def pre_autonomous():
    global starting_pos_x, starting_pos_y
    
    # Assuming drivetrain_gps_sensor has been initialized before calling this function
    starting_pos_x = drivetrain_gps_sensor.x_position(INCHES) * 12
    starting_pos_y = drivetrain_gps_sensor.y_position(INCHES) * 12

    
#region Autonomous
def default_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    robot_drivetrain.set_drive_velocity(50, PERCENT)
    extra_motor.set_velocity(100, PERCENT)
    extra_motor.spin_for(FORWARD, 270, DEGREES)
    robot_drivetrain.drive_for(FORWARD, 55, INCHES)
    extra_motor.spin_for(REVERSE, 270, DEGREES)
    robot_drivetrain.set_drive_velocity(100, PERCENT)
    robot_drivetrain.drive_for(FORWARD, 15, INCHES)

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
    brain.screen.clear_screen()
    # place driver control in this while loop
    robot_drivetrain.set_drive_velocity(100, PERCENT)
    extra_motor.set_velocity(100, PERCENT)


# Competition Instances

pre_autonomous()

starting_pos = determine_starting_point(starting_pos_x, starting_pos_y)

if starting_pos == "blue_offensive_red_team":
    comp = Competition(user_control, blue_offensive_red_team_autonomous) 
elif starting_pos == "blue_offensive_blue_team":
    comp = Competition(user_control, blue_offensive_blue_team_autonomous)
elif starting_pos == "red_offensive_red_team":
    comp = Competition(user_control, red_offensive_red_team_autonomous)
elif starting_pos == "red_offensive_blue_team":
    comp = Competition(user_control, red_offensive_blue_team_autonomous)
else:
    comp = Competition(user_control, default_autonomous)