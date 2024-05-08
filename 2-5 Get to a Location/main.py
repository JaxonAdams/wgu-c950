"""Dynamic Programming -- Get to a Location (2.5 LAB)"""


import math


# Point class
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"({self.x}, {self.y})"

# Main program
# Read in x and y for Point P
p = Point()
p.x = int(input())
p.y = int(input())

# Read in num of steps to be taken in X and Y directions
step_x = int(input())
step_y = int(input())

# Read in num of steps to be taken (backwards) every 3 steps
step_back = int(input())

# Write dynamic programming algorithm

# Output
print(f"Point P: {p}")

# TODO: REMOVE ME
print(f"Steps along X Axis: {step_x}")
print(f"Steps along Y Axis: {step_y}")
print(f"Steps taken backwards: {step_back}")
# TODO: REMOVE ME
