#!/usr/bin/env python

import argparse
import IPython
import numpy as np
import rosbag
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import time, sys, os
import os

bagname = '/media/mbuerki/UP-Drive-Dataset/umich/bags/2012-01-15_ds2r.bag'
bagname_out = '/media/mbuerki/UP-Drive-Dataset/umich/bags/2012-01-15_ds2r_odo.bag'

def process(bag_file):
  bag_path, bag_name = os.path.split(bag_file)
  bag_out = os.path.join(bag_path, os.path.splitext(bag_name)[0] + "_p.bag")

  print "Opening bag ", bag_file, "."
  bag_in = rosbag.Bag(bag_file, 'r')
  num_messages = bag_in.get_message_count()
  print "Done. Num messages: ", num_messages, "."

  bag_out = rosbag.Bag(bag_out, 'w')

  i = 0
  for topic, msg, t in bag_in.read_messages():
      if topic == '/pose_imu':
        m = Odometry()
        m.header = msg.header
        m.child_frame_id = "IMU/GPS"
        m.pose.pose = msg.pose

        msg = m

      bag_out.write(topic, msg, t)

      i += 1
      if i % 1000 == 0:
        print "Processed ", i, "/", num_messages, " messages."

  bag_out.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='...')

  parser.add_argument('bag_file', help='Rosbag to process.')
  
  parsed = parser.parse_args()
  bag_file = parsed.bag_file

  process(bag_file)
