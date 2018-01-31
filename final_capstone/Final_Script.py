import DBHelper as db
import RegisterHelper as register
import VoiceHelper as voice
import os
from threading import Thread


def readCode():
    global f
    if os.path.isfile("code.txt"):
        f = open("code.txt", "r")
        file = f.read()
        f.close()
        return file
    else:
        f = open("code.txt", "w")
        return register.registerVoice()

def FuncMain(pcode):
    while True:
        db.checkDB(pcode)
        voice.compareAudio()
        #voice.speakAndRecord()


if __name__ == "__main__":
    pcode = readCode()
    print pcode
    th1 = Thread(target=FuncMain(pcode),args=(1,))
    th1.setDaemon(True)
    th1.start()











