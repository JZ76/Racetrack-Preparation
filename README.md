# [DISSERTATION] Racetrack-Preparation


> This repository is used to pre-process a racetrack, in order to generate a center line csv file which can be used in another package called [global_racetrajectory_optimization](https://github.com/TUMFTM/global_racetrajectory_optimization) for calculating minimum time trajectory.   

Please feel free to raise topics in Issues section, I will try my best to answer them!    


## Environment


Any operating system should work (At least Ubuntu 20.04 and macOS 12.4). Note that not only the requirements.txt in this repository, but also [the requirements.txt in global_racetrajectory_optimization](https://github.com/TUMFTM/global_racetrajectory_optimization/blob/master/requirements.txt) need to be fulfilled.     

> Sidenote: ~= means recommended, == means must.    


## Motivation


In order to create a dataset for training a machine learning model for overtaking, I need one of the car can follow a minimum time trajectory. I found [this repository](https://github.com/TUMFTM/global_racetrajectory_optimization) where can calculate minimum time trajectory for a given racetrack. But the given racetrack must in [a certain format](https://github.com/TUMFTM/racetrack-database/blob/master/tracks/Austin.csv), position of a center point and the distance to left and right boundary of this point. You can find some racetracks made by them [here](https://github.com/TUMFTM/racetrack-database), [by using GPS](https://github.com/TUMFTM/racetrack-database#data-source-and-processing).  

However, sometimes we don't have GPS data, but we can generate a map by using LiDAR based Simultaneous Localisation and Mapping (SLAM). So, the task is very clear now, **how to calculate center points and the corresponding track widths by given a racetrack in png format?**   


## Pipeline

> Assuming the simulator is running well on your computer, and familiar with the basic usages first

1. For example, you have a racetrack called `de-espana.png`, and already set as the map in the simulator.   
2. There is a section of code at the bottom of `distance_transform.cpp` in the src folder, comment it off.  
3. catkin_make, and run the simulator. You should see a `image.csv` file in the simulator root folder (I already uploaded it to this repository for convenience).  
4. Open `map_to_centerline.py`, copy `de-espana.png` and `image.csv` into the same folder where `Centerline_generator.py` is.  
5. Open `image.csv` file, zoom out, check whether the shape of racetrack matches the shape in the csv file. If not matches, see how many times of rotate 90° can make them match.
6. Change the number of rotation in line 131 `distance_transform = np.rot90(distance_transform, 2)` in `map_to_centerline.py` file.   
7. Run the `map_to_centerline.py` file, you should see a `centerline.png` file in the folder.
8. Due to that the skeletonize algorithm not always output correct centerline, you need to double check the `centerline.png`.   

Still use the `de-espana.png` as example, the `centerline.png` looks like this. Clearly there are two circles which is wrong.    
<img width="1901" alt="Screenshot 2000-06-30 at 18 28 12" src="https://user-images.githubusercontent.com/6621970/176740343-f1ed58e0-eaf6-4778-a361-64d11cc0a58c.png">

9. You have to fix the `centerline.png` manually, by using any software that can edit png file in pixel level, such as Photoshop. Make sure one white pixel can ONLY connect to other two white pixels in a 3\*3 pixel square. I give some examples below, X means white pixel, assuming the center point is always the white pixel  
                                              
       For example, X 0 0     X 0 0     X 0 0       0 0 X     0 0 X     0 X X     0 X 0
                    0 X X     0 X 0     0 X 0       0 X 0     X X 0     0 X 0     X X X
                    0 0 0 ✅  X 0 0 ✅  0 0 X ✅    0 X X ❌  0 0 X ❌  0 X 0 ❌  0 0 0 ❌     
                    
10. After fix the `centerline.png`, comment off line 156, 157, 158 in the `map_to_centerline.py`, and rerun the script.   
11. Finally, you will see a `results.csv` in the folder, this will be the input of next part, which is using the [global_racetrajectory_optimization](https://github.com/TUMFTM/global_racetrajectory_optimization). You probably need `scale` to change the width of racetrack to make it more realism.  

> Steps below are not related to this repository, but I listed them here as reference.

12. After download the code, make sure you can run the demo successfully.  
13. Copy the `results.csv` to `/global_racetrajectory_optimization/inputs/tracks`  
14. Edit line 45 in `main_globaltraj.py` file to read your `results.csv`   
15. Run `main_globaltraj.py`, you should get minimum time trajectory waypoints in `outputs` folder called `traj_race_cl.csv`  
16. If you see an error about **spline is crossed**, then increase stepsize in line 13, 14, 15 in `global_racetrajectory_optimization/params/racecar.ini`  

We will only use three columns in `traj_race_cl.csv`: `x_m`, `y_m`, `psi_rad`  
`x_m`: x coordinate of this waypoint.   
`y_m`: y coordinate of this waypoint.  
`psi_rad`: heading theta to the next waypoint.  
[This tutorial](https://github.com/JZ76/f1tenth_simulator_two_agents/wiki/How-to-use-Model-Predictive-Control-algorithm) shows how to use `traj_race_cl.csv` file in MPC algorithm.
