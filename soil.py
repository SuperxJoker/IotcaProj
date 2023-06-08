import RPi.GPIO as GPIO
from time import sleep
from smbus import SMBus
import I2C_LCD_driver
import pyrebase
import random
import board


config = {

"apiKey": "AIzaSyBofJWJKXgM4iVzJSrCIc7hF-90KUehl0g",
"authDomain": "soilmoisturep.firebaseapp.com",
"databaseURL": "https://soilmoisturep-default-rtdb.firebaseio.com",
"storageBucket": "soilmoisturep.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

SENSOR_PIN = 27
WATER_PUMP = 13

DRY_VALUE = 1
WET_VALUE = 0

bus = SMBus(1)

#SENSOR SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

#WATER PUMP SETUP
GPIO.setup(WATER_PUMP, GPIO.OUT)

GPIO.output(WATER_PUMP, GPIO.LOW)



# Create a object for the LCD
lcd = I2C_LCD_driver.lcd()

# Starting text
lcd.lcd_display_string("System Loading",1,1)
for a in range (0,16):
lcd.lcd_display_string(".",2,a)
sleep(0.1)
lcd.lcd_clear()

def getSensorReadings():
    sensor_val = GPIO.input(SENSOR_PIN)
    print(sensor_val, end =" - ")

    sensor_per = 100 - ((sensor_val - WET_VALUE) * 100 / (DRY_VALUE - WET_VALUE))
    sensor_per = max(0,min(100, sensor_per))
    print(sensor_per)

    return sensor_per



def sendToFirebase(sensor_per):
    data = {
      "soil_percentage" : str(sensor_per)

  }
    db.child("Status").push(data)

    db.update(data)
    print("Sent to firebase")
    print(sensor_per)



while True:

    #GPIO.output(WATER_PUMP, GPIO.HIGH)
    sensor_per = getSensorReadings()

    lcd.lcd_display_string("Moisture:" + str(sensor_per) + "% " ,1,0)

    sendToFirebase(sensor_per)

    sleep(0.5)