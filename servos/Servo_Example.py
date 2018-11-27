#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  print "%d pulse" % pulse
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
    # Change speed of continuous servo on channel O
    pwm.setPWM(14, 0, 140)
    time.sleep(1)
    pwm.setPWM(14, 0, 580)
    time.sleep(2)
    pwm.setPWM(15, 0, 570)
    time.sleep(1)
    pwm.setPWM(15, 0, 140)
    time.sleep(2)


 while True:
     pwm.setPWM(15, 0,640)
     pwm.setPWM(15, 0,540)


for x in range(1,10):
    pwm.setPWM(0,0,)
