# -*- coding: utf-8 -*-
#!/usr/bin/env python


# Módulos
import re
import os
import time
import pickle
from random import randint
import datetime
import unicodedata
import goslate

import pygame
from pygame.locals import *

import pyaudio
# VOICE TO TEXT
import voice as sr
# WOLFRAM QUERYS
from wolfram import query_wolfram
# TEXTO TO SPEACH
from espeak import espeak

# SENSORS
from sensors.Adafruit_DHT.temp import temperature
# PIR
import RPi.GPIO as io

# MOTORS
from servos.moves import servos

# Constantes

#PIR SENSOR
io.setmode(io.BCM)
pir_pin =18
io.setup(pir_pin, io.IN)

#SHARP PROXIMITY
pin_sharp = 17
io.setup(pin_sharp, io.IN)

#LEDS PINS
led_r = 26
lef_l = 21

io.setup(led_r, io.OUT)
io.setup(lef_l, io.OUT)

#principal bottom

pin_button = 20
io.setup(pin_button, io.IN)



#espak defaul
espeak.set_voice('es-la')
espeak.set_parameter(espeak.Parameter.Range, 40)

# init values
data = {
        'birthday': '18/1/2015',
        'mother': 'Barbara Martinez',
        'father': 'Hernan Pazos',
        'name': 'wali',
        }
file = open('config.txt', 'w')
pickle.dump(data, file)
file.close()


# Clases
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
 
# Funciones
# ---------------------------------------------------------------------


def eyes(status):
    io.output(led_r, status)
    io.output(lef_l, status)


def strip_accents(s):
    print 'lo que dijo %s' % s
    print type(s)
    if isinstance(s, unicode):
        v = s
    else:
        v = unicode(s, 'utf-8')
    nkfd_form = unicodedata.normalize('NFKD', v)
    return ''.join(c for c in nkfd_form if not unicodedata.combining(c))


def c_w(string, words, operator='or'):
    s = strip_accents(string)
    w = strip_accents(words)
    #print '%s in %s' % (w, s)
    if operator == 'or':
        if any(x in s for x in w.split()):
           return True
        else:
           return False
    else:
        if all(x in s for x in w.split()):
            return True
        else:
            return False

def espeak_not_playing():
    print 'Waiting espeak!'
    while espeak.is_playing():
        # print 'playiando'
        if not espeak.is_playing():
            time.sleep(1)
            return False
    return True

def voice_to_text():
    r = sr.Recognizer()
    m = sr.Microphone(device_index=2)
    #eyes(True)
    print 'ESCUCHANDO'
    with m as source:
       audio = r.listen(source, timeout=40)
    print "Vamos a reconocer la voz."
    try:
        #eyes(False)
        words = r.recognize(audio).encode('utf-8')
        return words
    except LookupError:
        #eyes(False)
        return False

def actiones(words):
    if c_w(words,'años tienes', 'and'):
        now_year = int(datetime.date.today().year)
        file = open('config.txt', 'r')
        data = pickle.load(file)
        date_year = int(data.get('birthday').split('/')[2])
        nac = now_year - date_year
        espeak.synth('tengo %s años de edad' % str(nac))
        espeak_not_playing()
        main()

    elif c_w(words,'cumpleaños cumple fecha nacimiento'):
        file = open('config.txt', 'r')
        data = pickle.load(file)
        cumple = data.get('birthday').split('/')
        file.close()
        espeak.synth('Mi cumpleaños es el %s, de %s, del %s' % (cumple[0], cumple[1], cumple[2]))
        espeak_not_playing()
        main()

    elif c_w(words, 'mamá', 'and'):
        file = open('config.txt', 'r')
        data = pickle.load(file)
        mother = data.get('mother')
        file.close()
        espeak.synth('Mi mamá es,%s' % mother)
        espeak_not_playing()
        main()

    elif c_w(words, 'conoces a jacobo', 'and'):
        espeak.synth('Si es un chamaquito muy bien portado')
        espeak_not_playing()
        main()

    elif c_w(words,'como llamas', 'and'):
        file = open('config.txt', 'r')
        data = pickle.load(file)
        name = data.get('name')
        file.close()
        espeak.synth('Mi nombre es,  %s' % name)
        espeak_not_playing()
        main()

    elif c_w(words,'quien papá', 'and'):
        file = open('config.txt', 'r')
        data = pickle.load(file)
        father = data.get('father')
        file.close()
        espeak.synth('Mi papá, %s' % father)
        espeak_not_playing()
        main()

    elif c_w(words,'arriba manos', 'and'):
        s.hand_l_up()
        s.hand_r_up()
        espeak_not_playing()
        main()

    elif c_w(words,'abajo manos', 'and'):
        s.hand_l_down()
        s.hand_r_down()
        espeak_not_playing()
        main()

    elif c_w(words,'bailas bailar macarena'):
        s.macarena()
        time.sleep(8)
        main()

    elif c_w(words,'temperatura', 'and'):
        temp = temperature()
        espeak.synth(temp)
        espeak_not_playing()
        main()

    elif c_w(words,'estas enojado', 'and'):
        s.head_no()
        espeak.synth('no estoy enojado')
        espeak_not_playing()
        main()

    elif c_w(words,'estas contento', 'and'):
        s.head_yes()
        espeak.synth('si estoy contento')
        espeak_not_playing()
        main()

    elif c_w(words,'mira arriba', 'and'):
        s.head_up()
        time.sleep(1)
        main()

    elif c_w(words,'mira abajo', 'and'):
        s.head_dowm()
        time.sleep(1)
        main()

    elif c_w(words,'mira izquierda', 'and'):
        s.neck_left()
        time.sleep(1)
        main()

    elif c_w(words,'mira derecha', 'and'):
        s.neck_right()
        time.sleep(1)
        main()

    elif c_w(words,'mira centro', 'and'):
        s.neck_center()
        s.head_center()
        time.sleep(1)
        main()

    #funciones de  la camara
    elif c_w(words,'foto selfie fotogradfia'):
        espeak.synth('Te voy a tomar la foto a la de 3,')
        espeak_not_playing()
        for x in range(1,4):
            espeak.synth(str(x))
            espeak_not_playing()
            time.sleep(1)
        os.system('fswebcam -r 1200x1000 -S 10 --jpeg 100 --save /home/pi/src/walle/sensors/PIR/images/%H%M%S.jpg')
        espeak.synth('Listo!, he tomado la foto')
        espeak_not_playing()
        main()

    elif c_w(words,'transmite video ', 'and'):
        espeak.synth('Voy a empezar a tramsmitir  video lo puedes ver desde mi ip')
        espeak_not_playing()
        #aqui va el comando para empezar a  hacer el streamen
        os.system('')
        espeak.synth('Listo!, he ya puedes ver lo que estoy viendo')
        espeak_not_playing()

        while True :
            if io.input(pin_button):
                break
            else:
                s.monitor()
        main()

    elif c_w(words,'traducir'):
        to_translate = words.split()[1:]
        to_translate = ' '.join(c for c in to_translate)
        gs = goslate.Goslate()
        translate = gs.translate(to_translate, 'en')
        espeak.set_voice('en/en-n')
        espeak.synth(translate)
        espeak.set_voice('es-la')
        espeak_not_playing()
        main()

    elif c_w(words,'como se dice', 'and'):
        to_translate = words.split(' ')[3:][:-2]
        to_translate = ' '.join(c for c in to_translate)
        print 'voy a pasar a traducir %s' % to_translate
        gs = goslate.Goslate()
        translate = gs.translate(to_translate, 'en')
        print 'texto traducirdo %s' % translate
        espeak.set_voice('en')
        espeak.set_parameter(espeak.Parameter.Rate, 140)
        espeak.synth(translate)
        espeak_not_playing()
        main()

    elif c_w(words,'informacion de', 'and') or c_w(words,'cual es', 'and') or c_w(words,'cuanto es', 'and') or c_w(words,'quien es', 'and'):
        to_translate = words.split(' ')[2:]
        to_translate = ' '.join(c for c in to_translate)
        print 'voy a pasar a traducir %s' % to_translate
        gs = goslate.Goslate()
        translate_to_en = gs.translate(to_translate, 'en')
        print 'texto traducido %s' % translate_to_en
        info = query_wolfram(translate_to_en)
        translate_to_es = gs.translate(info, 'es').encode('utf-8')
        espeak.synth(translate_to_es.replace('|',': ').replace('\n',' '))
        espeak_not_playing()
        main()

    elif c_w(words,'camina adelante', 'or'):
        espeak.synth('Voy a caminar hasta llegar a la pared')
        espeak_not_playing()
        s.move_from()

        # mientras no detecte una senal del sensor sigue avanzando
        while True:
            if io.input(pin_sharp):
                espeak.synth('LLegue a la pared')
                espeak_not_playing()
                break

        s.move_back()
        time.sleep(4)
        s.move_back()
        time.sleep(4)
        s.leg_l_stop()
        time.sleep(4)
        s.leg_r_stop()
        main()

    elif c_w(words,'que hora', 'and') :
        espeak.synth('Son las %s con %s' % (datetime.datetime.now().time().hour, datetime.datetime.now().time().minute))
        espeak_not_playing()
        main()

    else:
        text_r = ['No se que significa:', 'No se quieres decir con:', 'No se que es:', 'No entendi:' ]
        espeak.synth('%s, %s' % (text_r[randint(0, len(text_r)-1)], words ))
        print 'texto reconocido: %s' % words
        espeak_not_playing()
        main()


# ---------------------------------------------------------------------
 
def main():
    espeak.set_voice('es-la')
    #led on
    while True:
        if io.input(pir_pin):
            if io.input(pin_button):
                print 'Button a!'
            else:
                try:
                    words = voice_to_text()
                    print 'here!'
                    if words:
                        actiones(words)
                    else:
                        pass
                        #text = ['No entendi', 'Dilo mas fuerte!', 'No entiendo lo que dices',  'No entiendo nada', 'Puedes hablar un poquito mas fuerte', 'No se que estas diciendo!']
                        #espeak.synth(text[randint(0, len(text)-1)])
                        #espeak_not_playing()
                except KeyError:
                    eyes(False)
                    print 'Time Out'
                except IOError:
                    print 'Se presento un error  de i/o'
                    time.sleep(2)
                    eyes(False)

if __name__ == '__main__':
    print 'Listo!'
    #espeak.synth('Puedes preguntarme mi edad, quienes son mis papas.')
    #espeak.synth('Puedes Pedirme que te tome una foto, que baile.')
    #espeak.synth('Tambien puedes  pedirme que traduzca a ingles alguna flase o palabra, diciendome')
    #espeak.synth('Como se dice buenos dias  en ingles')
    #espeak.synth('Me puedes preguntar sobre tus  artistas favoritos  diciendo  por ejemplo: quien es Michael Jackson')
    espeak_not_playing()
    s = servos()
    main()

