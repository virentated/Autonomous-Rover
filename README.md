
# Autonomous Rover 

A python machine learning project to navigate an autonomous rover through an obstacle course 


## Background Information
The rover this algorithm is made for contains 30 LIDAR sensors that sense obstacles in front of it. The objective of the navigation was to ensure the rover goes from its start point to the finish while avoiding all obstacles in its path
## Tech Stack

Language: Python<br/>
Libraries: Tkinter, Sci-Kit Learn


## Implementation

The project implements a two level deep neural-network to acomplosh its goal. 

The network has been trained using human-monitored data which was built from a Tkinter based GUI. The current heading angle of the rover and the distances ftom the 30 LIDAR sensors are recorded as a total of 31 inputs and the output angle as decided by the human-monitored data is recorded with it.

31 inputs plus the final output is recored into a csv file and this is fed to the neural netowrk for it to learn and finally accomplish its goal. 


## File descriptions

1) testNetwork.py : this code generates a GUI for the human to simulate the rover's movement and select the correct movement slot. Each selection is recorded as a data point. This is then stored in the training_data_final.csv file. The more accurate this data and the better the results of the neural network.

2) trainNetwrok.py: this code takes the data from the csv file and puts it into the the neural network. THe trained network is the model.joblib file.
