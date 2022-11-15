cmake_minimum_required(VERSION 3.0.2)
project(nturt_gps)

find_package(catkin REQUIRED COMPONENTS
        rospy
        gps_common
)

catkin_package(
        INCLUDE_DIRS
        LIBRARIES
        CATKIN_DEPENDS gps_common rospy
)

include_directories(
        ${catkin_INCLUDE_DIRS}
)

# python scripts
# executable: nturt_ros_node.py
catkin_install_python(PROGRAMS
        scripts/nturt_gps_node.py
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
