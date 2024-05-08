"""Dynamic Programming -- Get to a Location (2.5 LAB)"""


import math


# Point class
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return f"({self.x}, {self.y})"


class DistanceTracker:
    def __init__(self, target):
        self.distances = []
        self.target = target

    def calc_distance(self, p):
        return math.sqrt(abs((p.x - self.target.x)**2 + (p.y - self.target.y)**2))
    
    def add_point(self, point, iteration):
        self.distances.append((self.calc_distance(point), iteration))
        if len(self.distances) > 3:
            self.distances = self.distances[1:]

    def is_increasing(self):
        if len(self.distances) < 3:
            return False

        return self.distances[0][0] <= self.distances[1][0] <= self.distances[2][0]


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
def step_along(point, target, step_x, step_y, step_back):

    tracker = DistanceTracker(target)
    
    i = 0
    while True:
        
        if i % 3 == 2:  # triggers every three iterations
            # step back by the specified amount
            point.x -= step_back
            point.y -= step_back
        else:
            # step forward by the specified amount
            point.x += step_x
            point.y += step_y
        
        tracker.add_point(point, i+1)
        
        if tracker.is_increasing():
            return min(tracker.distances)
        
        i += 1


# Output
print(f"Point P: {p}")

smallest_dist, iteration = step_along(Point(), p, step_x, step_y, step_back)
print(smallest_dist, iteration)

# TODO: REMOVE ME
print(f"Steps along X Axis: {step_x}")
print(f"Steps along Y Axis: {step_y}")
print(f"Steps taken backwards: {step_back}")
# TODO: REMOVE ME
