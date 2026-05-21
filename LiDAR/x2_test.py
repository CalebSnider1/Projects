import ydlidar
import time
import math



ydlidar.os_init()

def start_scan():
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, "/dev/ttyUSB0")
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 7.0)    #change to increase or decrease speed (rated for max 10)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 3)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)

    ret = laser.initialize()
    if ret:
        init_val = 0
        ret = laser.turnOn()
        scan = ydlidar.LaserScan()
        while ret and ydlidar.os_isOk():
            r = laser.doProcessSimple(scan)
            if r:
                init_val = 0
                hz = round(1.0/scan.config.scan_time, 1) if scan.config.scan_time > 0 else 0
                print("Scan received:", scan.points.size(), "points at", hz, "Hz")
                for point in scan.points:
                    if point.range == 0:
                        continue
                    degrees = math.degrees(point.angle)
                    #print("angle:", round(degrees, 2), "range:", round(point.range, 3), "m")
                    secondDist = point.range
                    if init_val != 0 and (secondDist < firstDist):
                        firstDist = secondDist
                        closestAngle = degrees
                        closestDistance = point.range


                    elif init_val == 0:
                        firstDist = point.range
                        closestAngle = degrees
                        closestDistance = point.range
                        init_val = 1
                print("Closest Angle:", closestAngle, "Closest Distance:", closestDistance)


            else:
                print("Failed to get Lidar Data")
            time.sleep(0.05)
        laser.turnOff()
    laser.disconnecting()

start_scan()


