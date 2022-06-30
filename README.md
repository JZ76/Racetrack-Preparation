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


