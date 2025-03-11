#from __future__ import print_function
import rospy
import math
import cv2 as cv
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect
#from pyzbar.pyzbar import decode as qr_read
#from threading import Thread

# inits
rospy.init_node('flight')
bridge = CvBridge()

# proxys
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

#создание топика для просмотра распознанного изображения
color_debug = rospy.Publisher("/You_Name", Image)



#объявление процедуры check_temp, при вызове которой будет распознавание цветов
def check_temp(data):
    #создание переменной frame, где будет храниться изображение с камеры. Изображение это постоянно обрабатывается. В квадратных скобках определена рамка, откуда берется изображение. Кодировка изображения brg8 (8-ми битное изображение с кодировкой BGR)
    frame = bridge.imgmsg_to_cv2(data, 'bgr8')[100:140, 130:170]  
   
    #print(frame)

   #задание для каждого цвета диапазона в кодировке BGR. В результате в каждую из переменных запишется бинарное представление цвета (0 - если цвет не попадет в диапазон и 255 - если попадает). Это бинарное представление представлено в виде матрицы.
    red = cv.inRange(frame, (0, 0, 150), (0, 0, 255))
    yellow = cv.inRange(frame, (10, 80, 88), (49, 220, 225))
    green = cv.inRange(frame, (26, 28, 60), (135, 162, 225))

    #зададим словарь color, где запишем для каждого ключа 'r', 'y', 'g' значения из бинарной матрицы только не нулевые значения
    color = {'r': cv.countNonZero(red),
             'y': cv.countNonZero(yellow),
             'g': cv.countNonZero(green)}
    
    #публикация топика для просмотра распознанного изображения
    color_debug.publish(bridge.cv2_to_imgmsg(frame, 'bgr8')) 
   
    #зададим условие, если максимальное значение из словаря равно ключу 'y', тогда выводим на экран сообщение sbrosheno. Простыми словами, если он увидел желтый цвет, тогда выводить сообщение sbrosheno
    if max(color, key=color.get) == 'r':
        #print('sbrosheno') 
        print(get_telemetry().x,get_telemetry().y,get_telemetry().z)

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)



navigate_wait(z=1, frame_id='body', auto_arm=True)

image_sub = rospy.Subscriber('main_camera/image_raw', Image, check_temp)

navigate_wait(x=0.5, y=1, z=0.6, frame_id='aruco_map')


#navigate (x=0 , y=0 , z=0.6 , speed=1 ,frame_id='body', auto_arm=True)
#rospy.sleep(5)
#navigate (x=0 , y=0 , z=0.6 , speed=1 ,frame_id='aruco_map', auto_arm=True)
#rospy.sleep(5)
#check_temp()


land()
#rospy.spin()
