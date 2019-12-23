#used to debug RPi code on mac
import random

BOARD = "board"
IN = "in"
PUD_UP = "up"
PUD_DOWN = "down"
HIGH = True
LOW = False

def setmode(t):
    print(t)

def setwarnings(b):
    print(b)

def setup(channel, io, pull_up_down = None):
    print("channel:\t", channel, "\n",
          "     io:\t", io, "\n",
          "    pud:\t", pull_up_down, "\n")

def input(channel):
    return random.choice((HIGH,LOW))


def output(channel, state):
    print(channel, state)
    pass
          
