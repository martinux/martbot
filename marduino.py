import time, serial

try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
except:
    print("Can't find the serial connection!")
    ser = None

commands = {"on":["o"],
            "off":["n"], 
            "up":["u"], 
            "down":["d"],
            "1":["!"], 
            "2":["@"], 
            "scroll":["s"], 
            "clear":["^"], 
            "light":["U"], 
            "dark":["D"]
            }

def connector():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    return ser
    
    
def output(msg, user):
    if ser == None:
        if msg == "conn":
            ser = connector()
        msg = ["An LCD is not connected at this time."]
        return msg
        
    temp = ""
    try:
        temp, out = msg.split(' ', 1)
        if temp == "1":
            arduino_string = "!" + out
            ser.write(arduino_string)
            msg = "Line one is now: %s" % out
        elif temp == "2":
            arduino_string = "@" + out
            ser.write(arduino_string)
            msg = "Line two is now: %s" % out
    except:
        print("msg in is not a line!")
        
    if msg in commands.keys():
        print("A message was found for marduino: %s\n" % msg)
        
    if msg == "on":
        ser.write("o")
        msg = "I'm turning the backlight up to max brightness, %s" % user
    elif msg == "off":
        ser.write("n")
        msg = "I'm turning the backlight off, %s" % user
    elif msg == "scroll":
        ser.write("s")
        msg = "scrolling message!"
    elif msg == "up":
        ser.write("u")
        msg = "I'm turning the contrast up, %s" % user
    elif msg == "down":
        ser.write("d")
        msg = "I'm turning the contrast down, %s" % user
    elif msg == "light":
        ser.write("U")
        msg = "I'm turning the backlight brightness up, %s" % user
    elif msg == "dark":
        ser.write("D")
        msg = "I'm turning the backlight brightness down, %s" % user
    elif msg == "clear":
        ser.write("^")
        msg = "Screen cleared!"
    elif msg == "test":
        test()
    return [msg]

def test():
    status = "0"
    print("sending")
    ser.write("c")
    try:
        status = ser.read(1)
        print(status)
    except:
        print("Test failed!")
    if status != "1":
        ser.close()
        ser = serial.Serial('/dev/ttyACM0', 9600)
    else:
        print("Still alive! %d\n" % time.time())
    
    return

if __name__ == "__main__":
    while True:
        status = "0"
        time.sleep(10)
        print("sending")
        ser.write("c")
        status = ser.read(1)
        print(status)
        if status != "1":
            ser.close()
            ser = serial.Serial('/dev/ttyACM0', 9600)
        else:
            print("Still alive! %d\n" % time.time())
