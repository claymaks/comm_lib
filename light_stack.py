import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ADDR = 'http://172.20.10.2:5000'
STATION_ID = '/station/1'
ADDR += STATION_ID

def dif(lst):
    if lst[0] == lst[1]:
        return False
    return True

def disable(io, exceptions=[]):
    for c,i in io:
        if c not in exceptions:
            GPIO.output(c, GPIO.LOW)
            #print(c, "LOW")

io = [[15,"252176185193"], [11,"212220734"], [13,None]]
for c,i in io:
    GPIO.setup(c, GPIO.OUT)

GPIO.output(13, GPIO.HIGH)
disable(io, exceptions=[13])

scanned_card = [None, None]

bad_count = 0

def bump(lst, x):
    lst[1], lst[0] = lst[0], x
    
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()
    
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def rfid():
    global bad_count
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        bad_count = 0
        # Print UID
        bump(scanned_card, "%s%s%s%s" % (uid[0], uid[1], uid[2], uid[3]))
        #if dif(scanned_card):
            #print(scanned_card[0])
        #print(scanned_card[0])

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        bad_count = 0
        
        MIFAREReader.MFRC522_Read(8)
        MIFAREReader.MFRC522_StopCrypto1()
        
    else:
        bad_count += 1
        if bad_count > 1:
            bump(scanned_card, None)
while True:
    rfid()
    if dif(scanned_card):
        if scanned_card[0] == None:
            ID = 0
            in_place = False
        else:
            ID = scanned_card[0]
            in_place = True
        print(scanned_card[0])
        #print(requests.get(ADDR).json())
        print(requests.put(ADDR, data={'rfid':ID, 'in_place':in_place}).json())
        GPIO.output(c,GPIO.HIGH)
        disable(io, exceptions=[c])
        bump(scanned_card, scanned_card[0])
