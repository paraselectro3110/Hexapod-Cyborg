import time
from adafruit_servokit import ServoKit
import keyboard

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
    """
    Set the servo angle for a specific leg and joint, clamping to valid range (0-180).
    """
    clamped_angle = max(0, min(180, angle))
    if leg in ["right1", "right2", "right3"]:
        board = board1
    else:
        board = board2

    pin = LEG_SERVOS[leg][joint]

    try:
        # Set the servo to the clamped angle
        board.servo[pin].angle = clamped_angle
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


stand_pos_angles = {
    # right legs
    "right1": {"coxa": 100, "femur": 145, "tibia": 140},
    "right2": {"coxa": 95, "femur": 140, "tibia": 125},
    "right3": {"coxa": 90, "femur": 135, "tibia": 150},
    # left legs
    "left1": {"coxa": 95, "femur": 135, "tibia": 140},
    "left2": {"coxa": 90, "femur": 125, "tibia": 150},
    "left3": {"coxa": 90, "femur": 140, "tibia": 145},
}


def stand_pos():
    set_servo_angle("right1", "coxa", stand_pos_angles["right1"]["coxa"])
    set_servo_angle("right1", "femur", stand_pos_angles["right1"]["femur"])  # + = +
    set_servo_angle("right1", "tibia", stand_pos_angles["right1"]["tibia"])  # + = -

    set_servo_angle("right2", "coxa", stand_pos_angles["right2"]["coxa"])
    set_servo_angle("right2", "femur", stand_pos_angles["right2"]["femur"])  # + = +
    set_servo_angle("right2", "tibia", stand_pos_angles["right2"]["tibia"])  # + = -

    set_servo_angle("right3", "coxa", stand_pos_angles["right3"]["coxa"])
    set_servo_angle("right3", "femur", stand_pos_angles["right3"]["femur"])  # + = +
    set_servo_angle("right3", "tibia", stand_pos_angles["right3"]["tibia"])  # + = -

    set_servo_angle("left1", "coxa", stand_pos_angles["left1"]["coxa"])
    set_servo_angle("left1", "femur", stand_pos_angles["left1"]["femur"])  # + = +
    set_servo_angle("left1", "tibia", stand_pos_angles["left1"]["tibia"])  # + = -

    set_servo_angle("left2", "coxa", stand_pos_angles["left2"]["coxa"])
    set_servo_angle("left2", "femur", stand_pos_angles["left2"]["femur"])  # + = +
    set_servo_angle("left2", "tibia", stand_pos_angles["left2"]["tibia"])  # + = -

    set_servo_angle("left3", "coxa", stand_pos_angles["left3"]["coxa"])
    set_servo_angle("left3", "femur", stand_pos_angles["left3"]["femur"])  # + = +
    set_servo_angle("left3", "tibia", stand_pos_angles["left3"]["tibia"])  # + = -


# Move forward function
def move_forward():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle(
            "right1", "tibia", stand_pos_angles["right1"]["tibia"] - FM1 * 2
        )  # 140
        set_servo_angle(
            "right1", "femur", stand_pos_angles["right1"]["femur"] + FM1 * 3
        )  # 145

        set_servo_angle(
            "right3", "tibia", stand_pos_angles["right3"]["tibia"] - FM1 * 2
        )  # 150
        set_servo_angle(
            "right3", "femur", stand_pos_angles["right3"]["femur"] + FM1 * 3
        )  # 135

        set_servo_angle(
            "left2", "tibia", stand_pos_angles["left2"]["tibia"] - FM1 * 2
        )  # 150
        set_servo_angle(
            "left2", "femur", stand_pos_angles["left2"]["femur"] + FM1 * 3
        )  # 125
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle(
            "right1", "coxa", stand_pos_angles["right1"]["coxa"] + FM2
        )  # 100
        set_servo_angle(
            "right3", "coxa", stand_pos_angles["right3"]["coxa"] + FM2
        )  # 90
        set_servo_angle("left2", "coxa", stand_pos_angles["left2"]["coxa"] - FM2)  # 90
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle(
            "right1", "tibia", (stand_pos_angles["right1"]["tibia"] - 20) + FM3 * 2
        )  # 140 --> 120
        set_servo_angle(
            "right1", "femur", (stand_pos_angles["right1"]["femur"] + 30) - FM3 * 3
        )  # 145 --> 175

        set_servo_angle(
            "right3", "tibia", (stand_pos_angles["right3"]["tibia"] - 20) + FM3 * 2
        )  # 150 --> 130
        set_servo_angle(
            "right3", "femur", (stand_pos_angles["right3"]["femur"] + 30) - FM3 * 3
        )  # 135 --> 165

        set_servo_angle(
            "left2", "tibia", (stand_pos_angles["left2"]["tibia"] - 20) + FM3 * 2
        )  # 150 --> 130
        set_servo_angle(
            "left2", "femur", (stand_pos_angles["left2"]["femur"] + 30) - FM3 * 3
        )  # 125 --> 155

        FM3 += 1

    if FM2 >= 40:
        set_servo_angle(
            "right1", "coxa", (stand_pos_angles["right1"]["coxa"] + 40) - FM4
        )  # 100 --> 140
        set_servo_angle(
            "right3", "coxa", (stand_pos_angles["right3"]["coxa"] + 40) - FM4
        )  # 90 --> 130
        set_servo_angle(
            "left2", "coxa", (stand_pos_angles["left2"]["coxa"] - 40) + FM4
        )  # 90 --> 50
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle(
                "right2", "tibia", stand_pos_angles["right1"]["tibia"] - FM5 * 2
            )  # 125
            set_servo_angle(
                "right2", "femur", stand_pos_angles["right1"]["femur"] + FM5 * 3
            )  # 140

            set_servo_angle(
                "left1", "tibia", stand_pos_angles["right3"]["tibia"] - FM5 * 2
            )  # 140
            set_servo_angle(
                "left1", "femur", stand_pos_angles["right3"]["femur"] + FM5 * 3
            )  # 135

            set_servo_angle(
                "left3", "tibia", stand_pos_angles["left2"]["tibia"] - FM5 * 2
            )  # 145
            set_servo_angle(
                "left3", "femur", stand_pos_angles["left2"]["femur"] + FM5 * 3
            )  # 140

            FM5 += 1

        if FM6 <= 40:
            set_servo_angle(
                "right2", "coxa", stand_pos_angles["right2"]["coxa"] + FM6
            )  # 95
            set_servo_angle(
                "left1", "coxa", stand_pos_angles["left1"]["coxa"] - FM6
            )  # 95
            set_servo_angle(
                "left3", "coxa", stand_pos_angles["left3"]["coxa"] - FM6
            )  # 90
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle(
                "right2", "tibia", (stand_pos_angles["right2"]["tibia"] - 20) + FM7 * 2
            )  # 125 --> 105
            set_servo_angle(
                "right2", "femur", (stand_pos_angles["right2"]["tibia"] + 30) - FM7 * 3
            )  # 140 --> 170

            set_servo_angle(
                "left1", "tibia", (stand_pos_angles["left1"]["tibia"] - 20) + FM7 * 2
            )  # 140 --> 120
            set_servo_angle(
                "left1", "femur", (stand_pos_angles["left1"]["tibia"] + 30) - FM7 * 3
            )  # 135 --> 165

            set_servo_angle(
                "left3", "tibia", (stand_pos_angles["left3"]["tibia"] - 20) + FM7 * 2
            )  # 145 --> 125
            set_servo_angle(
                "left3", "femur", (stand_pos_angles["left3"]["tibia"] + 30) - FM7 * 3
            )  # 140 --> 170
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle(
                "right2", "coxa", (stand_pos_angles["right2"]["coxa"] + 40) - FM8
            )  # 95 --> 135
            set_servo_angle(
                "left1", "coxa", (stand_pos_angles["left1"]["coxa"] - 40) + FM8
            )  # 95 --> 55
            set_servo_angle(
                "left3", "coxa", (stand_pos_angles["left3"]["coxa"] - 40) + FM8
            )  # 90 --> 50
            FM8 += 1

        if FM8 >= 40:
            Impair_start = False
            FM5 = FM6 = FM7 = FM8 = 0

def move_backward():
    global FM1, FM2, FM3, FM4, FM5, FM6, FM7, FM8, Impair_start
    if FM1 <= 10:
        set_servo_angle(
            "right1", "tibia", stand_pos_angles["right1"]["tibia"] + FM1 * 2
        )  # Reversing the forward movement
        set_servo_angle(
            "right1", "femur", stand_pos_angles["right1"]["femur"] - FM1 * 3
        )

        set_servo_angle(
            "right3", "tibia", stand_pos_angles["right3"]["tibia"] + FM1 * 2
        )
        set_servo_angle(
            "right3", "femur", stand_pos_angles["right3"]["femur"] - FM1 * 3
        )

        set_servo_angle("left2", "tibia", stand_pos_angles["left2"]["tibia"] + FM1 * 2)
        set_servo_angle("left2", "femur", stand_pos_angles["left2"]["femur"] - FM1 * 3)
        FM1 += 1

    if FM2 <= 40:
        set_servo_angle("right1", "coxa", stand_pos_angles["right1"]["coxa"] - FM2)
        set_servo_angle("right3", "coxa", stand_pos_angles["right3"]["coxa"] - FM2)
        set_servo_angle("left2", "coxa", stand_pos_angles["left2"]["coxa"] + FM2)
        FM2 += 1

    if FM2 > 25 and FM3 <= 10:
        set_servo_angle(
            "right1", "tibia", (stand_pos_angles["right1"]["tibia"] + 20) - FM3 * 2
        )
        set_servo_angle(
            "right1", "femur", (stand_pos_angles["right1"]["femur"] - 30) + FM3 * 3
        )

        set_servo_angle(
            "right3", "tibia", (stand_pos_angles["right3"]["tibia"] + 20) - FM3 * 2
        )
        set_servo_angle(
            "right3", "femur", (stand_pos_angles["right3"]["femur"] - 30) + FM3 * 3
        )

        set_servo_angle(
            "left2", "tibia", (stand_pos_angles["left2"]["tibia"] + 20) - FM3 * 2
        )
        set_servo_angle(
            "left2", "femur", (stand_pos_angles["left2"]["femur"] - 30) + FM3 * 3
        )

        FM3 += 1

    if FM2 >= 40:
        set_servo_angle(
            "right1", "coxa", (stand_pos_angles["right1"]["coxa"] - 40) + FM4
        )
        set_servo_angle(
            "right3", "coxa", (stand_pos_angles["right3"]["coxa"] - 40) + FM4
        )
        set_servo_angle("left2", "coxa", (stand_pos_angles["left2"]["coxa"] + 40) - FM4)
        FM4 += 1
        Impair_start = True

    if FM4 >= 40:
        FM1 = FM2 = FM3 = FM4 = 0

    if Impair_start:
        if FM5 <= 10:
            set_servo_angle(
                "right2", "tibia", stand_pos_angles["right1"]["tibia"] + FM5 * 2
            )
            set_servo_angle(
                "right2", "femur", stand_pos_angles["right1"]["femur"] - FM5 * 3
            )

            set_servo_angle(
                "left1", "tibia", stand_pos_angles["right3"]["tibia"] + FM5 * 2
            )
            set_servo_angle(
                "left1", "femur", stand_pos_angles["right3"]["femur"] - FM5 * 3
            )

            set_servo_angle(
                "left3", "tibia", stand_pos_angles["left2"]["tibia"] + FM5 * 2
            )
            set_servo_angle(
                "left3", "femur", stand_pos_angles["left2"]["femur"] - FM5 * 3
            )

            FM5 += 1

        if FM6 <= 40:
            set_servo_angle("right2", "coxa", stand_pos_angles["right2"]["coxa"] - FM6)
            set_servo_angle("left1", "coxa", stand_pos_angles["left1"]["coxa"] + FM6)
            set_servo_angle("left3", "coxa", stand_pos_angles["left3"]["coxa"] + FM6)
            FM6 += 1

        if FM6 > 25 and FM7 <= 10:
            set_servo_angle(
                "right2", "tibia", (stand_pos_angles["right2"]["tibia"] + 20) - FM7 * 2
            )
            set_servo_angle(
                "right2", "femur", (stand_pos_angles["right2"]["tibia"] - 30) + FM7 * 3
            )

            set_servo_angle(
                "left1", "tibia", (stand_pos_angles["left1"]["tibia"] + 20) - FM7 * 2
            )
            set_servo_angle(
                "left1", "femur", (stand_pos_angles["left1"]["tibia"] - 30) + FM7 * 3
            )

            set_servo_angle(
                "left3", "tibia", (stand_pos_angles["left3"]["tibia"] + 20) - FM7 * 2
            )
            set_servo_angle(
                "left3", "femur", (stand_pos_angles["left3"]["tibia"] - 30) + FM7 * 3
            )
            FM7 += 1

        if FM6 >= 40:
            set_servo_angle(
                "right2", "coxa", (stand_pos_angles["right2"]["coxa"] - 40) + FM8
            )
            set_servo_angle(
                "left1", "coxa", (stand_pos_angles["left1"]["coxa"] + 40) - FM8
            )
            set_servo_angle(
                "left3", "coxa", (stand_pos_angles["left3"]["coxa"] + 40) - FM8
            )
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


# Main function
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
            pass  # Implement left movement
        elif keyboard.is_pressed("d"):
            pass  # Implement right movement
        elif keyboard.is_pressed("ctrl+s"):
            print("Setting Stand Position...")
            stand_pos()
        elif keyboard.is_pressed("ctrl+u"):
            print("Setting Up Position...")
            up_pos()
        elif keyboard.is_pressed("q"):
            print("Exiting program...")
            break

        time.sleep(0.007)  # Small delay to reduce CPU usage


if __name__ == "__main__":
    time.sleep(2)  # Set initial position
    main()
#     stand_pos()
