from adafruit_servokit import ServoKit
import time

# Initialize ServoKit instances for two PCA9685 boards
board1 = ServoKit(channels=16, address=0x40)

board1.servo[0].angle = 90
board1.servo[1].angle = 90
