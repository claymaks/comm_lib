import time
import random

scanned_card = [None, None]

def bump(lst, x):
    lst[1], lst[0] = lst[0], x

def rfid():
    while True:
        time.sleep(random.randint(0,10))
        bump(scanned_card, \
             random.choice(\
                 ("".join(str(random.randint(0,9)) for i in range(0,10)), '12345678', '22345678', '33345678')))
