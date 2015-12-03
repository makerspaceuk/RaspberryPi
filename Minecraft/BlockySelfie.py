# Martin O'Hanlon
# www.stuffaboutcode.com
# Minecraft Selfie Camera
# Minecraft Picture Rendering Script By Ferran Fabregas (ferri.fc@gmail.com)
# Blocky Selfie saving to file by Ivan Holland

import picamera
from PIL import Image
import math
from mcpi.minecraft import Minecraft
from time import sleep, time
import random

white=(221,221,221)
orange=(219,125,62)
magenta=(179,80,188)
lightblue=(107,138,201)
yellow=(177,166,39)
lime=(65,174,56)
pink=(208,132,153)
gray=(64,64,64)
lightgray=(154,161,161)
cyan=(46,110,137)
purple=(126,61,181)
blue=(46,56,141)
brown=(79,50,31)
green=(53,70,27)
red=(150,52,48)
black=(25,22,22)

blocksize = 16
ditheroffsets = (-10, -5, 0, 5, 10)
block = [[random.choice(ditheroffsets) for i in range(blocksize)] for j in range(blocksize)]
colors=(white,orange,magenta,lightblue,yellow,lime,pink,gray,lightgray,cyan,purple,blue,brown,green,red,black)

def ditherPixel(x, y, colour):
    newcolour = (colour[0] + block[x][y], colour[1] + block[x][y], colour[2] + block[x][y])
    return newcolour

def putBlock(image, pixX, pixY, colour):
    for x in range(0, blocksize):
        for y in range(0, blocksize):
            image.putpixel([pixX + x, pixY + y], ditherPixel(x, y, colour))

def takePicture(filename):
    with picamera.PiCamera() as camera:
        #camera.start_preview(alpha=192)
        sleep(1)
        camera.resolution = (768, 1024)
        camera.capture(filename)
        #camera.stop_preview()

def colormap(pixel):
    thecolor=0
    finalresult=256*256*256
    for idx,color in enumerate(colors):
        result=math.fabs(color[0]-pixel[0])+math.fabs(color[1]-pixel[1])+math.fabs(color[2]-pixel[2])
        if result<finalresult:
            finalresult=result
            thecolor=idx
    return thecolor

def buildMCImage(mc, filename, thumbname, pos):

    MAXY = 60
    im = Image.open(filename)

    #resize image file
    if im.size[1] > MAXY:
        ratio = MAXY / float(im.size[1])
        sizeY = MAXY
        sizeX = int(im.size[0] * ratio)
        im.thumbnail([sizeX, sizeY], Image.ANTIALIAS)
        size = im.size[0] * blocksize, im.size[1] * blocksize
      
    pixels=im.load()
    thumb = Image.new('RGB', size, 'black')

    startX = pos.x - int(im.size[0] / 2)
    startY = pos.y + sizeY
    for x in range (0,im.size[0]):
        for y in range (0,(im.size[1])):
            blockColour = colormap(pixels[x, y])
            mc.setBlock(startX + x, startY - y, pos.z - 1, 35,
                        blockColour)

            putBlock(thumb, x * blocksize, y * blocksize, colors[blockColour])
            #print "{}.{}.{}".format(x, y, 5)
            sleep(0.005)
    thumb.save(thumbname)
    

mc=Minecraft.create()
mc.postToChat("Welcome to Minecraft Camera")
mc.postToChat("Hit a block (right click with sword)")

while True:
    #has a block been hit?
    for hit in mc.events.pollBlockHits():
        fileroot = "/home/pi/MyAdventures/images/" + str(int(time()))
        fileroot = str(int(time()))
        filename = fileroot + ".png"
        thumbname = fileroot + "-thumb.png"
        mc.postToChat("Taking picture in 1 second")
        sleep(1)
        takePicture(filename)
        mc.postToChat("Building image")
        buildMCImage(mc, filename, thumbname, hit.pos)
        mc.postToChat("Image built")

        #clear any block hit events
        mc.events.clearAll()

        break
    sleep(0.1)
