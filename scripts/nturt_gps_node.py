import rospy
from gps3.agps3threaded import AGPS3mechanism
from gps_common.msg import GPSFix

def readGPS(data):
    keys = data.keys()
    for k in keys:
        if data[k] != "n/a":
            print("{}: {}".format(k, data[k]))
    print("----------------------------------")

def gps_available(data):
    if (
        data.speed == "n/a"
        or data.track == "n/a"
        or data.lon == "n/a"
        or data.lat == "n/a"
    ):
        return False
    return True

def run():
    pubgpsf = rospy.Publisher("GPS_fix", GPSFix, queue_size=100)
    rospy.init_node("talker")
    rate = rospy.Rate(10)
    agps_thread = AGPS3mechanism()
    agps_thread.stream_data()
    agps_thread.run_thread()

    gpsf = GPSFix()

    while not rospy.is_shutdown():
        GPS_raw_data = agps_thread.data_stream
        if gps_available(GPS_raw_data):
            gpsf.latitude = float(GPS_raw_data.lat)
            gpsf.longitude = float(GPS_raw_data.lon)
            gpsf.speed = float(GPS_raw_data.speed)
            gpsf.altitude = float(GPS_raw_data.alt)
            gpsf.climb = float(GPS_raw_data.climb)
            gpsf.track = float(GPS_raw_data.track)
            # gpsf.time = GPS_raw_data.time # str, not a float, type error, 

        # readGPS(vars(GPS_raw_data))
        # pub.publish(Odom)
        pubgpsf.publish(gpsf)
        rate.sleep()

if __name__ == "__main__":
    run()
