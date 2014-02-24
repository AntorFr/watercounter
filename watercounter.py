#!/usr/bin/env python

import pifacedigitalio
import MySQLdb
from threading import Timer

water = 0

def createwaterrecord(value):
    global water

    try :
       db = MySQLdb.connect(host="rsp03",
                         user="timelogger",
			 passwd="timelogger",
                         db = "timelogger" )
 
       sql = """INSERT INTO logger (dID,
             value, unit)
             VALUES ('1', %(value)d, 'L') ON DUPLICATE KEY UPDATE value=value+%(value)d;""" % {"value": value}
       cursor = db.cursor()
       cursor.execute(sql)
       db.commit()
       db.close()
    except:
      water += value
      #db.rollback() 

def waterAdd(event):
    global water
    water += 1

def PrintWater():
    global water
    oldwater = water
    water = 0
    print ("watercounter =  {0}.".format(oldwater))
    createwaterrecord(oldwater)
    t = Timer(60.0, PrintWater)
    t.start()

if __name__ == "__main__":
    #pifacedigitalio.init()
    #pifacedigitalio.digital_write_pullup(7,1)

    pifacedigital = pifacedigitalio.PiFaceDigital()
    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    listener.register(7, pifacedigitalio.IODIR_ON, waterAdd)
    listener.register(0, pifacedigitalio.IODIR_ON, waterAdd)
    listener.activate()
    print "Start counting"
    t = Timer(2.0, PrintWater)
    t.start()
