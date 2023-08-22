import pygame
import socket

# Initialize the pygame module
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Connect to the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# UDP setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('라즈베리파이 ip주소', 10055) 

while True:
    pygame.event.pump()
    # Send joystick axis values for acceleration, braking and steering
    acc_value = joystick.get_axis(2)
    brake_value = joystick.get_axis(1)
    steer_value = joystick.get_axis(0)

    if steer_value >= -0.2 and steer_value <= 0.2:
        command = 'stop'  # Use assignment operator instead of comparison
        if acc_value <= 1:
            if -1 <= acc_value < 0.8:
                command = 'f'
            elif acc_value >= 0.8 and acc_value < 1:
                command = 'stop'
    elif steer_value < -0.2:
        if -1 <= acc_value < 0.8:
                command = 'l_r' 
        else:
            command = 'l'

    elif steer_value > 0.2:
        if -1 <= acc_value < 0.8:
                command = 'f_r' 
        else:
            command = 'r'

    for i in range(joystick.get_numbuttons()):
        button = joystick.get_button(i)
        if button == 1:
            if i == 3:  # Change button number to match your gamepad button configuration
                command = 'close'
            elif i == 5:  # Change button number to match your gamepad button configuration
                command = 'stop'
            elif i == 4: 
                command = 'back'

    # Send command
    if command:
        sent = sock.sendto(command.encode(), server_address)
        print(command)

    # To reduce the rate of sending command and allow other commands to be processed
    pygame.time.wait(100)