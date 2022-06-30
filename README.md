# [DISSERTATION] Racetrack-Preparation


> This repository is used to pre-process a racetrack, in order to generate a center line csv file which can be used in [another package](https://github.com/TUMFTM/global_racetrajectory_optimization) for calculating minimum time trajectory.   

Please feel free to raise topics in Issues section, I will try my best to answer them!    


## Environment


Any operating system should work (At least Ubuntu 20.04 and macOS 12.4). Note that not only the requirements.txt in this repository, but also [the requirements.txt in that repository](https://github.com/TUMFTM/global_racetrajectory_optimization/blob/master/requirements.txt) need to be fulfilled.     

> Sidenote: ~= means recommended, == means must.    


## Motivation


In order to create a dataset for training a machine learning model for overtaking, I need one of the car can follow a minimum time trajectory. I found [this repository](https://github.com/TUMFTM/global_racetrajectory_optimization) where can calculate minimum time trajectory for a given racetrack. But the given racetrack must in [a certain format](https://github.com/TUMFTM/racetrack-database/blob/master/tracks/Austin.csv), position of a center point and the distance to left and right boundary of this point. You can find some racetracks made by them [here](https://github.com/TUMFTM/racetrack-database), [by using GPS](https://github.com/TUMFTM/racetrack-database#data-source-and-processing).  

However, sometimes we don't have GPS data, but we can generate a map by using LiDAR based Simultaneous Localisation and Mapping (SLAM). So, the task is very clear now, **how to calculate center points and the corresponding track widths by given a racetrack in png format?**   


## Pipeline

> Assuming the simulator is running well on your computer, and familiar with the basic usages first

1. For example, you have a racetrack called de-espana.png, and already set as the map in the simulator.   
2. There is a section of code at the bottom of distance_transform.cpp in the src folder, comment it off.  
3. catkin_make, and run the simulator. You should see a image.csv file in the simulator root folder.  
4. Open map_to_centerline.py, copy de-espana.png and image.csv into the same folder where Centerline_generator.py is.  
5. Open image.csv file, zoom out, check whether the shape of racetrack matches the shape in the csv file. If not matches, see how many times of rotate 90° can make them match.
6. Change the number of rotation in line 131 `distance_transform = np.rot90(distance_transform, 2)` in map_to_centerline.py file.   
7. Run the map_to_centerline.py file, you should see a centerline.png file in the folder.
8. Due to that the skeletonize algorithm not always output correct centerline, you need to double check the centerline.png.   

Still use the de-espana.png as example, the centerline.png looks like this    
![centreline](https://user-images.githubusercontent.com/6621970/176739822-273dadf2-5688-4679-8c60-8269b832aff1.png)
