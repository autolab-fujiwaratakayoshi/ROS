#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

jpos = [0.0, 0.0]

def callback(data):
    global jpos

    print(data)
    if data.buttons[0] == 1.0:
        jpos[0] = jpos[0] + 0.1
    
def listener():
    rospy.Subscriber("joy", Joy, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

def talker():
    global jpos

    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    r = rospy.Rate(10) # 10hz
    print("talker")
    while not rospy.is_shutdown():
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = ['base_to_arm', 'arm_to_head']
        msg.position = [jpos[0], jpos[1]]
        pub.publish(msg)
        r.sleep()
        
if __name__ == '__main__':
    rospy.init_node('co_joint_state_publisher', anonymous=True) 
    listener()
    try:
        talker()
    except rospy.ROSInterruptException: pass
