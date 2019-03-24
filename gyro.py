#!/usr/bin/python
import smbus
import math
import rospy
from std_msgs.msg import Int16
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(0)
address = 0x68
Orientation = 0
def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
def GetXY():
        bus.write_byte_data(address, power_mgmt_1, 0)
        beschleunigung_xout = read_word_2c(0x3b)
        beschleunigung_yout = read_word_2c(0x3d)
        beschleunigung_zout = read_word_2c(0x3f)
#       print "X___", beschleunigung_xout
#       print "y____", beschleunigung_yout
#       print "Z_____", beschleunigung_zout     
        beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
        beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
        beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
        Xangle = get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
        Yangle = get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
        return Xangle, Yangle
def Publish():
        global Orientation
        pub = rospy.Publisher('Orientation', Int16, queue_size=10)
        rospy.init_node('Accelerom', anonymous=True)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
                Position()
                position=0
                if Orientation < -5:
                        position = -1
                        Orientation=0
                if (Orientation > 5):
                        position = 1
                        Orientation=0
                pub.publish(position)
                rate.sleep()


def Position():
        global Orientation
        X, Y = GetXY()
        if (Y > 50):
                Orientation+=1
        if (Y < -50):
                Orientation-=1
if __name__ == '__main__':
        try:
                Publish()
        except rospy.ROSInterruptException:
                pass

