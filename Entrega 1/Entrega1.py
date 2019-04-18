#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Vector3
from math import pi
from std_msgs.msg import UInt8




bumper = None

def BUMPER(dado):
    global bumper
    bumper = dado.data


if __name__ == "__main__":
    rospy.init_node("roda_exemplo")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)
    recebe_bumper = rospy.Subscriber("/bumper", UInt8, BUMPER)

    try:
        while not rospy.is_shutdown():
            vel_andar = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
            vel_parar = Twist(Vector3(0,0,0), Vector3(0,0,0))
            vel_re = Twist(Vector3(-0.2,0,0), Vector3(0,0,0))
            vel_girar_90horario = Twist(Vector3(0,0,0), Vector3(0,0,-pi/4))
            vel_girar_90antihorario = Twist(Vector3(0,0,0), Vector3(0,0,pi/4))

            print(recebe_bumper)



            if recebe_bumper == 0:

                pub.publish(vel_andar)


            if recebe_bumper == 1:

                pub.publish(vel_re)
                rospy.sleep(4.0)
                pub.publish(vel_girar_90horario)
                rospy.sleep(2.0)

                recebe_bumper = 0


            elif recebe_bumper == 2:

                pub.publish(vel_re)
                rospy.sleep(4.0)
                pub.publish(vel_girar_90antihorario)
                rospy.sleep(2.0)

                recebe_bumper = 0



            elif recebe_bumper == 3:

                pub.publish(vel_andar)
                rospy.sleep(4.0)

                recebe_bumper = 0


            elif recebe_bumper == 4:

                pub.publish(vel_andar)
                rospy.sleep(4.0)

                recebe_bumper = 0





    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")