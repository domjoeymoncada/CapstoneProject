import speech_recognition as sr
import DBHelper as db
import VoiceHelper as voice
import wave
import pyaudio
from playsound import playsound
from gtts import gTTS

pcode = 0


# indicator for naming the wav files
# 1 - lights on
# 2 - lights off
# 3 - open door
# 4 - close door

def registerVoice():
    global pcode
    f = open("code.txt", "w")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/greetings.mp3")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/getcode.mp3")
    statePCode()
    print pcode
    f.write(pcode)
    f.close()
    file = readNewDataCode()
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction.mp3")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/again.mp3")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction.mp3")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction_2.mp3")
    for i in range(0, 4):
        if i + 1 == 1:
            print ("Command for turning the lights on")
            #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/lightsOn.mp3")
        elif i + 1 == 2:
            print ("Command for turning the lights off")
            #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/lightsOff.mp3")
        elif i + 1 == 3:
            print ("Command for closing the door")
            # playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/closeDoor.mp3")
        elif i + 1 == 4:
            print ("Command for opening the door")
            # playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/openDoor.mp3")
        recordAudio(i + 1)

    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/tnx.mp3")
    #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/bye.mp3")
    db.upStatusCode(pcode)
    voice.convertToTextFile()
    return file


def readNewDataCode():
    f = open("code.txt", "r")
    file = f.read()
    f.close()
    return file


def addSpace(p_code):
    ret = p_code.replace("", " ")
    if ret.find("0"):
        ret = ret.replace("0", "ZERO!")
    return ret


def removeWhiteSpace(code):
    ret = code.replace(' ', '')
    return ret


def statePCode():
    global pcode
    for x in range(0, 1):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 7
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Say Code:")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("done recording")
        #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/donerec.mp3")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        r = sr.Recognizer()
        with sr.WavFile("output.wav") as source:  # use "test.wav" as the audio source
            audio = r.record(source)  # extract audio data from the file

        try:
            pcode = r.recognize_google(audio)
            pcode = removeWhiteSpace(pcode)

            exist = db.existPCode(pcode)
            if exist == None:
                retCode = addSpace(pcode)
                tts = gTTS(text="The code:" + str(retCode) + "doesn't exist. Please state code again", lang='en')
                tts.save("response/validation.mp3")
                #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/validation.mp3")
                statePCode()
            else:
                retCode = addSpace(pcode)
                tts = gTTS(text=str(retCode) + 'IS YOUR CODE?', lang='en')
                tts.save("response/code.mp3")
                #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/code.mp3")
                #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/option.mp3")

                optionPicker()
                # os.rename("output.wav", rename)
        except LookupError:  # speech is unintelligible
            print("Could not understand audio")


def recordAudio(indicatior):
    for x in range(0, 1):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 7
        if indicatior == 1:
            WAVE_OUTPUT_FILENAME = "1.wav"
        elif indicatior == 2:
            WAVE_OUTPUT_FILENAME = "2.wav"
        elif indicatior == 3:
            WAVE_OUTPUT_FILENAME = "3.wav"
        elif indicatior == 4:
            WAVE_OUTPUT_FILENAME = "4.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Say command")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("done recording")
        #playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/donerec.mp3")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


def optionPicker():
    for x in range(0, 1):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "option.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Yes or No")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        r = sr.Recognizer()
        with sr.WavFile("option.wav") as source:  # use "test.wav" as the audio source
            audio = r.record(source)  # extract audio data from the file

        try:
            rename = r.recognize_google(audio)
            print("Transcription: " + rename)  # recognize speech using Google Speech Recognition
            if (rename == "yes"):
                print ("rigth code")
            else:
                statePCode()
                # os.rename("output.wav", rename)
        except LookupError:  # speech is unintelligible
            print("Could not understand audio")