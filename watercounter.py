import pifacedigitalio
import MySQLdb
from threading import Timer

water = 0

def createwaterrecord():
    db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
    cursor = db.cursor()
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
             LAST_NAME, AGE, SEX, INCOME)
             VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    try:
       cursor.execute(sql)
       db.commit()
    except:
      db.rollback()
    db.close()

def waterAdd(event):
    global water
    water += 1

def PrintWater():
    global water
    oldwater = water
    water = 0
    print ("watercounter =  {0}.".format(oldwater))
    t = Timer(30.0, PrintWater)
    t.start()

if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()
    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    listener.register(0, pifacedigitalio.IODIR_ON, waterAdd)
    listener.activate()
    print "Start counting"
    t = Timer(30.0, PrintWater)
    t.start()
