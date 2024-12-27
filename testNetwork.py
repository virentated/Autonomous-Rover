import Tkinter as tk
import math
import random
from qset_lib import Rover
from time import sleep
import numpy as np
import joblib
import pandas as pd

def faceTarget():
    # calculate the angle to the target in radians
    dx = target_x - rover.x
    dy = target_y - rover.y
    angle_to_target = math.atan2(dy, dx)
    
    # calculate the change in heading to face the target
    heading_diff = angle_to_target - math.radians(rover.heading)
    if heading_diff > math.pi:
        heading_diff -= 2 * math.pi
    elif heading_diff < -math.pi:
        heading_diff += 2 * math.pi
    heading_diff = heading_diff*180/math.pi

    rotateRover(heading_diff/2)
    rotateRover(heading_diff/2)

def targetHeading():
    dx = target_x - rover.x
    dy = target_y - rover.y
    angle = math.atan2(dy, dx)
    angle = math.degrees(angle)
    target_heading = angle - rover.heading
    if target_heading > 180:
        target_heading -= 360
    elif target_heading < -180:
        target_heading += 360
    return target_heading + 90

def rotateRover(heading_change):
    # calculate the target heading in degrees from -180 to 180
    target_heading = ((rover.heading + heading_change) % 360)
    
    # calculate the angular difference between current and target headings
    angle_diff = target_heading - rover.heading
    if angle_diff > 180:
        angle_diff -= 360
    elif angle_diff < -180:
        angle_diff += 360
    
    # calculate the direction and speed of the turn
    direction = 1 if angle_diff < 0 else -1
    
    # set the differential steering speeds to rotate the rover
    while abs(angle_diff) > 1:  # adjust the threshold as needed
        rover.send_command(direction, -direction)
        angle_diff = target_heading - rover.heading
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        sleep(0.01)
    
    # stop the rover when the desired heading is reached
    rover.send_command(0, 0)

def moveRover(distance):
    x1, y1 = rover.x, rover.y
    while (math.sqrt((x1 - rover.x)**2 + (y1 - rover.y)**2) < distance):
        lidar_distances = [max(min(x, 15), 0) for x in rover.laser_distances][8:22]
        if ((min(lidar_distances)) < 1):
            if lidar_distances.index(min(lidar_distances)) < 7:
                while ((min([max(min(x, 15), 0) for x in rover.laser_distances][8:15])) < 1):
                    rover.send_command(-1, 1)
            else:
                while ((min([max(min(x, 15), 0) for x in rover.laser_distances][15:22])) < 1):
                    rover.send_command(1, -1)
        rover.send_command(5, 5)
        sleep(0.01)
    rover.send_command(0,0)
    return


rover = Rover()
rover.send_command(0, 0)

# Load the training data from the CSV file
train_data = pd.read_csv('training_data_final.csv',header=None)

lidar_data = [max(min(x, 15), 0) for x in rover.laser_distances]
while len(lidar_data) != 30:
    lidar_data = [max(min(x, 15), 0) for x in rover.laser_distances]

target_x = random.randint(30, 35)
target_y = random.randint(-20, 20)
print('Target: ' + str(target_x) + ',' + str(target_y))

faceTarget()
model = joblib.load("model.joblib")
while math.sqrt((target_x - rover.x)**2 + (target_y - rover.y)**2) > 2:
    lidar_data = [max(min(x, 15), 0) for x in rover.laser_distances]
    target_heading = targetHeading()
    # print(target_heading)
    
    all_data = [target_heading]+lidar_data
    model_heading = model.predict([all_data])
    rotateRover(model_heading - 90)
    moveRover(1)
