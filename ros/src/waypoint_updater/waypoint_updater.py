#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint

import math

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 150  # Number of waypoints we will publish. You can change this number


class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)

        # TODO: Add other member variables you need below
        self.curr_pose = PoseStamped()
        self.incoming_waypoints = Lane()

        rospy.Timer(rospy.Duration(.05), self.update_waypoints_tcb)

        rospy.spin()

    def pose_cb(self, msg):
        self.curr_pose = msg
        return 0

    def waypoints_cb(self, waypoints):
        self.incoming_waypoints = waypoints
        return 0

    def update_waypoints_tcb(self, event):

    	if len(self.incoming_waypoints.waypoints) > 1: 
	        closest_indices = self.closest_waypoints(self.incoming_waypoints, self.curr_pose)

	        waypoints = []
	        start = closest_indices[1]

	        for i in range (0,LOOKAHEAD_WPS-1):
	        	waypoints.append(self.incoming_waypoints.waypoints[(i+start)%len(self.incoming_waypoints.waypoints)])

	        self.publish(waypoints)

        return 0



    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        pass

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    # this distance function returns the distance along a prescribed
    # path in the given waypoints list 
    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist

    # this distance function returns the indices in the waypoint 
    # vector of the two nearest waypoints to the vehicles current
    # position (Euclidean distance only). We assume the car is 
    # between those two waypoints
    def closest_waypoints(self, waypoints, curr_pose):
    	
    	indices = []
    	distances = []

    	#calculate a distance between curr_pose and each waypoint
    	for i in range(len(waypoints.waypoints)): 
    		
    		#unpack and label incoming data
    		wp_x = waypoints.waypoints[i].pose.pose.position.x
    		wp_y = waypoints.waypoints[i].pose.pose.position.y
    		wp_z = waypoints.waypoints[i].pose.pose.position.z
    		pose_x = curr_pose.pose.position.x
    		pose_y = curr_pose.pose.position.y
    		pose_z = curr_pose.pose.position.z

    		#calculate and add distance to list
    		distance = math.sqrt((pose_x-wp_x)**2 + (pose_y-wp_y)**2  + (pose_z-wp_z)**2)
    		distances.append(distance)

    	#find lowest distance
    	min_index = distances.index(min(distances))

    	#find second lowest distance (and correct index if needed)
    	del distances[min_index]
    	nxt_min_index = distances.index(min(distances))

    	if nxt_min_index >= min_index: 
    		nxt_min_index += 1

    	indices = [min_index, nxt_min_index]
    	indices.sort()

    	return indices

    def publish(self, waypoints): 
    	lane = Lane()
    	lane.header.frame_id = '/world'
    	lane.header.stamp = rospy.Time(0)
    	lane.waypoints = waypoints
    	self.final_waypoints_pub.publish(lane)


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
