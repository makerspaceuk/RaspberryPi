from bluetooth import *
from sense_hat import SenseHat
from time import sleep
import sys
　
# Set up sense HAT object
sense = SenseHat()
　
def setBubble(x, y):
    # print "{0}{1}".format(x,y)
    sense.clear()
    sense.set_pixel(x, y, 255, 255, 255)
    sense.set_pixel(x, y + 1, 255, 255, 255)
    sense.set_pixel(x + 1, y, 255, 255, 255)
    sense.set_pixel(x + 1, y + 1, 255, 255, 255)
　
def drawBT(colour):
    sense.clear()
    sense.set_pixel(0, 3, colour)
    sense.set_pixel(1, 2, colour)
    sense.set_pixel(1, 3, colour)
    sense.set_pixel(1, 5, colour)
    sense.set_pixel(2, 1, colour)
    sense.set_pixel(2, 3, colour)
    sense.set_pixel(2, 4, colour)
    sense.set_pixel(3, 2, colour)
    sense.set_pixel(3, 3, colour)
    sense.set_pixel(4, 2, colour)
    sense.set_pixel(4, 3, colour)
    sense.set_pixel(5, 1, colour)
    sense.set_pixel(5, 3, colour)
    sense.set_pixel(5, 4, colour)
    sense.set_pixel(6, 2, colour)
    sense.set_pixel(6, 3, colour)
    sense.set_pixel(6, 5, colour)
    sense.set_pixel(7, 3, colour)
　
# Set up a flag to allow testing without using bluetooth
doBT = True
　
# Define the Bluetooth address of our Bluetooth server
serverBTAddress = "B8:27:EB:66:55:58"
　
# Create client bluetooth socket and connect to server
if doBT:
    try:
        drawBT((0,255,0))
        clientSocket = BluetoothSocket(RFCOMM)
        clientSocket.connect((serverBTAddress, 3))
        drawBT((0,0,255))
        print "Bluetooth connected"
        sleep(2)
    except:
        drawBT((255,0,0))
        print "Bluetooth error"
        sys.exit()
　
# Initialise variables
prevCommand = 0
　
# Show level bubble at centre of sense hat
setBubble(3, 3)
　
try:
    while True:
        # Read the orientation from the Sense HAT
        orientation = sense.get_orientation()
        pitch = orientation['pitch']
        roll = orientation['roll']
        yaw = orientation['yaw']
　
        # Pitch can have any value between 270 to 360 and 0 to 90
        # 270 is backward pitch
        # 360/0 is level
        # 90 is forward pitch
        if pitch >= 0 and pitch <= 90:
            # Forward pitch (1 to indicate fully forward)
            pitch = (pitch / 180) + 0.5
        elif pitch >= 270 and pitch <= 360:
            # Reverse pitch (0 to indicate fully reverse)
            pitch = 0.5 - ((360 - pitch) / 180)
        else:
            # 0.5 to indicate level
            pitch = 0.5
　
        # Roll can have any value from 0 to 360
        # 270 is right roll
        # 360/0 is level
        # 90 is left roll
        if roll >= 0 and roll <= 90:
            # Left roll
            roll = (roll / 180) + 0.5
        elif roll >= 270 and roll <= 360:
            # Right roll
            roll = 0.5 - ((360 - roll) / 180)
        else:
            # Ignore anything between 90 and 270
            # 0.5 to indicate level
            roll = 0.5
　
        # Construct a command to send to crane
        # This is a 2 digit number
        # Digit 1 is the pitch value (0 - 7)
        # Digit 2 is the roll value (0 - 7)
        pitch = int(pitch * 7)
        roll = int(roll * 7)
        command = str(pitch) + str(roll)
　
        # Only send the command if it is different to last command
        if command != prevCommand:
            # Send command to crane
            # print("Command={0}".format(command))
            if doBT:
                clientSocket.send(str(command))
            prevCommand = command
            setBubble(6 - pitch, roll)
        
        sleep(0.01)
　
except:
    if doBT:
        # Close the Bluetooth socket
        clientSocket.close()
　
        # Indicate bluetooth connection closed
        drawBT((255,0,0))
　
