from Read import rfid, scanned_card, bump
from threading import Thread 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def dif(lst):
    if lst[0] == lst[1]:
        return False
    return True

def disable(io, exceptions=[]):
    for c,i in io:
        if c not in exceptions:
            GPIO.output(c, GPIO.LOW)

io = [[11,"12345678"], [12,"22345678"], [13,"33345678"]]

Thread(target=rfid).start()


while True:
    print(scanned_card)
    if dif(scanned_card):
        for c,i in io:
            if i == scanned_card[0]:
                GPIO.output(c,GPIO.HIGH)
                disable(io, exceptions=[c])
                bump(scanned_card, i)
                break
            
