# coding: utf-8
"""
For RaspberryPi model A
"""

from time import sleep
import RPi.GPIO as GPIO

control_frequency = 1000

pwm = 12
grp1 = 24
grp2 = 26
grp3 = 16
grp4 = 22

brightness0 = 1
brightness1 = 400
brightness2 = 700
brightness3 = 1023

led_all = [grp1, grp2, grp3, grp4]


def init():
  GPIO.setmode(GPIO.BOARD)

  # pwm
  GPIO.setup(pwm, GPIO.OUT)
  GPIO.output(pwm, True)
  GPIO.PWM(pwm, brightness0)

  # led out
  for grp in led_all:
    sleep(0.25)
    GPIO.setup(grp, GPIO.OUT)
    GPIO.output(grp, True)

  # 全灯(1s)
  wait = 1.0 / (brightness3 - brightness0)
  for brightness in range(1, 1024):
    GPIO.PWM(pwm, brightness)
    sleep(wait)

  # グループ4から1まで順に消灯(250ms/group)
  wait = 1.0 / 250
  for grp in [grp4, grp3, grp2, grp1]:
    GPIO.output(grp, False)
    sleep(wait)


def main() :
  init()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    GPIO.cleanup()
