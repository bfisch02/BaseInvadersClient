#!/opt/bb/bin/python2.7

import sys
import time
import math
from random import random

# Custom modules
from birequests import BIRequestHandler
from biminemanager import BIMineManager, BIMine

SCAN_TIME = 5
BRAKE_THRESHOLD = .5
SLEEP_TIME = .025

class BIController(object):
    def __init__(self, reqhandler, username, logger):
        self.rh = reqhandler
        self.username = username
        self.mineManager = BIMineManager(username, logger)
        self.last_scan_time = 0
        self.target = None
        self.logger = logger

    def start(self):
        rh = self.rh

        # Accelerate in random direction
        rand_dir = random() * 6.2
        rh.accelerate(random() * rand_dir, 1)

        # Game loop
        while True:
            time.sleep(SLEEP_TIME)

            # Update info on owned mines
            scoreboard = rh.scoreboard()
            if scoreboard:
                score, numMines = scoreboard[self.username]
                self.mineManager.updateOwnedCount(numMines)

            # Get status and update coordinates
            status = rh.status()
            if not status:
                continue
            (self.x, self.y, self.dx, self.dy) = \
                    status.x, status.y, status.dx, status.dy
            self.direction = math.atan2(self.dy, self.dx)
            self.speed = math.hypot(self.dx, self.dy)

            # Get nearby mines
            for mine in status.scan_data.mines:
                self.mineManager.addMine(mine)

            # Bomb nearby player
            if status.scan_data.players:
                player_to_bomb = status.scan_data.players[0]
                rh.bomb(player_to_bomb[0], player_to_bomb[1], 30)

            # Use scan (if available) to check owned mine or random location
            if self.last_scan_time + SCAN_TIME < time.time():
                scan = None
                mine = self.mineManager.getMineToScan(self.x, self.y)
                if mine:
                    scan = rh.scan(mine.x, mine.y)
                else:
                    scan = self.randomScan()
                if scan:
                    for mine in scan.mines:
                        self.mineManager.addMine(mine)
                    self.last_scan_time = time.time()

            # Find target
            target, distance = self.mineManager.getClosestAvailable(self.x, self.y)

            # If there is no target, bomb and accelerate
            if not target:
                self.target = None
                self.bombForSpeed()
                rh.accelerate(self.direction, 1)

            else:

                # Get direction to target
                mineDirX = target.x - self.x
                mineDirY = target.y - self.y

                # Handle edge cases
                if abs(mineDirX) > 5000:
                    mineDirX = mineDirX - 10000
                if abs(mineDirY) > 5000:
                    mineDirY = mineDirY - 10000
                mineDirection = math.atan2(mineDirY, mineDirX)

                # Brake if new target or ship moving fast in wrong direction
                if target != self.target or \
                        (self.speed > BRAKE_THRESHOLD and \
                        abs(self.direction - mineDirection) > math.pi):
                    if self.speed > BRAKE_THRESHOLD:
                        rh.accelerate(math.pi + self.direction, 1)
                        rh.brake()
                    else:
                        self.target = target

                # Accelerate towards target at conditional rate
                elif self.target:
                    newSpeed = 1
                    if distance > 4000 and self.speed > 5:
                        self.bombForSpeed()
                    if distance < 100:
                        newSpeed = .2
                    if distance < 50:
                        newSpeed = .1
                    rh.accelerate(mineDirection, newSpeed)

    # Randomly modify direction
    def getNewDirection(self):
        return self.direction + (random() * math.pi / 4) - (math.pi / 8)

    # Bomb behind current direction to pick up speed
    def bombForSpeed(self):
        distance = min(50, self.speed * .2)
        distX = distance * math.cos(self.direction)
        distY = distance * math.sin(self.direction)
        self.rh.bomb(self.x + distX, self.y + distY, 21)

    # Randomly scan within the given radius
    def randomScan(self, radius = 500):
        randX = random() * (2 * radius) + self.x - radius
        randY = random() * (2 * radius) + self.y - radius
        return self.rh.scan(randX, randY)
