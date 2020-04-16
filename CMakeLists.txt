cmake_minimum_required(VERSION 2.8.3)
project(joy2rc)
find_package(catkin REQUIRED roscpp std_msgs sensor_msgs joy message_generation)

add_message_files(
  FILES
      IntAdc.msg
)

generate_messages(
  DEPENDENCIES
   std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs
)



#catkin_package()
