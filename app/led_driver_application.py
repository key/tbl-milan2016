# coding: utf-8
"""
For RaspberryPi model A
"""

import RPi.GPIO as GPIO
from time import sleep as psleep

from autobahn.twisted.wamp import Application


GRP1 = 24
GRP2 = 26
GRP3 = 16
GRP4 = 22
PWM = 12
PWM_FREQUENCY = 80

STATE_NORMAL = 0
STATE_DEMO = 1

value = 0
state = STATE_DEMO
transition = False
led_all = [GRP1, GRP2, GRP3, GRP4]


def init():
    print 'init'
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PWM, GPIO.OUT)
    p = GPIO.PWM(PWM, PWM_FREQUENCY)
    p.start(100)
    GPIO.output(PWM, True)

    # グループ1からグループ4まで点灯
    for grp in led_all:
        print 'pin %d on' % grp
        GPIO.setup(grp, GPIO.OUT)
        GPIO.output(grp, True)
        psleep(0.25)

    # 点滅
    for x in range(0, 2):
        p.ChangeDutyCycle(0)
        psleep(0.2)
        p.ChangeDutyCycle(100)
        psleep(0.2)

    for b in range(100, -1, -1):
        p.ChangeDutyCycle(b)
        psleep(0.01)

    psleep(0.2)

    for b in range(0, 101):
        p.ChangeDutyCycle(b)
        psleep(0.01)

    # グループ4から1まで消灯
    for grp in [GRP4, GRP3, GRP2, GRP1]:
        print 'pin %d off' % grp
        GPIO.output(grp, False)
        psleep(0.25)
    GPIO.output(PWM, False)

    grp1_p = GPIO.PWM(GRP1, PWM_FREQUENCY)
    grp2_p = GPIO.PWM(GRP2, PWM_FREQUENCY)
    grp3_p = GPIO.PWM(GRP3, PWM_FREQUENCY)
    grp4_p = GPIO.PWM(GRP4, PWM_FREQUENCY)
    grp1_p.start(0)
    grp2_p.start(0)
    grp3_p.start(0)
    grp4_p.start(0)

    for b in range(0, 101):
        grp1_p.ChangeDutyCycle(b)
        grp2_p.ChangeDutyCycle(b)
        grp3_p.ChangeDutyCycle(b)
        grp4_p.ChangeDutyCycle(b)
        psleep(0.03)

    for b in range(100, -1, -1):
        grp1_p.ChangeDutyCycle(b)
        grp2_p.ChangeDutyCycle(b)
        grp3_p.ChangeDutyCycle(b)
        grp4_p.ChangeDutyCycle(b)
        psleep(0.03)

    print 'initialize done'


app = Application(u'cc.triplebottomline')


@app.signal('onjoined')
def onjoined(*args):
    # TODO start led driver
    print 'realm joined'


@app.signal('onleaved')
def onleaved(*args):
    # TODO stop led driver
    print 'realm leaved'


@app.subscribe('cc.triplebottomline.led.state')
def on_state_changed(val):
    if 0 <= val <= 1:
        global state
        state = val
        print 'currentState: %d' % state
        print('Received an event with something: %d' % val)


@app.subscribe('cc.triplebottomline.led.value')
def on_value_changed(val):
    if 0 <= val <= 100:
        global value
        value = val
        print 'currentValue: %d' % value
        print('Received an event with something: %d' % val)


@app.register(u'cc.triplebottomline.led.getValue')
def get_value():
    global value
    print 'currentValue: %d' % value
    return value


@app.register(u'cc.triplebottomline.led.getState')
def get_state():
    global state
    print 'currentState: %d' % value
    return state


if __name__ == '__main__':
    try:
        init()
        app.run(u'ws://127.0.0.1:8080/ws', u'realm1')

    except KeyboardInterrupt:
        # GPIO.cleanup()
        pass
