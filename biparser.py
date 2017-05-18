#!/opt/bb/bin/python2.7

import sys
from itertools import izip_longest

class ScanData(object):
    def __init__(self):
        self.mines = []
        self.players = []
        self.bombs = []

    def addMine(self, owner, x, y):
        self.mines.append(((float(x), float(y)), owner))

    def addPlayer(self, x, y, dx, dy):
        self.players.append((float(x), float(y), float(dx), float(dy)))

    def addBomb(self, x, y, t):
        self.bombs.append((float(x), float(y), float(t)))

class Status(object):
    def __init__(self, x, y, dx, dy, scan_data):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(dx)
        self.dy = float(dy)
        self.scan_data = scan_data

    def __str__(self):
        return 'COORDS: ' + ' '.join((str(round(x, 2)) for x in (self.x, self.y, self.dx, self.dy)))

class BIParser(object):
    def parseStatus(self, text):
        status_data = text.split()
        if status_data[0] != "STATUS_OUT":
            sys.stderr.write("Status error: " + text)
            return None

        # Create status object
        status_data = status_data[1:]
        x, y, dx, dy = status_data[:4]
        scan_data = self.parseScanData(status_data[4:])
        return Status(x, y, dx, dy, scan_data)

    def parseAccelerate(self, text):
        if text.split()[0] != "ACCELERATE_OUT":
            sys.stderr.write("Accelerate error: " + text)
            return False
        return True

    def parseDrive(self, text):
        if text.split()[0] != "DRIVE_OUT":
            sys.stderr.write("Drive error: " + text)
            return False
        return True

    def parseMines(self, text):
        mines_data = text.split()
        if mines_data[0] != "MINES_OUT":
            return None
        mines = []
        for (owner, x, y) in grouper(3, mines_data[2:]):
            mines.append((owner, x, y))
        return mines

    def parseBrake(self, text):
        if text.split()[0] != "BRAKE_OUT":
            sys.stderr.write("Brake error: " + text)
            return False
        return True

    def parseBomb(self, text):
        if text.split()[0] != "BOMB_OUT":
            return False
        return True

    def parseScan(self, text):
        scan_data = text.split()
        if scan_data[0] != "SCAN_OUT":
            return None
        return self.parseScanData(scan_data[1:])

    def parseScoreboard(self, text):
        data = text.split()
        if data[0] != "SCOREBOARD_OUT":
            sys.stderr.write("Scoreboard error: " + text)
            return None
        scoreboard = {}
        for (player, score, num_mines) in grouper(3, data[1:]):
            scoreboard[player] = (float(score), int(num_mines))
        return scoreboard

    def parseConfigurations(self, text):
        data = text.split()
        if data[0] != "CONFIGURATIONS_OUT":
            sys.stderr.write("Configurations error: " + text)
            return None
        configurations = {}
        for (key, value) in grouper(2, data[1:]):
            configurations[key] = value
        return configurations

    def parseScanData(self, scan_data):
        # Get relevant indices
        mine_index = scan_data.index("MINES")
        player_index = scan_data.index("PLAYERS")
        bomb_index = scan_data.index("BOMBS")

        # Get relevant data
        mine_data = scan_data[mine_index + 1:player_index]
        player_data = scan_data[player_index + 1:bomb_index]
        bomb_data = scan_data[bomb_index + 1:]

        scan_data = ScanData()

        # Populate mine data
        for (owner, x, y) in grouper(3, mine_data[1:]):
            scan_data.addMine(owner, x, y)

        # Populate player data
        for (x, y, dx, dy) in grouper(4, player_data[1:]):
            scan_data.addPlayer(x, y, dx, dy)

        # Populate bomb data
        for (x, y, t) in grouper(3, bomb_data[1:]):
            scan_data.addBomb(x, y, t)

        return scan_data

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
