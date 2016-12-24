#!/usr/bin/env python
import rospy, sys
from swarm.msg import QuadStamped

if __name__ == '__main__':
    rospy.init_node('swarm_go_up_and_stay', anonymous=True)
    rate = rospy.Rate(100)
    argv = sys.argv
    rospy.myargv(argv)
    n = int(argv[1])

    pub = []
    quad = []
    for i in range(n):
        pub.append(rospy.Publisher('/uav' + str(i) + '/des_pos', QuadStamped, queue_size=n))
        quad.append(QuadStamped())
        quad[i].header.frame_id = 'world'
        xy = rospy.get_param('/uav' + str(i))
        quad[i].x = xy['x']
        quad[i].y = xy['y']
        quad[i].z = 0
        quad[i].yaw = 0

    try:
        while not rospy.is_shutdown():
            for i in range(n):
                quad[i].header.stamp = rospy.Time.now()
                if quad[i].header.stamp.secs >= 2:
                    quad[i].z = 1.0
                pub[i].publish(quad[i])
                rospy.loginfo("%f = [%f, %f, %f - %f]", i, quad[i].x, quad[i].y, quad[i].z, quad[i].yaw)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass

    finally:
        for i in range(n):
            quad[i].header.stamp = rospy.Time.now()
            quad[i].z = 0
            pub[i].publish(quad[i])
        rospy.loginfo("End of node")
