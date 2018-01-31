import DBHelper as db
import pyaudio
import wave
from playsound import playsound
import numpy as np
from scipy.io.wavfile import read
from python_speech_features import mfcc
from numpy.linalg import norm
from fastdtw import fastdtw


import time

a_id_lights = -1
a_id_doors = -1
light_state = -1 #status of the lights
door_state = -1 #status of the door
p_code = -1

def assignAppliance(pcode):
    global a_id_lights
    global a_id_doors
    global p_code
    global light_state
    global door_state
    p_code = pcode
    resultCursor = db.getUserAppliance(pcode)
    for row in resultCursor:
        if row[2] == 1:
            a_id_lights = row[0]
            light_state = row[3]
            print a_id_lights
        if row[2] == 2:
            a_id_doors = row[0]
            door_state = row[3]
            print a_id_doors

def doMath():
     i = 0
     print ("BOBO U:"+str(i))
     i+=1
     time.sleep(1)

def convertToTextFile():
    npy_array = []

    a = read("1.wav")
    b = read("2.wav")
    c = read("3.wav")
    d = read("4.wav")

    a_mfcc = mfcc(a[1])
    b_mfcc = mfcc(b[1])
    c_mfcc = mfcc(c[1])
    d_mfcc = mfcc(d[1])

    temp_obj1 = {
        'title': 'on',
        'value': a_mfcc
    }

    temp_obj2 = {
        'title': 'off',
        'value': b_mfcc
    }

    temp_obj3 = {
        'title': 'lock',
        'value': c_mfcc
    }

    temp_obj4 = {
        'title': 'unlock',
        'value': d_mfcc
    }

    npy_array.append(temp_obj1)
    npy_array.append(temp_obj2)
    npy_array.append(temp_obj3)
    npy_array.append(temp_obj4)

    np.save("conf", npy_array)


def compareAudio():
    conf = np.load("conf.npy")
    global storeCommand

    while True:
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print "recording..."
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print "finished recording"

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        inp = read("output.wav")
        inp_mfcc = mfcc(inp[1])

        min_value = []

        for compare in conf:
            dist, path = fastdtw(inp_mfcc, compare['value'], dist=lambda x, y: norm(x - y, ord=1))
            min_value.append(dist)
            # print "{} -> current audio: {}".format(compare['title'], dist)

        ans = np.argmin(min_value)
        obj_value = conf[ans]

        retval = obj_value['title']


        if retval == "on" and storeCommand != "on":
            db.updateAppliance_Voice(p_code, 1, 1, a_id_lights)
        elif retval == "off" and storeCommand != "off":
            db.updateAppliance_Voice(p_code, 1, 0, a_id_lights)
        elif retval == "lock" and storeCommand != "lock":
            db.updateAppliance_Voice(p_code, 2, 1, a_id_doors)
        elif retval == "unlock" and storeCommand != "unlock":
            db.updateAppliance_Voice(p_code, 2, 0, a_id_doors)

        storeCommand = retval
        print storeCommand