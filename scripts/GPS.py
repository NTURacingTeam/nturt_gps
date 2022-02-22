import rospy
import math
from gps3.agps3threaded import AGPS3mechanism
from nav_msgs.msg import Odometry


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
    pub = rospy.Publisher("GPS", Odometry, queue_size=100)
    rospy.init_node("talker")
    rate = rospy.Rate(10)
    Odom = Odometry()
    agps_thread = AGPS3mechanism()
    agps_thread.stream_data()
    agps_thread.run_thread()

    while not rospy.is_shutdown():
        GPS_raw_data = agps_thread.data_stream
        if gps_available(GPS_raw_data):
            speed = GPS_raw_data.speed
            track = math.radians(GPS_raw_data.track)
            Odom.header.stamp = rospy.Time.now()
            Odom.pose.pose.position.x = GPS_raw_data.lon
            Odom.pose.pose.position.y = GPS_raw_data.lat
            Odom.pose.pose.orientation.x = speed * math.cos(track)
            Odom.pose.pose.orientation.y = speed * math.sin(track)
        readGPS(vars(GPS_raw_data))
        pub.publish(Odom)
        rate.sleep()


if __name__ == "__main__":
    run()
