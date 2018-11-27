from servos.Adafruit_PWM_Servo_Driver import PWM
"""
Move servos
pwm = PWM(0x40)
pwm.setPWMFreq(60)
pwm.setPWM(0, 0, 500)

"""

import time


class servos:
    pwm = PWM(0x40)
    pwm.setPWMFreq(60)

    def setPWM(self, servo, val, stop=True):
        """

        :param servo:
            0 head
            1 neck
            2 hand right 2
            3 hand left  3
            12 leg  left
            13 leg right
        :param val:
        :param stop:
        :return:
        """

        self.pwm.setPWM(servo, 0, val)
        if stop:
            time.sleep(.2)
            self.pwm.setPWM(servo, 0, 0)


    def head_up(self):
        self.setPWM(0, 630)

    def head_down(self):
        self.setPWM(0, 460)

    def head_center(self):
        self.setPWM(0, 560, False)
        time.sleep(3)
        self.setPWM(0, 560)

    def head_yes(self):
        #muve up
        for i in range(1,3):
            self.head_down()
            self.head_up()
            time.sleep(.1)
        self.head_up()


    def neck_left(self):
        self.setPWM(1, 580)

    def neck_right(self):
        self.setPWM(1, 340)

    def neck_center(self):
        self.setPWM(1, 430)

    def head_no(self):
        for i in range(1,3):
            self.neck_right()
            self.neck_left()
            time.sleep(.1)
        self.neck_center()

    def monitor(self):
        self.neck_right()
        #muve up
        for i in range(1,3):
            for x in range(330, 600, 10):
                self.setPWM(1, x)
                time.sleep(.1)
            for x in range(600, 330, -10):
                self.setPWM(1, x)
                time.sleep(.1)
            time.sleep(.5)
        self.neck_center()

    def hand_r_up(self):
        self.setPWM(2, 560)

    def hand_r_center(self):
        self.setPWM(2, 330)

    def hand_r_down(self):
        self.setPWM(2, 210)

    def hand_l_up(self):
        self.setPWM(3, 140)

    def hand_l_center(self):
        self.setPWM(3, 330)

    def hand_l_down(self):
        self.setPWM(3, 470)

    def macarena(self):
        self.hand_l_down()
        self.hand_r_down()
        self.head_down()
        self.leg_l_from()
        time.sleep(.5)
        self.leg_l_stop()
        self.hand_l_center()
        self.leg_r_from()
        time.sleep(.3)
        self.head_up()
        self.hand_r_center()
        time.sleep(.3)
        self.leg_r_stop()
        self.neck_right()
        self.hand_l_up()
        time.sleep(.3)
        self.hand_l_center()
        self.neck_left()
        self.hand_r_up()
        self.move_from()
        time.sleep(.3)
        self.move_back()
        time.sleep(.3)
        self.leg_l_stop()
        self.leg_r_stop()
        self.neck_center()
        self.hand_l_down()
        self.hand_r_down()
        self.head_center()

    def leg_r_from(self):
        self.setPWM(12, 500, False)

    def leg_l_from(self):
        self.setPWM(13, 100, False)

    def leg_r_stop(self):
        self.setPWM(12, 0, False)

    def leg_l_stop(self):
        self.setPWM(13, 0, False)

    def leg_r_back(self):
        self.setPWM(12, 100, False)

    def leg_l_back(self):
        self.setPWM(13, 500, False)

    def move_from(self):
        self.leg_r_from()
        self.leg_l_from()

    def move_back(self):
        self.leg_r_back()
        self.leg_l_back()




