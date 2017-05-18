#!/opt/bb/bin/python2.7

import sys
import math
from random import random
from time import time

mineCaptureTimes = {}

# [
#   {
#     point: (x, y),
#     owner: owner
#   },
#   ...
# ]
def getDirection(username, position, mines):
    closest = None
    closest_distance = 10000

    for mine in mines:
        if mine["owner"] == username and mine["point"] not in mineCaptureTimes:
            mineCaptureTimes[mine["point"]] = time()

    minesToRemove = set()
    for item in mineCaptureTimes:
        if mineCaptureTimes[item] + 5 < time():
            minesToRemove.add(item)
    for mine in minesToRemove:
        del mineCaptureTimes[mine]

    for mine in mines:
        if mine["owner"] != username and mine["point"] not in mineCaptureTimes:
            distance = getDistance(position, mine["point"])
            if distance < closest_distance:
                closest = mine["point"]
                closest_distance = distance
    if closest:
        return getAngle(position, closest)

def getDistance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def getAngle(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]
    return -180 * math.atan2(y, x) / math.pi
