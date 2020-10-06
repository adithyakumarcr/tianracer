#!/usr/bin/env python

import rospy

#from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDrive

import sys, select, termios, tty

msg = """
Control Your racecar!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
space key, k : force stop
w/x: shift the middle pos of throttle by +/- 5 pwm
a/d: shift the middle pos of steering by +/- 2 pwm
CTRL-C to quit
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

moveBindings= { 'i':(1,0),'k':(-1,0),'j':(0,+1),'l':(0,-1), 'u':(1,+1),'o':(1,-1) ,'m':(-1,+1),'.':(-1,-1)}



if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('racecar_teleop')
    

    ackermann = AckermannDrive()
    ackermann_pub= rospy.Publisher('/tianracer/ackermann_cmd',AckermannDrive, queue_size=5)

    control_speed = 0 
    control_turn = 0  

    
    print msg
    print vels(control_speed,control_turn)
    while(1):
        key = getKey()	
     
	
	if key in moveBindings.keys():
	    control_speed=moveBindings[key][0]*1
	    control_turn=moveBindings[key][1]*90
	    print vels(control_speed,control_turn)


	
	elif key == 'w':
            control_speed=1
	    #control_speed = control_speed-0.1
            print vels(control_speed,control_turn)

        elif key == 's' :
            control_speed=-1
	    #control_speed = control_speed +0.1
            print vels(control_speed,control_turn)

	
        
	elif key == 'a' :
            #control_turn = control_turn + 2
	    control_turn=90
            print vels(control_speed,control_turn)
            
        elif key == 'd' :
            #control_turn = control_turn - 2
	    control_turn=-90
            print vels(control_speed,control_turn)
	
	elif key=='':
		control_speed=0	
		control_turn=0	

        elif key == '\x03' :
            break

        ackermann.speed=control_speed
        ackermann.steering_angle=control_turn*(3.14/180)
        ackermann_pub.publish(ackermann) 
	
         

   
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
