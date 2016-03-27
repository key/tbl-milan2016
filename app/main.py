# coding: utf-8
"""
For RaspberryPi model A
"""

from time import sleep
import RPi.GPIO as GPIO

control_frequency = 1000

pwm = 18
grp1 = 8
grp2 = 7
grp3 = 23
grp4 = 25

brightness0 = 0
brightness1 = 400
brightness2 = 700
brightness3 = 1023

led_all = [grp1, grp2, grp3, grp4]


def init():
  GPIO.cleanup([pwm] + led_all)

  # pwm
  GPIO.PWM(pwm, brightness0)

  # led out
  for grp in led_all:
    GPIO.setup(grp, GPIO.OUT)
    GPIO.output(grp, True)

  # 全灯(1s)
  wait = 1.0 / (brightness3 - brightness0)
  for brightness in range(0, 1024):
    GPIO.PWM(pwm, brightness)
    sleep(wait)

  # グループ4から1まで順に消灯(250ms/group)
  wait = 1.0 / 250
  for grp in [grp4, grp3, grp2, grp1]:
    GPIO.output(grp, False)
    sleep(wait)


def main() :
  init()

  while True:
    sleep(1.0 / target_brightness)


if __name__ = '__main__':
  main()
