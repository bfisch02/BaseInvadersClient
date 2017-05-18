#!/opt/bb/bin/python2.7

import sys
import time
import math
from random import random

# Custom modules
from birequests import BIRequestHandler
from biminemanager import BIMineManager, BIMine
from bilogic import getDirection

SLEEP_INTERVAL = .5

class BIController(object):
    def __init__(self, reqhandler, username, logger):
        self.rh = reqhandler
        self.username = username
        self.logger = logger

    def start(self):
        rh = self.rh
        target = None
        mines = {}
        rand_dir = random() * 6.2
        rh.drive(rand_dir, 90)

        # Game loop
        while True:
            status = rh.status()
            position = (status.x, status.y)
            new_mines = self.__get_mines()
            for mine in new_mines:
                mines[mine["point"]] = mine
            angle = getDirection(self.username, position, mines.values())
            if angle != None:
                speed = 90;
                angle_radians = -1 * angle * math.pi / 180
                rh.drive(angle_radians, speed)
            time.sleep(SLEEP_INTERVAL)

    def __get_mines(self):
        mines = self.rh.mines()
        return [format_mine(mine) for mine in mines]

def format_mine(mine):
    return {
        "owner": mine[0],
        "point": (float(mine[1]), float(mine[2]))
    }
