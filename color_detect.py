from __future__ import print_function
import rospy
import cv2 as cv
from clever import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clever.srv import SetLEDEffect
from threading import Thread
import math
import numpy

rospy.init_node('flight')
bridge = CvBridge()

set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

num=[]
count=[]
detect_color=[]
detect_color_second=[]

def color(data):
    global num, count, detect_color, detect_color_second
    frame = bridge.imgmsg_to_cv2(data, 'bgr8')[80:190, 100:215]  # get frame

    color_ranges = {
        'y':((),()),
        'b':((),()),
        'r':((),())
    }

    for color_name,(lower,uper) in color_ranges.items():
        mask = cv.inRange(frame, np.array(lower), np.array(uper))
        if cv.countNonZero(mask)>3500:
            countours = _

 image_sub = rospy.Subscriber('main_camera/image_raw', Image, color, queue_size=1)