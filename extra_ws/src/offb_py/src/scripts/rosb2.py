import rosbag
import rospy
from geometry_msgs.msg import *



def callback(data):
    print 1
    bag.write('/mavros/local_position/pose',data)
def callback2(data):
    print 2
    bag2.write('/mavros/local_position/velocity', data)

bag = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/test.bag', 'w')
bag2 = rosbag.Bag('/home/yanlong/extra_ws/src/offb_py/src/scripts/report/test2.bag', 'w')



def main():
    rospy.init_node('drone_track_data_saver')

    rospy.Subscriber('/mavros/local_position/velocity', geometry_msgs.msg.TwistStamped, callback2)
    rospy.Subscriber('/mavros/local_position/pose', geometry_msgs.msg.PoseStamped, callback)
    rate = rospy.Rate(20) # 10hz
    t0=rospy.Time.now()
    while not rospy.is_shutdown():
        rate.sleep()
        t1=rospy.Time.now()
    else:
        bag.close()
        bag2.close()
        print t1-t0-rospy.Duration(5.0)

if __name__ == '__main__':
        main()
