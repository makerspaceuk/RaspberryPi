from bluetooth import *
import RPi.GPIO as GPIO
import time
import threading
import os
　
# Define some lists of motor speeds
speedsTurnLeft = [0, 0, 0, 0, 60, 80, 100, 0]
speedsTurnRight = [100, 80, 60, 0, 0, 0, 0, 0]
speedsHookDown = [0, 0, 0, 0, 60, 80, 100, 0]
speedsHookUp = [100, 80, 60, 0, 0, 0, 0, 0]
　
# Initialise GPIO settings
GPIO.setmode(GPIO.BCM)
　
# Define GPIO pin numbers for the motors
# Motor 1 is crane rotation
motorTurnLeft = 16
motorTurnRight = 19
　
# Motor 2 is the the hook
motorHookDown = 13
motorHookUp = 12
　
# Use a PWM frequency of 100
pwmFrequency= 100
　
craneThreadContinue = True
　
def craneThread():
　
    def cleanUp():
        print "Running clean up routine"
        # Stop all motors and cleanup GPIO
        hookUp.ChangeDutyCycle(0)
        hookDown.ChangeDutyCycle(0)
        turnLeft.ChangeDutyCycle(0)
        turnRight.ChangeDutyCycle(0)
　
        # Close the bluetooth sockets
        clientSocket.close()
        serverSocket.close()
　
    print "Starting crane thread"
    # Setup the GPIO pins as outputs
    GPIO.setup(motorTurnLeft, GPIO.OUT)
    GPIO.setup(motorTurnRight, GPIO.OUT)
    GPIO.setup(motorHookDown, GPIO.OUT)
    GPIO.setup(motorHookUp, GPIO.OUT)
　
    # Define PWM objects
    hookUp = GPIO.PWM(motorHookUp, pwmFrequency)
    hookDown = GPIO.PWM(motorHookDown, pwmFrequency)
    turnLeft = GPIO.PWM(motorTurnLeft, pwmFrequency)
    turnRight = GPIO.PWM(motorTurnRight, pwmFrequency)
　
    # Start PWM objects with a duty cycle of 0
    hookUp.start(0)
    hookDown.start(0)
    turnLeft.start(0)
    turnRight.start(0)
　
    def motorCheck(dutyCycle):
        # Quick check that all motors are working
        # print "Hook up"
        hookUp.ChangeDutyCycle(dutyCycle)
        hookDown.ChangeDutyCycle(0)
        turnLeft.ChangeDutyCycle(0)
        turnRight.ChangeDutyCycle(0)
        time.sleep(1)
　
        # print "Hook down"
        hookUp.ChangeDutyCycle(0)
        hookDown.ChangeDutyCycle(dutyCycle)
        turnLeft.ChangeDutyCycle(0)
        turnRight.ChangeDutyCycle(0)
        time.sleep(1)
　
        # print "Turn right"
        hookUp.ChangeDutyCycle(0)
        hookDown.ChangeDutyCycle(0)
        turnLeft.ChangeDutyCycle(0)
        turnRight.ChangeDutyCycle(dutyCycle)
        time.sleep(1)
　
        # print "Turn left"
        hookUp.ChangeDutyCycle(0)
        hookDown.ChangeDutyCycle(0)
        turnLeft.ChangeDutyCycle(dutyCycle)
        turnRight.ChangeDutyCycle(0)
        time.sleep(1)
　
        # print "All stop"
        hookUp.ChangeDutyCycle(0)
        hookDown.ChangeDutyCycle(0)
        turnLeft.ChangeDutyCycle(0)
        turnRight.ChangeDutyCycle(0)
　
    motorCheck(60)
　
    # Create bluetooth server socket
    serverSocket = BluetoothSocket(RFCOMM)
　
    # Bind server socket
    serverSocket.bind(("", 3))
　
    # Wait for client connection
    serverSocket.listen(1)
    clientSocket, address = serverSocket.accept()
　
    # Main loop to wait for a bluetooth packet, decode and act on it
    try:
        while craneThreadContinue:
            # Receive a bluetooth packet
            data = clientSocket.recv(2)
            # print "Received [%s]" % data
　
            # Convert the packet to an integer
            intData = int(data)
　
            # Hook is first digit and rotation is second digit
            hookVal = int(intData / 10)
            turnVal = int(intData % 10)
　
            # Set motor duty cycles
            # print "Hook={0}, Turn={1}".format(hookVal,turnVal)
            hookUp.ChangeDutyCycle(speedsHookUp[hookVal])
            hookDown.ChangeDutyCycle(speedsHookDown[hookVal])
            turnLeft.ChangeDutyCycle(speedsTurnLeft[turnVal])
            turnRight.ChangeDutyCycle(speedsTurnRight[turnVal])
　
        # Indicate thread is closing
        motorCheck(60)
        # Do clean up
        cleanUp()
　
    except:
        cleanUp()
　
print "Start crane thread"
crane = threading.Thread(target=craneThread)
crane.start()
　
GPIO.setup(4, GPIO.IN, GPIO.PUD_DOWN)
　
while True:
    try:
        if GPIO.input(4) == 1:
            startTime = time.time()
            # Button has been pressed
            print "Button pressed"
            while GPIO.input(4) == 1:
                time.sleep(0.2)
            endTime = time.time()
　
            if endTime - startTime > 2:
                # Button pressed for more than 2 seconds, so handle it
                # Handler routine times out in 5 seconds
　
                pressCount = 0
                while time.time() < (endTime + 5):
                    if GPIO.input(4) == 1:
                        print "Button pressed"
                        while GPIO.input(4) == 1:
                            time.sleep(0.2)
                        pressCount += 1
                        endTime = time.time()
　
                print pressCount
　
                if pressCount == 1:
                    # Reset crane thread
                    if craneThreadContinue:
                        print "Stopping crane thread"
                        craneThreadContinue = False
                    else:
                        print "Resetting crane thread"
                        if crane.isAlive():
                            print "Thread is still alive ..."
                        else:
                            print "Starting new crane thread"
                            craneThreadContinue = True
                            crane = threading.Thread(target=craneThread)
                            crane.start()
　
                elif pressCount == 2:
                    # Reboot
                    print "Rebooting ..."
                    os.system("sudo reboot")
　
                elif pressCount == 3:
                    # Shutdown
                    print "Shutting down ..."
                    os.system("sudo shutdown -h 0")
　
        time.sleep(0.2)
    except:
        GPIO.cleanup()
　
