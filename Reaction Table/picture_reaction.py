# Import required libraries
import RPi.GPIO as GPIO
import pygame
import MPR121
import sys
from time import sleep, time
import random

# Initialise pygame library
pygame.init()
pygame.mixer.init()

# Get the current display size to get objects sized and positioned correctly
infoObject = pygame.display.Info()
WINDOWWIDTH = infoObject.current_w
WINDOWHEIGHT = infoObject.current_h

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

print WINDOWWIDTH
print WINDOWHEIGHT

IMAGESIZE = 600

# Define the length of the game in seconds
GAMETIME = 3.0

# Setup pygame window
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Match Race')
BASICFONT = pygame.font.Font('freesansbold.ttf', 36)

# Define sounds to play
player1Sound = pygame.mixer.Sound("/home/pi/python_games/match1.wav")
player2Sound = pygame.mixer.Sound("/home/pi/python_games/match5.wav")
penaltySound = pygame.mixer.Sound("/home/pi/python_games/badswap.wav")
countSound   = pygame.mixer.Sound("/home/pi/python_games/match0.wav")

# Define a list of images to display
images = ("/home/pi/python_code/Reaction/M-R1.jpg",
          "/home/pi/python_code/Reaction/M-R2.jpg",
          "/home/pi/python_code/Reaction/M-R3.jpg",
          "/home/pi/python_code/Reaction/M-R4.jpg",
          "/home/pi/python_code/Reaction/M-R5.jpg",
          "/home/pi/python_code/Reaction/M-R6.jpg",
          "/home/pi/python_code/Reaction/M-G1.jpg",
          "/home/pi/python_code/Reaction/M-G2.jpg",
          "/home/pi/python_code/Reaction/M-G3.jpg",
          "/home/pi/python_code/Reaction/M-G4.jpg",
          "/home/pi/python_code/Reaction/M-G5.jpg",
          "/home/pi/python_code/Reaction/M-G6.jpg",
          "/home/pi/python_code/Reaction/M-B1.jpg",
          "/home/pi/python_code/Reaction/M-B2.jpg",
          "/home/pi/python_code/Reaction/M-B3.jpg",
          "/home/pi/python_code/Reaction/M-B4.jpg",
          "/home/pi/python_code/Reaction/M-B5.jpg",
          "/home/pi/python_code/Reaction/M-B6.jpg",
          "/home/pi/python_code/Reaction/M-Y1.jpg",
          "/home/pi/python_code/Reaction/M-Y2.jpg",
          "/home/pi/python_code/Reaction/M-Y3.jpg",
          "/home/pi/python_code/Reaction/M-Y4.jpg",
          "/home/pi/python_code/Reaction/M-Y5.jpg",
          "/home/pi/python_code/Reaction/M-Y6.jpg")

# Function which simply waits for a pad to be touched
def waitForTouch():
    touched = False
    while not touched:
        if sensor.touch_status_changed():
            sensor.update_touch_data()
            for i in range(12):
                if sensor.is_new_touch(i):
                    touched = True

# Function to display an initialisation message
def displayInitialise():
    displayX = int (WINDOWWIDTH / 2)
    displayY = int (WINDOWHEIGHT / 2)
    numberFont = pygame.font.Font('freesansbold.ttf', 36)
    label = numberFont.render("Initialising. Please wait ...", True, (255,255,255))
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(label, (displayX - int (label.get_width() / 2), displayY - int (label.get_height() / 2)))
    pygame.display.update()

# Function to display a countdownn at the start of the game
def displayCountdown(start):
    displayX = int (WINDOWWIDTH / 2)
    displayY = int (WINDOWHEIGHT / 2)
    numberFont = pygame.font.Font('freesansbold.ttf', 250)
    for i in range(start, 0, -1):
        countSound.play()
        label = numberFont.render(str(i), True, (255,255,255))
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(label, (displayX - int (label.get_width() / 2), displayY - int (label.get_height() / 2)))
        pygame.display.update()
        sleep(1)

# Function to display the player scores
def displayScores(player1, player2):
    displayX = int (WINDOWWIDTH / 2)
    displayY = int (WINDOWHEIGHT / 2)
    numberFont = pygame.font.Font('freesansbold.ttf', 70)
    label1 = numberFont.render("Player 1 score = " + str(player1), True, (255,255,255))
    label2 = numberFont.render("Player 2 score = " + str(player2), True, (255,255,255))
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(label1, (displayX - int (label1.get_width() / 2), displayY - label1.get_height()))
    DISPLAYSURF.blit(label2, (displayX - int (label1.get_width() / 2), displayY - label1.get_height() + label2.get_height()))
    pygame.display.update()
    sleep(5)

# Function to display instruction to continue game
def displayContinue():
    displayX = int (WINDOWWIDTH / 2)
    displayY = WINDOWHEIGHT
    numberFont = pygame.font.Font('freesansbold.ttf', 50)
    label = numberFont.render("Touch any pad to continue ...", True, (255,255,255))
    DISPLAYSURF.blit(label, (displayX - int (label.get_width() / 2), displayY - label.get_height()))
    pygame.display.update()

# Function to display image
def displayPicture(image):
    displayX = int (WINDOWWIDTH / 2) - int (image.get_width() / 2)
    displayY = int (WINDOWHEIGHT / 2) - int (image.get_height() / 2)
    spaceRect = pygame.Rect(displayX, displayY, IMAGESIZE, IMAGESIZE)
    DISPLAYSURF.blit(image, spaceRect)
    pygame.display.update()

# Define a list of colours from LED combinations
RED     = (1, 0, 0)
GREEN   = (0, 1, 0)
BLUE    = (0, 0, 1)
YELLOW  = (1, 1, 0)
MAGENTA = (1, 0, 1)
CYAN    = (0, 1, 1)
WHITE   = (1, 1, 1)
BLACK   = (0, 0, 0)

displayInitialise()

# Define a list of display images
displayImages = []
for image in images:
    displayImage = pygame.image.load(image)
    if displayImage.get_size() != (IMAGESIZE, IMAGESIZE):
        displayImage = pygame.transform.smoothscale(displayImage, (IMAGESIZE, IMAGESIZE))
    displayImages.append(displayImage)

# Define pin numbers for LED colours
REDPIN = 31
GREENPIN = 29
BLUEPIN = 37

# Define a list for the pin numbers
pins = (REDPIN, GREENPIN, BLUEPIN)

# Define a list of colours
colours = (RED, GREEN, BLUE, YELLOW, WHITE, CYAN)

# Define a list of screen colours
SCREENRED    = (255, 0, 0)
SCREENGREEN  = (0, 255, 0)
SCREENBLUE   = (0, 0, 255)
SCREENWHITE  = (255, 255, 255)
SCREENYELLOW = (255, 255, 0)
SCREENORANGE = (255, 127, 0)

# Define a list of screen colours
#screenColours = (SCREENRED, SCREENORANGE, SCREENYELLOW, SCREENGREEN, SCREENBLUE, SCREENWHITE)
screenColours = (SCREENWHITE, SCREENWHITE, SCREENWHITE, SCREENWHITE, SCREENWHITE, SCREENWHITE)

# Setup GPIO pins for LEDs
GPIO.setmode(GPIO.BOARD)

GPIO.setup(REDPIN, GPIO.OUT)
GPIO.setup(GREENPIN, GPIO.OUT)
GPIO.setup(BLUEPIN, GPIO.OUT)

# Switch LEDs off
for pin in pins:
    GPIO.output(pin, True)

# Initialise capacitive touch sensor
try:
    sensor = MPR121.begin()
except Exception as e:
    print e
    sys,exit(1)

continuePlaying = True

while continuePlaying:
    # Initialise score to 0
    score1 = 0
    score2 = 0

    # Start of game
    try:
        displayCountdown(5)
        # Record game start time
        startTime = time()

        # No penalty wait time to start with
        penalty = 0.0

        # Loops for 30 seconds
        while time() < startTime + GAMETIME:
            sleep(penalty)

            # Always wait at least 0.5 seconds between touches
            penalty = 0.5

            # Generate a random number for the colour
            rand = random.randint(0, len(colours) - 1)
            colour = colours[rand]

            # Switch LEDs to generate colour
            for i in range(3):
                GPIO.output(pins[i], colour[i] != 1)

            # Clear screen before displaying new image
            DISPLAYSURF.fill(BLACK)
            pygame.display.update()

            sleep(0.2)
            colour = random.randint(0, 3)
            DISPLAYSURF.fill(screenColours[rand])
            displayPicture(displayImages[rand + (colour * 6)])

            # Loop until correct pad is touched
            touched = False
            while not touched and time() < startTime + GAMETIME:
                if sensor.touch_status_changed():
                    sensor.update_touch_data()
                    for i in range(12):
                        if sensor.is_new_touch(i):
                            if i == rand or i == rand + 6:
                                touched = True
                                touchedBy = i
                            else:
                                print "Penalty"
                                penaltySound.play()
    #                            penalty = penalty + 0.5

            # If touch was inside game time, add to score
            if time() < startTime + GAMETIME:
                if touchedBy < 6:
                    player1Sound.play()
                    score1 = score1 + 1
                else:
                    player2Sound.play()
                    score2 = score2 + 1

            # Switch all LED pins off
            for pin in pins:
                GPIO.output(pin, True)

        # End of game loop, so display scores
        print "Player 1, your total score is", score1
        print "Player 2, your total score is", score2
        displayScores(score1, score2)

        # Display a message telling player how to continue
        displayContinue()

        # Wait for a pad to be touched
        waitForTouch()

        # Allow the program to quit by checking for Escape key being pressed when pad is touched
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print "QUIT"
                continuePlaying = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print "ESCAPE"
                continuePlaying = False
            else:
                print "Continue"
                continuePlaying = True

    # Clean up if program is interrupted
    except KeyboardInterrupt:
        for pin in pins:
            GPIO.output(pin, True)
        GPIO.cleanup()

# Do final bit of cleanup
for pin in pins:
    GPIO.output(pin, True)
GPIO.cleanup()
