"""
Copyright 2022 Jiancheng Zhang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import math
import csv
import queue

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from skimage.morphology import skeletonize

"""
Two input files: A png file, obstacle should be black, racetrack should be white, the racetrack must be closed
                 A csv file, generated from distance_transform.cpp in the simulator
                 
Two output files: A png file, center line of the racetrack
                  A csv file, format matches https://github.com/TUMFTM/racetrack-database/tree/master/tracks
"""

# scale is used for changing size of a racetrack.
# Due to the package we are using to calculate minimum time trajectory is based on real vehicle model,
# and their demo is using racetracks in real size.
# But the png and csv file lost size information
# You don't have to calculate a very accurate scale factor,
# just need to make sure the "w_tr_right_m" and "w_tr_left_m" is between 4 and 6 in the results.csv
# remember this scale, you will need it when draw the minimum time trajectory in the simulator

# Australia 5
# Malaysian 3
# Gulf 6
# Shanghai 5
scale = 3

# movement in 8 directions
"""
0  0  0
 \ | /
0--X--0
 / | \ 
0  0  0
"""
directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [-1, -1], [1, 0], [1, -1], [0, -1]]

# ----------------------------------------------------------------------------------------------------------------------

def dfs(i, j):

    # First in first out
    qu = queue.Queue()

    # put in the starting point, a very common way of matrix serialization
    qu.put(i * columns + j)
    # this position is visited
    visited[i][j] = 1
    # this is the place to use scale
    result_data = [j / scale,
                   i / scale,
                   distance_transform[i][j] / scale,
                   distance_transform[i][j] / scale]
    writer.writerow(result_data)

    # standard DFS structure, while + for + if
    while not qu.empty():

        current = qu.get()

        # deserialization, current_x is the modulus because we added j after columns * i
        # And current_y is integer division but need to round to floor, otherwise an extra 1 will in the current_x
        current_y = math.floor(current / columns)
        current_x = math.floor(current % columns)

        # iterate through all 8 directions
        for k in range(8):

            # calculate the new position after moving to that direction
            newY = current_y + directions[k][0]
            newX = current_x + directions[k][1]

            # if it is a white dot AND not seen before
            if skeleton[newY][newX] and not visited[newY][newX]:

                qu.put(newY * columns + newX)
                visited[newY][newX] = 1
                result_data = [newX / scale,
                               newY / scale,
                               distance_transform[newY][newX] / scale,
                               distance_transform[newY][newX] / scale]
                writer.writerow(result_data)

                # early stop, make sure dfs only go in one direction rather than bidirectional
                # because when meet first white dot, it will find two white dots that not visited
                # but for other white dots, no such problem.
                # In the 8 directions, one is itself, another is the one where it comes (must be visited), another is the next one
                break

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

# ----------------------------------------------------------------------------------------------------------------------
# Read a csv file ------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # the csv file is the output from distance_transform.cpp in the simulator,
    # where contains distance between anypoint to its nearest obstacle
    # once you get that csv, open it, and zoom out, you should see racetrack shape which made by numbers
    # the unit is meter, each index is 1 meter
    data = pd.read_csv("image.csv")
    # last column is NaN, drop it
    distance_transform = np.array(data.iloc[:, :-1])

    # compare distance_transform with your racetrack png image,
    # probably you will find there is rotation between csv and image,
    # usually distance_transform can match the png image after rotate 180 degree, which is rot90(distance_transform, 2)
    # if the csv matches the image, you can comment out this code
    distance_transform = np.rot90(distance_transform, 2)

# ----------------------------------------------------------------------------------------------------------------------
# Read a png image, generate center line -------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # Using Image package in pillow lib
    # convert('L') means output greyscale data: white:255 black:0
    image = np.array(Image.open(r"de-espana.png").convert('L'))

    # you can change threshold, because boundary between white and black is grey
    # how many grey cells you would like to convert to white? 255 means I don't want any grey cells
    image[image < 255] = 0

    # First step is convert numerical data to boolean, white is True(none 0), black is False(0)
    # The input matrix must be binary data, i.e. only 0 and 1
    # The algorithm not always fully success, like what I showed in the repository
    skeleton = skeletonize(image.astype(bool))

# ----------------------------------------------------------------------------------------------------------------------

    # OPTIONAL
    # if the algorithm failed, you can fix the center line manually, and input again
    # Compare with the section above, the only difference is we don't have to use skeletonize algorithm again
    # image = np.array(Image.open(r"centerline.png").convert('L'))
    # image[image < 255] = 0
    # skeleton = image.astype(bool)

# ----------------------------------------------------------------------------------------------------------------------
# Output a png image ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    # color map using gray https://matplotlib.org/stable/tutorials/colors/colormaps.html
    plt.imsave('centerline.png', skeleton, cmap='gray')
    plt.imshow(skeleton, cmap='gray', interpolation='nearest')
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Output a csv file ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

    with open("results.csv", "w", newline='') as file:

        # header should be exact same as the header in https://github.com/TUMFTM/racetrack-database/tree/master/tracks
        header = ["# x_m", "y_m", "w_tr_right_m", "w_tr_left_m"]

        writer = csv.writer(file)
        writer.writerow(header)

        # the shape of distance_transform should match shape of skeleton
        # row and columns can be seen as how many meters in row and column direction
        row = distance_transform.shape[0]
        columns = distance_transform.shape[1]

        # preparing a boolean matrix for depth first search
        visited = np.zeros([row, columns])

        for i in range(row):
            for j in range(columns):
                # find a white dot
                if skeleton[i, j]:
                    # pass the starting position to dfs()
                    dfs(i, j)

                    # early stop, due to the center line is closed, if we find a white dot, and finish whole dfs,
                    # which means we already went through all white dots in skeleton
                    break
