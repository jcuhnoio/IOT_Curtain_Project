from adafruit_motorkit import MotorKit
import board

kit = MotorKit(i2c=board.I2C())
kit.motor1.throttle = 0
