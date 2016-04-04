# coding: utf-8
"""
For RaspberryPi model A
"""

from time import sleep as psleep

from autobahn.twisted.wamp import Application
from autobahn.twisted.util import sleep
import wiringpi
import RPi.GPIO as GPIO


# RPi board pin header number
GPIO_GROUP1 = 24
GPIO_GROUP2 = 26
GPIO_GROUP3 = 16
GPIO_GROUP4 = 22
GPIO_PWM = 12

PWM_FREQUENCY = 80

STATE_NORMAL = 0
STATE_DEMO = 1

value = 0
state = STATE_DEMO
transition = False
led_all = [GPIO_GROUP1, GPIO_GROUP2, GPIO_GROUP3, GPIO_GROUP4]


def init():
    print 'init'
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PWM, GPIO.OUT)
    p = GPIO.PWM(GPIO_PWM, PWM_FREQUENCY)
    p.start(100)
    GPIO.output(GPIO_PWM, True)

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
    for grp in [GPIO_GROUP4, GPIO_GROUP3, GPIO_GROUP2, GPIO_GROUP1]:
        print 'pin %d off' % grp
        GPIO.output(grp, False)
        psleep(0.25)
    GPIO.output(GPIO_PWM, False)

    grp1_p = GPIO.PWM(GPIO_GROUP1, PWM_FREQUENCY)
    grp2_p = GPIO.PWM(GPIO_GROUP2, PWM_FREQUENCY)
    grp3_p = GPIO.PWM(GPIO_GROUP3, PWM_FREQUENCY)
    grp4_p = GPIO.PWM(GPIO_GROUP4, PWM_FREQUENCY)
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
    print 'realm joined'

    global state

    # setup hardware pwm using wiringpi
    wiringpi.wiringPiSetupPhys()
    wiringpi.pinMode(12, 2)
    wiringpi.pwmWrite(12, 1024)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_GROUP1, GPIO.OUT)
    GPIO.setup(GPIO_GROUP2, GPIO.OUT)
    GPIO.setup(GPIO_GROUP3, GPIO.OUT)
    GPIO.setup(GPIO_GROUP4, GPIO.OUT)
    grp1_p = GPIO.PWM(GPIO_GROUP1, PWM_FREQUENCY)
    grp2_p = GPIO.PWM(GPIO_GROUP2, PWM_FREQUENCY)
    grp3_p = GPIO.PWM(GPIO_GROUP3, PWM_FREQUENCY)
    grp4_p = GPIO.PWM(GPIO_GROUP4, PWM_FREQUENCY)
    grp1_p.start(0)
    grp2_p.start(0)
    grp3_p.start(0)
    grp4_p.start(0)
    GPIO.output(GPIO_GROUP1, True)
    GPIO.output(GPIO_GROUP2, True)
    GPIO.output(GPIO_GROUP3, True)
    GPIO.output(GPIO_GROUP4, True)

    while True:
        if state == STATE_DEMO:
            print 'demo mode'
            wiringpi.pwmWrite(12, 1024)

            # グループ1からグループ4まで点灯
            for grp_p in [grp1_p, grp2_p, grp3_p, grp4_p]:
                for d in range(0, 101):
                    grp_p.ChangeDutyCycle(d)
                    yield sleep(0.03)
                    if state != STATE_DEMO:
                        break
                if state != STATE_DEMO:
                    break
            sleep(2)

            for d in range(100, -1, -1):
                v = int((1024 / 100.0) * d)
                wiringpi.pwmWrite(12, d)
                yield sleep(0.005)

                if state != STATE_DEMO:
                    break
            for grp_p in [grp1_p, grp2_p, grp3_p, grp4_p]:
                grp_p.ChangeDutyCycle(0)

            yield sleep(2)

        elif state == STATE_NORMAL:
            for grp_p in [grp1_p, grp2_p, grp3_p, grp4_p]:
                grp_p.ChangeDutyCycle(100)
            v = int((1024 / 100.0) * value)
            wiringpi.pwmWrite(12, v)
            if state != STATE_NORMAL:
                break
            yield sleep(0.001)


@app.signal('onleaved')
def onleaved(*args):
    # TODO stop led driver
    print 'realm leaved'


@app.subscribe('cc.triplebottomline.led.state')
def on_state_changed(val):
    if 0 <= val <= 1:
        global state
        state = val


@app.subscribe('cc.triplebottomline.led.value')
def on_value_changed(val):
    if 0 <= val <= 100:
        global value, state
        value = val
        state = STATE_NORMAL


@app.register(u'cc.triplebottomline.led.getValue')
def get_value():
    global value
    return value


@app.register(u'cc.triplebottomline.led.getState')
def get_state():
    global state
    return state


if __name__ == '__main__':
    try:
        # init()
        app.run(u'ws://127.0.0.1:8080/ws', u'realm1')

    except KeyboardInterrupt:
        # GPIO.cleanup()
        pass
