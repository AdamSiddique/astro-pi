import datetime
import ephem
import os
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()
#sense.set_imu_config(True, True, True)
#Make Data File
with open("dataFileNy.csv","w") as file:
    file.write("Time, Humidity, MagneticX, MagneticY, MagneticZ, Temperature, Pressure, AccelerationX, AccelerationY, AccelerationZ, Angle from sun \n")

#Position and Day/Night
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20299.39644679  .00001347  00000-0  32240-4 0  9990"
line2 = "2 25544  51.6450  64.1844 0001663  59.0364 352.4687 15.49332070252203"

iss = ephem.readtle(name, line1, line2)
iss.compute()

sun = ephem.Sun()
sun.compute()

moon = ephem.Moon()
moon.compute()


#Time
start_time = datetime.datetime.now()
now_time = datetime.datetime.now()
duration = datetime.timedelta(seconds=10)

# vinkel beregnes ved oversættelse til radian med repr
## nedenstående giver den ækvatoriale vinkel mellem solen og ISS
vinkel = float(repr(iss.ra))-float(repr(sun.ra))
vinkel2 = float(repr(moon.ra))-float(repr(sun.ra))

angle_from_sun = vinkel
if (abs(vinkel) < 3.141592/2):
        print('Det er dag!')
else:
        print("Det er nat")

while now_time < start_time + duration:
    
    #Acceleration
    #Try to get acc data
    try:
        raw = sense.get_accelerometer_raw()
        acc_x = ("{x}".format(**raw))
        acc_y = ("{y}".format(**raw))
        acc_z = ("{z}".format(**raw))
        
    #Give all values 0 if magnet data fails
    except:
        acc_x = ""
        acc_y = ""
        acc_z = ""
    
    #Get humidity
    try:
        humidity = sense.get_humidity()
    except:
        humidity = ""
    
    #Try to get magnet data
    try:
        raw = sense.get_compass_raw()
        magnet_x = float(raw['x'])
        magnet_y = float(raw['y'])
        magnet_z = float(raw['z'])
        print("x:" + magnet_x +" y:" + magnet_y + " z:" + magnet_z)
    #Give all values 0 if magnet data fails
    except:
        magnet_x = ""
        magnet_y = ""
        magnet_z = ""
        
    #Get temperture
    try:
        temperature = sense.get_temperature()
    except:
        temperature = ""
    
    #Get pressure
    try:
        pressure = sense.get_pressure()
    except:
        pressure = ""
    
    #Update time variable
    now_time = datetime.datetime.now()
    
    #Append data to dataFile.csv
    with open ("dataFileNy.csv", "a") as file:
        file.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s  \n" % (now_time, humidity, magnet_x, magnet_y, magnet_z, temperature, pressure, acc_x, acc_y, acc_z, angle_from_sun))
    sleep(0.1)
