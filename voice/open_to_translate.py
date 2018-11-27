# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import speech as sr
r = sr.Recognizer()
with sr.WavFile(sys.argv[1]) as source:              # use "test.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    print "You said:",  r.recognize(audio).encode('UTF-8')    # recognize speech using Google Speech Recognition
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")


"""
try:
    list = r.recognize(audio,True)                  # generate a list of possible transcriptions
    print("Possible transcriptions:")
    for prediction in list:
        print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")
"""
