#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(11, 12, 7, 8, 9, 10);

int backlight = 6;      // backlight pin
int cur_brightness = 100;  // Default brightness value
int bright_change = 50;  // Brightness change step size
int contrast = 5;       // contrast pin
int cur_contrast = 50;  // Default contrast value
int contrast_change = 10; // Contrast change step size

int incomingByte = 0;   // for incoming serial data

// LCD output
int bufferArray[250];     // Our array to store characters arriving from serial port.
int output = 0;
int buf_size[3] = {0, 0};  // Buffer size - two lines.
int i = 0;

void setup() {
    // set up the LCD's number of columns and rows: 
    lcd.begin(16, 2);
    
    pinMode(backlight, OUTPUT);
    pinMode(contrast, OUTPUT);
    analogWrite(backlight, 250);
    // set default contrast
    analogWrite(contrast, cur_contrast);
    delay(500);
    lcd.print("Hello!");
    Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
    delay(5000);
    lcd.clear();
    analogWrite(backlight, cur_brightness);
}

void loop() {
  int count = Serial.available();

    if (Serial.available() > -1) {
        delay(1000);
        for (i=0; i<count ; i++) {
           bufferArray[i] = Serial.read();          // Put into array
           output = 1;                              // Show new data has been recieved
        }
        //Serial.print("Buffer 1: "); Serial.println(buf_size[0]);
        //Serial.print("Buffer 2: "); Serial.println(buf_size[1]);
        //Serial.print("Character count: ");Serial.println(count);
    }
    
    int msg = 0;
    if (output != 0) {                      // If new bytes have been recieved                
        int position = 0;
        if (bufferArray[0] == '!') {        // Print on first line if message begins with '!'
            lcd.clear();
            lcd.setCursor(0,0);
            position = 1;
            buf_size[0] = count;               // Keep track of how big the last message was.
            msg = 1;
        } 
        else if (bufferArray[0] == '@') {   // Print on second line if message begins with '@'
            lcd.setCursor(0,1);
            position = 1;
            buf_size[1] = count;
            msg = 1;
        }
        else if (bufferArray[0] == '^') {   // Clear screen if message begins with '^'
            lcd.clear();
            buf_size[0] = 0; buf_size[1] = 0;
            lcd.setCursor(0,0);
            position = 1;
        }
        else if (bufferArray[0] == 's') {
            int scroll_n;
            if (buf_size[0] > buf_size[1]) {  // Determine which line is longer.
                scroll_n = buf_size[0];
            }
            else {
                scroll_n = buf_size[1];
            }
            // Use longer line as number of chars to scroll.
            for (int positioncounter = 0; positioncounter < scroll_n; positioncounter++) {
                lcd.scrollDisplayLeft();
                delay(300);
            }
            for (int positioncounter = 0; positioncounter < scroll_n; positioncounter++) {
                lcd.scrollDisplayRight();
                delay(300);
            }
        }
        else if (bufferArray[0] == 'u') {       // Contrast up
            cur_contrast = cur_contrast - contrast_change;
            if (cur_contrast > 0 && cur_contrast < 90) {
                analogWrite(contrast, cur_contrast);
                //Serial.print("contrast: ");
                //Serial.println(cur_contrast, DEC);
            }
        }
        else if (bufferArray[0] == 'd') {       // Contrast down
            cur_contrast = cur_contrast + 10;
            if (cur_contrast > 0 && cur_contrast < 90) {
                analogWrite(contrast, cur_contrast);
                //Serial.print("contrast: ");
                //Serial.println(cur_contrast, DEC);
            }
        }
        else if (bufferArray[0] == 'o') {       // Backlight on
            analogWrite(backlight, 250);
            cur_brightness = 250;
        }
        else if (bufferArray[0] == 'n') {       // Backlight off
            analogWrite(backlight, 0);
            cur_brightness = 0;
        }
        else if (bufferArray[0] == 'U') {       // Backlight up
            cur_brightness = cur_brightness + bright_change;
            if (cur_brightness > -1 && cur_brightness < 251) {
                analogWrite(backlight, cur_brightness);
                //Serial.print("brightness: ");
                //Serial.println(cur_brightness, DEC);
            }
            else {
                cur_brightness = cur_brightness - bright_change;
            }
        }
        else if (bufferArray[0] == 'D') {       // Backlight down
            cur_brightness = cur_brightness - bright_change;
            if (cur_brightness > -1 && cur_brightness < 251) {
                analogWrite(backlight, cur_brightness);
                //Serial.print("brightness: ");
                //Serial.println(cur_brightness, DEC);
            }
            else {
                cur_brightness = cur_brightness + bright_change;
            }
        }
        else if (bufferArray[0] == 'c') {       // ping
            Serial.write("1");
        }
        else {
            lcd.clear();
            lcd.setCursor(0,0);
        }
        int j;
        //Serial.print("msg is size: "); Serial.println(count);
        if (msg == 1) {
            for (j = position; j < count; j++) {
                lcd.write(bufferArray[j]);
            }
        }
        output = 0;                               // Don't print on next iteration
        memset(bufferArray, 0, count);
        count = 0;
    }
}
