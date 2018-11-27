from multiprocessing import Process
import threading
import os

from flask import Flask, render_template, Response
import RPi.GPIO as io
from video.camera_pi import Camera

from servos.moves import servos

app = Flask(__name__)

# SETUP

# SERVOS
s = servos()
s.alloff()

# PIR SENSOR
io.setmode(io.BCM)
pir_pin = 18
io.setup(pir_pin, io.IN)

# SHARP PROXIMITY
pin_sharp = 17
io.setup(pin_sharp, io.IN)

# LEDS PINS
led_r = 26
lef_l = 21

#io.setup(led_r, io.OUT)
#io.setup(lef_l, io.OUT)


def proximity_stop():
    while True:
        if io.input(pin_sharp):
            print('Stop')
            s.stop()
            break


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/alloff/')
def alloff():
    s.alloff()
    return render_template('index.html')


# MOVES
@app.route('/moves/<action>/')
def moves(action):
    if action == 'front':
        p = Process(target=s.move_from())
        p.start()
    elif action == 'back':
        p = Process(target=s.move_back())
        p.start()
    elif action == 'left':
        p1 = Process(target=s.leg_l_stop())
        p1.start()
        p2 = Process(target=s.leg_r_from())
        p2.start()
    elif action == 'right':
        p1 = Process(target=s.leg_r_stop())
        p1.start()
        p2 = Process(target=s.leg_l_from())
        p2.start()
    elif action == 'stop':
        p = Process(target=s.stop())
        p.start()
    elif action == 'circle':
        p1 = Process(target=s.leg_l_from())
        p1.start()
        p2 = Process(target=s.leg_r_back())
        p2.start()

    elif action == 'front_sensor':
        p1 = Process(target=s.move_from())
        p1.start()
        proximity = threading.Thread(target=proximity_stop())
        proximity.start()

    return render_template('index.html')


# hands
@app.route('/hands/<action>/')
def hands(action):
    if action == 'up':
        p = Process(target=s.hands_up())
        p.start()
    elif action == 'down':
        p = Process(target=s.hands_down())
        p.start()
    elif action == 'open':
        p = Process(target=s.hands_open())
        p.start()
    elif action == 'aplaudir':
        p = Process(target=s.hands_aplaudir())
        p.start()
    elif action == 'mentada':
        p = Process(target=s.hands_mentada())
        p.start()
    return render_template('index.html')


# LEFT HAND
@app.route('/hang_left/<action>/')
def hand_l(action):
    if action == 'up':
        s.hand_l_up()
    elif action == 'down':
        s.hand_l_down()
    elif action == 'center':
        s.hand_l_elbow_up()
        s.hand_l_center()
    elif action == 'left':
        s.hand_l_elbow_center()
    elif action == 'right':
        s.hand_l_elbow_up()
    elif action == 'up_manual':
        s.hand_l_up_manual()
    elif action == 'down_manual':
        s.hand_l_down_manual()
    elif action == 'up_elbow_manual':
        s.hand_l_elbow_up_manual()
    elif action == 'down_elbow_manual':
        s.hand_l_elbow_down_manual()


    return render_template('index.html')


# RIGHT HAND
@app.route('/hang_right/<action>/')
def hand_r(action):
    if action == 'up':
        p = Process(target=s.hand_r_up())
        p.start()
    elif action == 'down':
        p = Process(target=s.hand_r_down())
        p.start()
    elif action == 'center':
        p = Process(target=s.hand_r_elbow_up())
        p.start()
        p = Process(target=s.hand_r_center())
        p.start()
    elif action == 'left':
        p = Process(target=s.hand_r_elbow_up())
        p.start()
    elif action == 'right':
        p = Process(target=s.hand_r_elbow_center())
        p.start()


    return render_template('index.html')


# HEAD
@app.route('/head/<action>/')
def head(action):
    if action == 'up':
        p = Process(target=s.head_up())
        p.start()

    elif action == 'down':
        p = Process(target=s.head_down())
        p.start()

    elif action == 'center':
        p1 = Process(target=s.head_center())
        p2 = Process(target=s.neck_center())
        p1.start()
        p2.start()

    elif action == 'left':
        p = Process(target=s.neck_left())
        p.start()

    elif action == 'right':
        p = Process(target=s.neck_right())
        p.start()

    elif action == 'off':
        p = Process(target=s.head_off())
        p.start()

    elif action == 'yes':
        p = Process(target=s.head_yes())
        p.start()

    elif action == 'no':
        p = Process(target=s.head_no())
        p.start()

    elif action == 'up_manual':
        p = Process(target=s.head_manual_up())
        p.start()
    elif action == 'down_manual':
        p = Process(target=s.head_manual_down())
        p.start()

    elif action == 'left_manual':
        p = Process(target=s.neck_manual_left())
        p.start()

    elif action == 'right_manual':
        p = Process(target=s.neck_manual_right())
        p.start()

    return render_template('index.html')


# SENSORS
@app.route('/sensors/<type>/')
def sensors(type):
    pass
    return render_template('index.html', msg=temp)

# AMENITIES
@app.route('/actions/<type>/')
def actions(type):

    if type == 'foto':
        os.system('fswebcam -r 1200x1000 -S 10 --jpeg 100 --save /home/pi/src/walle/sensors/PIR/images/%H%M%S.jpg')
    return render_template('index.html', msg='Se tomo la foto')


#video

@app.route('/video/')
def video():
    return render_template('video.html')

def gen(camera):

    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    p = Process(target=s.hands_open())
    p.start()
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.25')
