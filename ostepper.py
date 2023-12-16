# Write your code here :-)
import machine
import time
# Define the GPIO pins for STEP and DIR
STEP_PIN1 = machine.Pin(17, machine.Pin.OUT)
DIR_PIN1 = machine.Pin(16, machine.Pin.OUT)
STEP_PIN2 = machine.Pin(14, machine.Pin.OUT)
DIR_PIN2 = machine.Pin(15, machine.Pin.OUT)




# Set the direction (CW or CCW, 1 for clockwise, 0 for counterclockwise)

num_steps = 200  # Adjust for your motor's steps per revolution
delay = 100 # Adjust for your desired speed and torque; units in microseconds
#Step the motor

def movex(distance):
    if distance > 0:
        direction = 0
    else:
        direction = 1
    DIR_PIN1.value(direction)
    for i in range(num_steps*abs(distance)):
        STEP_PIN1.value(1)
        time.sleep_us(delay)
        STEP_PIN1.value(0)
        time.sleep_us(delay)
    STEP_PIN1.value(0)
    DIR_PIN1.value(0)


def movey(distance):
    if distance > 0:
        direction = 0
    else:
        direction = 1
    DIR_PIN2.value(direction)
    for i in range(num_steps*abs(distance)):
        STEP_PIN2.value(1)
        time.sleep_us(delay)
        STEP_PIN2.value(0)
        time.sleep_us(delay)
    STEP_PIN2.value(0)
    DIR_PIN2.value(0)
