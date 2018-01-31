import mysql.connector
from mysql.connector import errorcode
import ResponseHelper as response
from datetime import datetime


# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(2, GPIO.OUT)


# 1 - lights on
# 2 - lights off
# 3 - close door
# 4 - open door

wattageArr = [20,0]

def checkDB(code):
    global cursor
    try:
            config = {
                'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
                'user': 'vaha',
                'password': 'capstone',
                'database': 'vahadb'
            }
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            query1 = "SELECT * FROM appliance where p_code=" + code + ";"
            cursor.execute(query1)
            for (a_id, a_name, a_type, a_state, p_code) in cursor:
                if a_type == 1:
                    if a_state == 2:
                        upStatusAppliance(a_id, p_code, a_type)
                        logOnViaVoice(p_code,a_id)
                        print ("state lights on")
                        # put lights on command here
                    elif a_state == 3:
                        downStatusAppliance(a_id, p_code, a_type)
                        logOffViaVoice()
                        calculateWattage(a_type)
                        print ("state lights off")
                        # put lights off command here

                if (a_type == 2):
                    if a_state == 2:
                        upStatusAppliance(a_id, p_code, a_type)
                        logOnViaVoice(p_code, a_id)
                        print ("state up door")
                    elif a_state == 3:
                        downStatusAppliance(a_id, p_code, a_type)
                        logOffViaVoice()
                        print ("state off door")

    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            checkDB(code)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")

        else:
            print(err)

    cursor.close()

def updateAppliance_Voice(pcode, atype, command, a_id):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "UPDATE appliace SET a_state = " + command + " WHERE p_code = " + pcode + " AND a_type = " + atype + ";"
        cursor.execute(query)
        cnx.commit()

        if command == 1:
            logOnViaVoice(pcode,a_id)
            if atype == 1:
              print "On light"
              #put command for lights on
            elif atype == 2:
              print "Open doors"
              #put command for open door
        elif command == 0:
            logOffViaVoice()
            if atype == 1:
                print "Off Light"
                calculateWattage(atype)
                #put command for lights off
            elif atype == 2:
                print "Close door"
                #put command for closing door


    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            updateAppliance_Voice(pcode,atype,command,a_id)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()


def getUserAppliance(pcode):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM appliance WHERE p_code =" + pcode + ";"
        cursor.execute(query)
        ret = cursor.fetchall()
        return ret
    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            getUserAppliance(pcode)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()


def readFileCode():
    f = open("code.txt", "r");
    file = f.read()
    return file


def downStatusAppliance(a_id, p_code, a_type):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "UPDATE appliance SET a_state = 0 WHERE p_code = " + str(p_code) + " AND a_id = " + str(
            a_id) + " AND a_type = " + str(a_type) + ";"
        cursor.execute(query)
        cnx.commit()
        # GPIO.output(2, 1)

    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            downStatusAppliance(a_id,p_code,a_type)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()


def upStatusAppliance(a_id, p_code, a_type):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "UPDATE appliance SET a_state = 1 WHERE p_code = " + str(p_code) + " AND a_id = " + str(
            a_id) + " AND a_type = " + str(a_type) + ";"
        cursor.execute(query)
        cnx.commit()
        # GPIO.output(2, 0)

    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            upStatusAppliance(a_id,p_code,a_type)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()


def logOffViaVoice():
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "SELECT u_id FROM logging ORDER BY u_id DESC LIMIT 1;"
        cursor.execute(query)
        log = cursor.fetchone()
        # add wattage to query
        query = "UPDATE logging SET u_end =  CURRENT_TIMESTAMP WHERE u_id = " + str(log[0]) + ";"
        cursor.execute(query)
        cnx.commit()
        #UPDATE logging SET u_end =  CURRENT_TIMESTAMP WHERE u_id = 12;"

    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            logOffViaVoice()
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()

def calculateWattage(a_type):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor, idx
    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM logging ORDER BY u_id DESC LIMIT 1;"
        cursor.execute(query)
        log = cursor.fetchone()
        #do math for wattage
        if a_type == 1:
            idx = 0
        elif a_type == 2:
            idx = 1

        wattage = wattageArr[idx]
        timeDif = log[2] - log[1]
        strTime = str(timeDif)
        (h,m,s) = strTime.split(":")
        result = float(h)*3600 + float(m)*60 + float(s)
        print result
        result = (result/60)/60
        print result
        upWatt = (wattage * result * 30)/1000.000
        print float(upWatt)


        query = "UPDATE logging SET u_wattage = "+str(upWatt)+" WHERE u_id = " + str(log[0]) + ";"
        cursor.execute(query)
        cnx.commit()

        # GPIO.output(2, 1)

    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST:
            print "continue checking DB"
            calculateWattage(a_type)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()



def logOnViaVoice(pcode, a_id):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO logging VALUES(null,CURRENT_TIMESTAMP(),null," + str(pcode) + "," + str(a_id) + ",null);"
        cursor.execute(query)
        cnx.commit()
        # GPIO.output(2, 0)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()


def existPCode(pcode):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM register_code WHERE rc_status = 0 AND rc_code = " + pcode + ";"
        cursor.execute(query)
        profile = cursor.fetchone()
        return profile

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def upStatusCode(pcode):
    config = {
        'host': 'vaha-capstone.cxi4v1yyl9po.us-east-2.rds.amazonaws.com',
        'user': 'vaha',
        'password': 'capstone',
        'database': 'vahadb'
    }
    cnx = mysql.connector.connect(**config)
    global cursor
    try:
        cursor = cnx.cursor()
        query = "UPDATE register_code SET rc_status = 1 WHERE rc_code = " + pcode + ";"
        cursor.execute(query)
        cnx.commit()


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor.close()