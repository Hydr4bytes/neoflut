# a simpel pixelflut client

from re import S
import socket
import time
from tkinter import Canvas
from venv import create
from PIL import Image, ImageDraw, ImageFont
import random
# import threading
from multiprocessing import Process
import os
import configparser
import colorsys
from math import *

gradient = {}

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

# get a image and convert it to a random list of pixels
def getpixels(imagepath, screensize, center=False, fill=False):
    canvas = screensize

    image = Image.open(imagepath)
    resized_image = image.resize(canvas)
    pix = resized_image.convert('RGB').load()

    pixels = []
    for x in range(canvas[0]):
        for y in range(canvas[1]):
            if(x % 2 == 0):
                (r, g, b) = pix[x,y]
                pixels.append((x, y, r, g, b))
            else:
                (r, g, b) = gradient[y]
                pixels.append((x, y, int(r), int(g), int(b)))

    # randomize the list
    random.shuffle(pixels)
    return pixels

def strings(pixels):
    # make a list of strings to send
    lines = []
    for pixel in pixels:
        line = "PX %s %s %s%s%s\n" % (pixel[0], pixel[1], '%0*x' % (2,pixel[2]), '%0*x' % (2,pixel[3]), '%0*x' % (2,pixel[4]))
        lines.append(line)
    return lines

def connect(server_address, port):
    # Create a TCP/IP socket to a ip and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_address = ('') # ip
    # port = 1234
    server_address = (server_address, port)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    print('connected')
    return sock

def send_thread(lines, server_address, port):
    # connect to server
    sock = connect(server_address, port)
    # prepare to send by generating a string and encoding it
    data = ''.join(lines).encode()
    # send data in a loop
    while True:
        sock.sendall(data)


# main function
def main():
    # get image and server address from config file
    configReader = configparser.ConfigParser()
    configReader.read('config.ini')
    config = configReader['Neoflut']

    imagepath = config['image']
    server_address = config['address']
    port = int(config['port'])
    multicon = int(config['threads'])
    screenx = int(config['screenX'])
    screeny = int(config['screenY'])
    centering = int(config['center'])
    fill = int(config['fill'])
    screensize = (screenx, screeny)

    for i in range(screensize[1]):
        gradient[i] = hsv_to_rgb(i/screensize[1], 1, 1)

    # get pixels from image
    pixels = getpixels(imagepath, screensize, centering, fill)
    # make a list of strings to send
    lines = strings(pixels)

    # if multicon is not 0, connect to server multicon times in seperate proseses, starting each thread with a random offset
    if multicon != 0:
        for i in range(multicon):
            # random number between 0 and number of lines
            offset = (random.randint(0, len(lines)))
            # start thread with offset
            # create new list with offset and reapeat the skipped lines at the end
            newlines = lines[offset:] + lines[:offset]
            # threading.Thread(target=send_thread, args=(newlines, server_address, port)).start()
            Process(target=send_thread, args=(newlines, server_address, port)).start()

if __name__ == "__main__":
    main()
