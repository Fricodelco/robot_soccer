#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script is modified based on 
# https://github.com/d-zenju/mpu9250/blob/master/MPU9250.py
# from d-zenju


import smbus
import time
import math
import rospy
from std_msgs.msg import Int16
Orientation = 0
class MPU9250():
    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.addr = 0x68
        # set bypass mode for magnetometer
        self.bus.write_byte_data(self.addr, 0x37, 0x02)
    def readLine(self, address, high, low):
        hline = self.bus.read_byte_data(address, high)
        lline = self.bus.read_byte_data(address, low)
        value = (hline << 8) + lline
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value


    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))


    def get_y_rotation(self,x,y,z):
        dist= self.dist(y,z)
        radians = math.atan2(x, dist)
        return radians

    def get_x_rotation(self,x,y,z):
        dist = self.dist(x,z)
        radians = math.atan2(y, dist)
        return radians
 def readAccel(self):
        # register address(MPU9250)
        ACCEL_XOUT_H = 0x3B
        ACCEL_XOUT_L = 0x3C
        ACCEL_YOUT_H = 0x3D
        ACCEL_YOUT_L = 0x3E
        ACCEL_ZOUT_H = 0x3F
        ACCEL_ZOUT_L = 0x40
        # calculate
        xout = self.readLine(self.addr, ACCEL_XOUT_H, ACCEL_XOUT_L)
        yout = self.readLine(self.addr, ACCEL_YOUT_H, ACCEL_YOUT_L)
        zout = self.readLine(self.addr, ACCEL_ZOUT_H, ACCEL_ZOUT_L)
        X = 2.0 * xout / 32768.0
        Y = 2.0 * yout / 32768.0
        Z = 2.0 * zout / 32768.0
        Xangle = self.get_x_rotation(X, Y, Z)
        Yangle = self.get_y_rotation(X, Y, Z)
        return math.degrees(Xangle), math.degrees(Yangle)
    """def readGyro(self):
        # register address(MPU9250)
        GYRO_XOUT_H = 0x43
        GYRO_XOUT_L = 0x44
        GYRO_YOUT_H = 0x45
        GYRO_YOUT_L = 0x46
        GYRO_ZOUT_H = 0x47
        GYRO_ZOUT_L = 0x48
        # calculate
        xout = self.readLine(self.addr, GYRO_XOUT_H, GYRO_XOUT_L)
        yout = self.readLine(self.addr, GYRO_YOUT_H, GYRO_YOUT_L)
        zout = self.readLine(self.addr, GYRO_ZOUT_H, GYRO_ZOUT_L)
        x = 250.0 * xout / 32768.0
        y = 250.0 * yout / 32768.0
        z = 250.0 * zout / 32768.0
        return [x, y, z]"""
    """def readTemp(self):
        # register address(MPU9250)
        TEMP_OUT_H = 0x41
        TEMP_OUT_L = 0x42
        temp_out = self.readLine(self.addr, TEMP_OUT_H, TEMP_OUT_L)
        temp = temp_out / 340.0 + 36.53
        return temp"""
    def readMagnet(self):
        # register address(AK8963)
        MAGNET_XOUT_L = 0x03
        MAGNET_XOUT_H = 0x04
        MAGNET_YOUT_L = 0x05
        MAGNET_YOUT_H = 0x06
        MAGNET_ZOUT_L = 0x07
        MAGNET_ZOUT_H = 0x08
        # MPU9250 datsheet page 24: slave address for the AK8963 is 0X0C
        AK8963_ADDRESS = 0x0C
        self.bus.write_byte_data(AK8963_ADDRESS, 0x0A, 0x12)
        # calculate
        time.sleep(0.05)
        xout = self.readLine(AK8963_ADDRESS, MAGNET_XOUT_H, MAGNET_XOUT_L)
        yout = self.readLine(AK8963_ADDRESS, MAGNET_YOUT_H, MAGNET_YOUT_L)
        zout = self.readLine(AK8963_ADDRESS, MAGNET_ZOUT_H, MAGNET_ZOUT_L)
        x = 1200.0 * xout / 4096.0
        y = 1200.0 * yout / 4096.0
        z = 1200.0 * zout / 4096.0
        return x,y,z

    def Publish(self):
        global Orientation
        pub = rospy.Publisher('Orientation', Int16, queue_size=10)
        rospy.init_node('Accelerom', anonymous=True)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
                self.Position()
                position=0
                if Orientation < -5:
                        position = -1
                        Orientation=0
                if (Orientation > 5):
                        position = 1
                        Orientation=0
                pub.publish(position)
                rate.sleep()


    def Position(self):
        global Orientation
        X, Y = self.readAccel()
        if (Y > 55):
                Orientation+=1
        if (Y < -55):
                Orientation-=1
if __name__ == '__main__':
        mpu9250 = MPU9250()
        try:
                mpu9250.Publish()
        except rospy.ROSInterruptException:
                pass
                                                                                       137,1-8       Bot
