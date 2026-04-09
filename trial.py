import time
from adafruit_servokit import ServoKit
import keyboard
from climb import climb_stair

# Initialize ServoKit instances for two PCA9685 boards
board1 = ServoKit(channels=16, address=0x40)
board2 = ServoKit(channels=16, address=0x41)


# Define servo pins for each leg
LEG_SERVOS = {
    "right1": {"coxa": 9, "femur": 8, "tibia": 7},
    "right2": {"coxa": 12, "femur": 11, "tibia": 10},
    "right3": {"coxa": 15, "femur": 14, "tibia": 13},
    "left1": {"coxa": 15, "femur": 14, "tibia": 13},
    "left2": {"coxa": 12, "femur": 11, "tibia": 10},
    "left3": {"coxa": 9, "femur": 8, "tibia": 7},
}

# Constants for custom servo pulse range (for first 4 motors)
CUSTOM_SERVOMIN = 550  # Custom minimum pulse length
CUSTOM_SERVOMAX = 2400  # Custom maximum pulse length


# Function to map angle (0-180) to pulse width (125-575)
def angle_to_pulse(angle, min_pulse, max_pulse):
    pulse = min_pulse + (angle * (max_pulse - min_pulse) // 180)
    return pulse


# Function to set servo angle
def set_servo_angle(leg, joint, angle):
    # Validate angle range
    if angle < 0 or angle > 180:
        raise ValueError(f"Angle must be between 0 and 180 degrees. Got: {angle}")

    # Select the correct board
    if leg in ["right1", "right2", "right3"]:
        board = board1
    else:
        board = board2

    pin = LEG_SERVOS[leg][joint]

    try:
        # Set the pulse width range
        #         board.servo[pin].set_pulse_width_range(CUSTOM_SERVOMIN, CUSTOM_SERVOMAX)
        # Use the correct board variable here (was using board1 always)
        board.servo[pin].angle = angle
    except Exception as e:
        print(f"Error setting servo angle for {leg} {joint}: {e}")


# Initialize movement variables
FM1 = FM2 = FM3 = FM4 = FM5 = FM6 = FM7 = FM8 = 0
Impair_start = False


# Stand position
def up_pos():
    set_servo_angle("right1", "coxa", 100)
    set_servo_angle("right1", "femur", 100)  # + = +
    set_servo_angle("right1", "tibia", 90)  # + = -

    set_servo_angle("right2", "coxa", 95)
    set_servo_angle("right2", "femur", 110)
    set_servo_angle("right2", "tibia", 90)

    set_servo_angle("right3", "coxa", 90)
    set_servo_angle("right3", "femur", 95)
    set_servo_angle("right3", "tibia", 90)

    set_servo_angle("left1", "coxa", 95)
    set_servo_angle("left1", "femur", 85)
    set_servo_angle("left1", "tibia", 90)

    set_servo_angle("left2", "coxa", 90)
    set_servo_angle("left2", "femur", 85)
    set_servo_angle("left2", "tibia", 110)

    set_servo_angle("left3", "coxa", 90)
    set_servo_angle("left3", "femur", 95)
    set_servo_angle("left3", "tibia", 90)


def stand_pos():
    set_servo_angle("right1", "coxa", 100)
    set_servo_angle("right1", "femur", 145)  # + = +
    set_servo_angle("right1", "tibia", 140)  # + = -

    set_servo_angle("right2", "coxa", 95)
    set_servo_angle("right2", "femur", 140)
    set_servo_angle("right2", "tibia", 125)

    set_servo_angle("right3", "coxa", 90)
    set_servo_angle("right3", "femur", 135)
    set_servo_angle("right3", "tibia", 150)

    set_servo_angle("left1", "coxa", 95)
    set_servo_angle("left1", "femur", 135)
    set_servo_angle("left1", "tibia", 140)

    set_servo_angle("left2", "coxa", 90)
    set_servo_angle("left2", "femur", 125)
    set_servo_angle("left2", "tibia", 150)

    set_servo_angle("left3", "coxa", 90)
    set_servo_angle("left3", "femur", 140)
    set_servo_angle("left3", "tibia", 145)


# Move forward function


def move_forward():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle("right1", "tibia", 140 - FM1 * 2)
        set_servo_angle("right1", "femur", 145 + FM1 * 3)

        set_servo_angle("right3", "tibia", 150 - FM1 * 2)
        set_servo_angle("right3", "femur", 135 + FM1 * 3)

        set_servo_angle("left2", "tibia", 150 - FM1 * 2)
        set_servo_angle("left2", "femur", 125 + FM1 * 3)
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle("right1", "coxa", 100 + FM2)

        set_servo_angle("right3", "coxa", 90 + FM2)

        set_servo_angle("left2", "coxa", 90 - FM2)
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle("right1", "tibia", 120 + FM3 * 2)
        set_servo_angle("right1", "femur", 175 - FM3 * 3)

        set_servo_angle("right3", "tibia", 130 + FM3 * 2)
        set_servo_angle("right3", "femur", 165 - FM3 * 3)

        set_servo_angle("left2", "tibia", 130 + FM3 * 2)
        set_servo_angle("left2", "femur", 155 - FM3 * 3)
        FM3 += 1

    if FM2 >= 40:
        set_servo_angle("right1", "coxa", 140 - FM4)
        set_servo_angle("right3", "coxa", 130 - FM4)
        set_servo_angle("left2", "coxa", 50 + FM4)
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle("right2", "tibia", 125 - FM5 * 2)
            set_servo_angle("right2", "femur", 140 + FM5 * 3)

            set_servo_angle("left1", "tibia", 140 - FM5 * 2)
            set_servo_angle("left1", "femur", 135 + FM5 * 3)

            set_servo_angle("left3", "tibia", 145 - FM5 * 2)
            set_servo_angle("left3", "femur", 140 + FM5 * 3)
            FM5 += 1

        if FM6 <= 40:
            set_servo_angle("right2", "coxa", 95 + FM6)
            set_servo_angle("left1", "coxa", 95 - FM6)
            set_servo_angle("left3", "coxa", 90 - FM6)
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle("right2", "tibia", 105 + FM7 * 2)
            set_servo_angle("right2", "femur", 170 - FM7 * 3)

            set_servo_angle("left1", "tibia", 120 + FM7 * 2)
            set_servo_angle("left1", "femur", 165 - FM7 * 3)

            set_servo_angle("left3", "tibia", 125 + FM7 * 2)
            set_servo_angle("left3", "femur", 170 - FM7 * 3)
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle("right2", "coxa", 135 - FM8)
            set_servo_angle("left1", "coxa", 55 + FM8)
            set_servo_angle("left3", "coxa", 50 + FM8)
            FM8 += 1

        if FM8 >= 40:
            Impair_start = False
            FM5 = FM6 = FM7 = FM8 = 0


def move_backward():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle("right1", "tibia", 140 - FM1 * 2)
        set_servo_angle("right1", "femur", 145 + FM1 * 3)

        set_servo_angle("right3", "tibia", 150 - FM1 * 2)
        set_servo_angle("right3", "femur", 135 + FM1 * 3)

        set_servo_angle("left2", "tibia", 150 - FM1 * 2)
        set_servo_angle("left2", "femur", 125 + FM1 * 3)
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle("right1", "coxa", 100 - FM2)

        set_servo_angle("right3", "coxa", 90 - FM2)

        set_servo_angle("left2", "coxa", 90 + FM2)
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle("right1", "tibia", 120 + FM3 * 2)
        set_servo_angle("right1", "femur", 175 - FM3 * 3)

        set_servo_angle("right3", "tibia", 130 + FM3 * 2)
        set_servo_angle("right3", "femur", 165 - FM3 * 3)

        set_servo_angle("left2", "tibia", 130 + FM3 * 2)
        set_servo_angle("left2", "femur", 155 - FM3 * 3)
        FM3 += 1

    if FM2 >= 40:
        set_servo_angle("right1", "coxa", 140 + FM4)
        set_servo_angle("right3", "coxa", 130 + FM4)
        set_servo_angle("left2", "coxa", 50 - FM4)
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle("right2", "tibia", 125 - FM5 * 2)
            set_servo_angle("right2", "femur", 140 + FM5 * 3)

            set_servo_angle("left1", "tibia", 140 - FM5 * 2)
            set_servo_angle("left1", "femur", 135 + FM5 * 3)

            set_servo_angle("left3", "tibia", 145 - FM5 * 2)
            set_servo_angle("left3", "femur", 140 + FM5 * 3)
            FM5 += 1

        if FM6 <= 40:
            set_servo_angle("right2", "coxa", 95 - FM6)
            set_servo_angle("left1", "coxa", 95 + FM6)
            set_servo_angle("left3", "coxa", 90 + FM6)
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle("right2", "tibia", 105 + FM7 * 2)
            set_servo_angle("right2", "femur", 170 - FM7 * 3)

            set_servo_angle("left1", "tibia", 120 + FM7 * 2)
            set_servo_angle("left1", "femur", 165 - FM7 * 3)

            set_servo_angle("left3", "tibia", 125 + FM7 * 2)
            set_servo_angle("left3", "femur", 170 - FM7 * 3)
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle("right2", "coxa", 135 + FM8)
            set_servo_angle("left1", "coxa", 55 - FM8)
            set_servo_angle("left3", "coxa", 50 - FM8)
            FM8 += 1

        if FM8 >= 40:
            Impair_start = False
            FM5 = FM6 = FM7 = FM8 = 0


def rotate_right():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle("right1", "tibia", 140 - FM1 * 2)
        set_servo_angle("right1", "femur", 145 + FM1 * 3)

        set_servo_angle("right3", "tibia", 150 - FM1 * 2)
        set_servo_angle("right3", "femur", 135 + FM1 * 3)

        set_servo_angle("left2", "tibia", 150 - FM1 * 2)
        set_servo_angle("left2", "femur", 125 + FM1 * 3)
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle("right1", "coxa", 100 - FM2)

        set_servo_angle("right3", "coxa", 90 - FM2)

        set_servo_angle("left2", "coxa", 90 - FM2)
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle("right1", "tibia", 120 + FM3 * 2)
        set_servo_angle("right1", "femur", 175 - FM3 * 3)

        set_servo_angle("right3", "tibia", 130 + FM3 * 2)
        set_servo_angle("right3", "femur", 165 - FM3 * 3)

        set_servo_angle("left2", "tibia", 130 + FM3 * 2)
        set_servo_angle("left2", "femur", 155 - FM3 * 3)
        FM3 += 1

    if FM2 >= 40:
        set_servo_angle("right1", "coxa", 140 + FM4)
        set_servo_angle("right3", "coxa", 130 + FM4)
        set_servo_angle("left2", "coxa", 50 + FM4)
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle("right2", "tibia", 125 - FM5 * 2)
            set_servo_angle("right2", "femur", 140 + FM5 * 3)

            set_servo_angle("left1", "tibia", 140 - FM5 * 2)
            set_servo_angle("left1", "femur", 135 + FM5 * 3)

            set_servo_angle("left3", "tibia", 145 - FM5 * 2)
            set_servo_angle("left3", "femur", 140 + FM5 * 3)
            FM5 += 1

        if FM6 <= 40:
            set_servo_angle("right2", "coxa", 95 - FM6)
            set_servo_angle("left1", "coxa", 95 - FM6)
            set_servo_angle("left3", "coxa", 90 - FM6)
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle("right2", "tibia", 105 + FM7 * 2)
            set_servo_angle("right2", "femur", 170 - FM7 * 3)

            set_servo_angle("left1", "tibia", 120 + FM7 * 2)
            set_servo_angle("left1", "femur", 165 - FM7 * 3)

            set_servo_angle("left3", "tibia", 125 + FM7 * 2)
            set_servo_angle("left3", "femur", 170 - FM7 * 3)
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle("right2", "coxa", 135 + FM8)
            set_servo_angle("left1", "coxa", 55 + FM8)
            set_servo_angle("left3", "coxa", 50 + FM8)
            FM8 += 1

        if FM8 >= 40:
            Impair_start = False
            FM5 = FM6 = FM7 = FM8 = 0


def rotate_left():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle("right1", "tibia", 140 - FM1 * 2)
        set_servo_angle("right1", "femur", 145 + FM1 * 3)

        set_servo_angle("right3", "tibia", 150 - FM1 * 2)
        set_servo_angle("right3", "femur", 135 + FM1 * 3)

        set_servo_angle("left2", "tibia", 150 - FM1 * 2)
        set_servo_angle("left2", "femur", 125 + FM1 * 3)
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle("right1", "coxa", 100 + FM2)

        set_servo_angle("right3", "coxa", 90 + FM2)

        set_servo_angle("left2", "coxa", 90 + FM2)
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle("right1", "tibia", 120 + FM3 * 2)
        set_servo_angle("right1", "femur", 175 - FM3 * 3)

        set_servo_angle("right3", "tibia", 130 + FM3 * 2)
        set_servo_angle("right3", "femur", 165 - FM3 * 3)

        set_servo_angle("left2", "tibia", 130 + FM3 * 2)
        set_servo_angle("left2", "femur", 155 - FM3 * 3)
        FM3 += 1

    if FM2 >= 40:
        set_servo_angle("right1", "coxa", 140 - FM4)
        set_servo_angle("right3", "coxa", 130 - FM4)
        set_servo_angle("left2", "coxa", 50 - FM4)
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle("right2", "tibia", 125 - FM5 * 2)
            set_servo_angle("right2", "femur", 140 + FM5 * 3)

            set_servo_angle("left1", "tibia", 140 - FM5 * 2)
            set_servo_angle("left1", "femur", 135 + FM5 * 3)

            set_servo_angle("left3", "tibia", 145 - FM5 * 2)
            set_servo_angle("left3", "femur", 140 + FM5 * 3)
            FM5 += 1

        if FM6 <= 40:
            set_servo_angle("right2", "coxa", 95 + FM6)
            set_servo_angle("left1", "coxa", 95 + FM6)
            set_servo_angle("left3", "coxa", 90 + FM6)
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle("right2", "tibia", 105 + FM7 * 2)
            set_servo_angle("right2", "femur", 170 - FM7 * 3)

            set_servo_angle("left1", "tibia", 120 + FM7 * 2)
            set_servo_angle("left1", "femur", 165 - FM7 * 3)

            set_servo_angle("left3", "tibia", 125 + FM7 * 2)
            set_servo_angle("left3", "femur", 170 - FM7 * 3)
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle("right2", "coxa", 135 - FM8)
            set_servo_angle("left1", "coxa", 55 - FM8)
            set_servo_angle("left3", "coxa", 50 - FM8)
            FM8 += 1

        if FM8 >= 40:
            Impair_start = False
            FM5 = FM6 = FM7 = FM8 = 0


def display_menu():
    print("\n--- Robot Control Menu ---")
    print("W: Move Forward")
    print("S: Move Backward ")
    print("A: Move Left (not implemented)")
    print("D: Move Right (not implemented)")
    print("Ctrl+S: Set Stand Position")
    print("Ctrl+U: Set Up Position")
    print("Q: Quit the Program")
    print("---------------------------\n")


def main():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    # Display the control menu
    display_menu()

    while True:
        if keyboard.is_pressed("w"):
            move_forward()
        elif keyboard.is_pressed("s"):
            move_backward()  # Implement backward or another movement if necessary
        elif keyboard.is_pressed("a"):
            rotate_left()  # Implement left movement
        elif keyboard.is_pressed("d"):
            rotate_right()  # Implement right movement
        elif keyboard.is_pressed("j"):
            print("Setting Stand Position...")
            stand_pos()
        elif keyboard.is_pressed("k"):
            print("Setting Up Position...")
            up_pos()
        elif keyboard.is_pressed("c"):
            print("climb stairs")
            climb_stair()
        elif keyboard.is_pressed("q"):
            print("Exiting program...")
            break

        time.sleep(0.007)  # Small delay to reduce CPU usage

        time.sleep(0.007)


if __name__ == "__main__":
    stand_pos()
    time.sleep(2)  # Set initial position
    main()
#     stand_pos()
