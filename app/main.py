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

brightness0 = 0.5
brightness1 = 400
brightness2 = 700
brightness3 = 1023

led_all = [grp1, grp2, grp3, grp4]


def init():
  print 'init'
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pwm, GPIO.OUT)
  p = GPIO.PWM(pwm, brightness3)
  p.start(100)
  GPIO.output(pwm, True)

  # グループ1からグループ4まで点灯
  for grp in led_all:
    print 'pin %d on' % grp
    GPIO.setup(grp, GPIO.OUT)
    GPIO.output(grp, True)
    sleep(0.25)

  # 点滅
  for x in range(0, 2):
    p.ChangeDutyCycle(0)
    sleep(0.2)
    p.ChangeDutyCycle(100)
    sleep(0.2)

  for b in range(100, -1, -1):
    p.ChangeDutyCycle(b)
    sleep(0.01)
  for b in range(0, 101):
    p.ChangeDutyCycle(b)
    sleep(0.01)

  # グループ4から1まで順に消灯
  for grp in [grp4, grp3, grp2, grp1]:
    print 'pin %d off' % grp
    GPIO.output(grp, False)
    sleep(0.25)
  GPIO.output(pwm, False)

  print 'initialize done'


demo = False


def main() :
  init()


  while True:
    break
    # TODO デモモードの分岐
    if demo:
      pass
    else:
      pass


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    GPIO.cleanup()
