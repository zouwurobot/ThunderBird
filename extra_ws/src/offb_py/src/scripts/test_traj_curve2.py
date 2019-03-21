#!/usr/bin/env python
import rosbag
import rospy
from geometry_msgs.msg import *
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
from robot.trajectory import jtraj
import numpy as np
import time

current_state = State()
current_p=PoseStamped()
recordflag=0
def state_cb(msg):
	global current_state
	current_state = msg
	#print "callback"

def callback(data):
	global recordflag
	global current_p
	current_p=data
	if recordflag!=0:
		bag.write('/mavros/local_position/pose', data)

def callback2(data):
	global recordflag
	if recordflag != 0:
		bag2.write('/mavros/local_position/velocity', data)

def callback3(data):
	global recordflag
	if recordflag!=0:
		bag3.write('/mavros/setpoint_position/local', data)

def callback4(data):
	global recordflag
	if recordflag != 0:
		bag4.write('/mavros/setpoint_velocity/cmd_vel', data)

def local_position_pose():
	rospy.Subscriber('/mavros/local_position/pose',geometry_msgs.msg.PoseStamped, callback)

def local_position_velocity():
	rospy.Subscriber('/mavros/local_position/velocity',geometry_msgs.msg.TwistStamped, callback2)

if __name__=="__main__":
	bag = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/data_curve2_{}.bag'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'w')
	bag2 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/data2_curve2_{}.bag'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'w')
	bag3 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/data3_curve2_{}.bag'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'w')
	bag4 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/data4_curve2_{}.bag'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), 'w')
	global current_state
	global recordflag
	rospy.init_node('offb_node', anonymous=True)	
	rospy.Subscriber("mavros/state", State, state_cb)
	local_position_pose()
	local_position_velocity()
	rospy.Subscriber('/mavros/setpoint_position/local', geometry_msgs.msg.PoseStamped, callback3)
	rospy.Subscriber('/mavros/setpoint_velocity/cmd_vel', geometry_msgs.msg.Twist, callback4)
	local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
	local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', Twist, queue_size=10)

	print("Publisher and Subscriber Created")
	arming_client = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
	set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode)
	print("Clients Created")

	rate = rospy.Rate(20)


	while(not current_state.connected):
		print(current_state.connected)
		rate.sleep()
	
	print("Creating pose")
	pose = PoseStamped()
	#set position here
	pose.pose.position.x = 0
	pose.pose.position.y = 0
	pose.pose.position.z = 0

	vel = Twist()
	vel.linear.x = 0
	vel.linear.y = 0
	vel.linear.z = 0


	#presend some position for stack
	for i in range(100):
		local_pos_pub.publish(pose)
		rate.sleep()
		
	print("Creating Objects for services")
	offb_set_mode = SetMode()
	offb_set_mode.custom_mode = "OFFBOARD"
	arm_cmd = CommandBool()
	arm_cmd.value = True
	num=0
	land=0
	arrived=0
	freq=20


	#reference trajectory parameters
	q0=[0,0,0]
	q1=[0,0,1.5]
	qd1=[0.1,0,0]
	q2=[2,2.5,2.5]
	qd2=[0,0.3,0]
	q3=[1,4,1.5]
	qd3=[0,0,0]

	tf=4        #time between setting points
	tv=np.linspace(0, tf, (tf*freq)+1, endpoint=True)
	A = jtraj(q0, q1, tv, qd0=None, qd1=None)
	A2 = jtraj(q1, q2, tv, qd1, qd2)
	A3 = jtraj(q2, q3, tv, qd2, qd3)



	last_request = rospy.Time.now()

	j=1
	point=0

	xarrive=0
	yarrive=0
	zarrive=0
	flagarrive=0
	timearrive=0


	while not rospy.is_shutdown():
		#print(current_state)
		if land == 0:
			if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0))):
				resp1 = set_mode_client(0,offb_set_mode.custom_mode)
				if resp1.mode_sent:
					print ("Offboard enabled")
				last_request = rospy.Time.now()
			elif (not current_state.armed and (rospy.Time.now() - last_request > rospy.Duration(5.0))):
				arm_client_1 = arming_client(arm_cmd.value)
				if arm_client_1.success:
					print("Vehicle armed")

				last_request = rospy.Time.now()

			if arrived==0:
				if point==0:
					pose.pose.position.x = A[0][j-1,0]
					pose.pose.position.y = A[0][j-1,1]
					pose.pose.position.z = A[0][j-1,2]
					vel.linear.x = A[1][j-1,0]
					vel.linear.y = A[1][j-1,1]
					vel.linear.z = A[1][j-1,2]

				#To judge whether the drone arrives at home point
				if point==1:
					if (current_p.pose.position.x-q1[0]<0.1 and current_p.pose.position.x-q1[0]>-0.1):
						xarrive=1
					if (current_p.pose.position.y - q1[1] < 0.1 and current_p.pose.position.y - q1[1] > -0.1):
						yarrive = 1
					if (current_p.pose.position.z-q1[2]<0.1 and current_p.pose.position.z-q1[2]>-0.1):
						zarrive=1
					if xarrive==1 and yarrive==1 and zarrive==1:

						recordflag=1
						if flagarrive!=1:
							timearrive=rospy.Time.now()
							print ("daole")
							flagarrive=1
						if rospy.Time.now() - timearrive > rospy.Duration(10.0):
							point+=1
							print rospy.Time.now() - timearrive- rospy.Duration(10.0)

				#Sending ref traj
				if point==2:
					pose.pose.position.x = A2[0][j-1,0]
					pose.pose.position.y = A2[0][j-1,1]
					pose.pose.position.z = A2[0][j-1,2]
					vel.linear.x = A2[1][j-1,0]
					vel.linear.y = A2[1][j-1,1]
					vel.linear.z = A2[1][j-1,2]
				if point==3:
					pose.pose.position.x = A3[0][j-1,0]
					pose.pose.position.y = A3[0][j-1,1]
					pose.pose.position.z = A3[0][j-1,2]
					vel.linear.x = A3[1][j-1,0]
					vel.linear.y = A3[1][j-1,1]
					vel.linear.z = A3[1][j-1,2]


				if point!=1:
					if j==tf*freq+1:
						j=0
						point+=1
						print("arrived",point-1)
						if point==4:
							arrived=1
					j+=1


				local_pos_pub.publish(pose)
				local_vel_pub.publish(vel)

			#finish all the trajs
			else:
				local_pos_pub.publish(pose)
				num += 1
				if num >= 400:
					land = 1
					recordflag=0
					bag.close()
					bag2.close()
					bag3.close()
					bag4.close()

        #landing code
		else:
			offb_set_mode = SetMode()
			offb_set_mode.custom_mode = "AUTO.LAND"
			resp1 = set_mode_client(0, offb_set_mode.custom_mode)
			if resp1.mode_sent:
				print ("LANDING")
                
		#uprint current_state
		rate.sleep()
	
