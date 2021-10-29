#pip install adafruit-circuitpython-motorkit
#pip install pyrebase

from adafruit_motorkit import MotorKit
from gpiozero import Button
import time
import pyrebase
import board
from collections import OrderedDict

firebaseConfig = {
    "apiKey": "AIzaSyBXzcTWnqVKIty3m_5k3QCqbBPse4WmiJ8",
    "authDomain": "curtainapp-5caed.firebaseapp.com",
    "databaseURL": "https://curtainapp-5caed-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "curtainapp-5caed",
    "storageBucket": "curtainapp-5caed.appspot.com",
    "messagingSenderId": "724688145111",
    "appId": "1:724688145111:web:822d9b27a75b67a7053e92",
    "measurementId": "G-0LVN54PBQ4"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
kit = MotorKit(i2c=board.I2C())
openButton = Button(4)
closeButton = Button(17)
limitSwitchRight = Button(18)
limitSwitchLeft = Button(27)
state_ref = db.child("state")

while True:
    kit.motor1.throttle = 0
    while openButton.is_pressed or state_ref.child("motorState").get().val() == OrderedDict([('motorState', 'opening')]):
        print("opening")
        if not limitSwitchLeft.is_pressed or not limitSwitchRight.is_pressed:
            kit.motor1.throttle = -1.0

    kit.motor1.throttle = 0
    while closeButton.is_pressed or state_ref.child("motorState").get().val() == OrderedDict([('motorState', 'closing')]):
        print("closing")
        if not limitSwitchLeft.is_pressed or not limitSwitchRight.is_pressed:
            kit.motor1.throttle = 1.0

    if limitSwitchLeft.is_pressed:
        state_ref.child("curtainState").update({"curtainState":"closed"})

    if limitSwitchRight.is_pressed:
        state_ref.child("curtainState").update({"curtainState":"opened"})

    print(state_ref.child("motorState").get().val())
    print(type(state_ref.child("motorState").get().val()))

    time.sleep(0.1)
