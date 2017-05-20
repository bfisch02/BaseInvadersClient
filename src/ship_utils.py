import math

def getDistance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def getAngle(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]
    return -180 * math.atan2(y, x) / math.pi
