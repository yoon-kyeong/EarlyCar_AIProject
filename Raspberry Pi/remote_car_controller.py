import socket
from YB_Pcb_Car import YB_Pcb_Car 
#YB_Pcb_Car코드 및 기본 코드는 http://www.yahboom.net/study/Raspbot 공식 사이트에 있다
import time

car = YB_Pcb_Car()

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ('192.168.0.32', 10055)  # Replace with your Raspberry Pi's IP address
sock.bind(server_address)

print('Waiting for a connection...')

try:
    while True:
        # Receive the data
        data, address = sock.recvfrom(4096)
        command = data.decode()

        print('Received command: ', command)

        # Execute the command
        if command == 'f':
            car.Car_Run(100, 100)
        elif command == 'stop':
            car.Car_Stop()
        elif command == 'l':
            car.Car_Left(0, 150)
        elif command == 'r':
            car.Car_Right(150, 0)
        else:
            print('Invalid command:', command)

finally:
    # Clean up the socket
    sock.close()

#python3 코드이름.py로 실행해야 한다.