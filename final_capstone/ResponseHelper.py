from gtts import gTTS
from playsound import playsound
import RegisterHelper as register

import mysql.connector
from mysql.connector import errorcode
from time import time

sampArr = [10,20,30]
wattageArr = [20,0]

string = "hello"

def sample():
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction.mp3")
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/again.mp3")
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction.mp3")
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/instruction_2.mp3")
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/tnx.mp3")
    playsound("C:/Users/Owner/PycharmProjects/final_capstone/response/bye.mp3")


def sample1():
    global string
    string = string+" world"


def sample3():
    toPrint = string
    print toPrint






if __name__ == "__main__":
   # calculateWattage(1)
    sample1()
    sample3()
