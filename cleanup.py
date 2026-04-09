from adafruit_servokit import ServoKit
import time

# Initialize ServoKit instances for two PCA9685 boards
board1 = ServoKit(channels=16, address=0x40)
board2 = ServoKit(channels=16, address=0x41)

# Servo pulse range
SERVOMIN = 125  # Minimum pulse length count
SERVOMAX = 575  # Maximum pulse length count


# Angle-to-pulse conversion function
def angle_to_pulse(angle):
    return int((SERVOMAX - SERVOMIN) * angle / 180 + SERVOMIN)


# Right leg functions
def right_leg_1(i, angle):  # Right Leg 1 --> 0, 1, 2
    if i == 2:
        board1.servo[i + 4].angle = angle
    else:
        board2.servo[i - 1].angle = angle


def right_leg_2(i, angle):  # Right Leg 2 --> 3, 4, 5
    board1.servo[i + 2].angle = angle


def right_leg_3(i, angle):  # Right Leg 3 --> 13, 14, 15
    board1.servo[i + 12].angle = angle


# Left leg functions
def left_leg_1(i, angle):  # Left Leg 1 --> 13, 14, 15
    board2.servo[i + 12].angle = angle


def left_leg_2(i, angle):  # Left Leg 2 --> 3, 4, 5
    board2.servo[i + 2].angle = angle


def left_leg_3(i, angle):  # Left Leg 3 --> 6, 7, 2
    if i == 3:
        board2.servo[i - 1].angle = angle
    else:
        board2.servo[i + 5].angle = angle

def stand_pos():
    # Right leg

    right_leg_1(1, None)  # R1
    right_leg_1(2, None)
    right_leg_1(3, None)

    right_leg_2(1, None)  # R2
    right_leg_2(2, None)
    right_leg_2(3, None)

    right_leg_3(1, None)  # R3
    right_leg_3(2, None)
    right_leg_3(3, None)

    # Left leg
    left_leg_1(1, None)  # L1
    left_leg_1(2, None)
    left_leg_1(3, None)

    left_leg_2(1, None)  # L2
    left_leg_2(2, None)
    left_leg_2(3, None)

    left_leg_3(1, None)  # L3
    left_leg_3(2, None)
    left_leg_3(3, None)


# Main execution
if __name__ == "__main__":
    stand_pos()
