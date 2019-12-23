import RPi.GPIO as GPIO
import MFRC522
import signal
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
            #print(c, "LOW")

io = [[15,"1071402628"], [11,"9024615418"], [13,None]]
for c,i in io:
    GPIO.setup(c, GPIO.OUT)

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

    # If a card is found
    if status == MIFAREReader.MI_OK:
        #card detected
        pass
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        bump(scanned_card, "%s%s%s%s" % (uid[0], uid[1], uid[2], uid[3]))
        if dif(scanned_card):
            print(scanned_card[0])
        #print(scanned_card[0])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        bad_count = 0
        
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            #auth fail
            pass
    else:
        bad_count += 1
        if bad_count >= 5:
            bump(scanned_card, None)


while True:
    rfid()
    if dif(scanned_card):
        for c,i in io:
            if i == scanned_card[0]:
                print(c)
                GPIO.output(c,GPIO.HIGH)
                disable(io, exceptions=[c])
                bump(scanned_card, i)
                break
            
