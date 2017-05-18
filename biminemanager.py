#!/opt/bb/bin/python2.7

import time
import math

# Min time between discovery and attack
TIME_THRESHOLD = 1

# Text associated with an unknown owner
UNKNOWN_OWNER = '--'

# Mine Class
class BIMine(object):
    def __init__(self, p, owner):
        self.x = p[0]
        self.y = p[1]
        self.owner = owner
        self.owner_changed = 0
        self.found_time = time.time()
        self.last_seen = time.time()

    def setOwner(self, owner):
        self.owner = owner

    def distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

# Mine Manager Class
class BIMineManager(object):
    def __init__(self, username, logger):
        self.username = username
        self.mines = {}
        self.owned_mines = {}
        self.owned_count = 0
        self.owned_time = time.time()
        self.logger = logger

    def addMine(self, mine):
        minePoint = mine[0]
        owner = mine[1]

        # If mine is new, create object
        if minePoint not in self.mines:
            self.mines[minePoint] = BIMine(minePoint, owner)

        # Otherwise, update information
        else:
            mine = self.mines[minePoint]
            old_owner = mine.owner

            # Update owned mines if ownership has changed
            if owner != old_owner:
                if old_owner == self.username:
                    self.owned_count -= 1
                    del self.owned_mines[minePoint]
                elif owner == self.username:
                    self.owned_count += 1
                    self.owned_mines[minePoint] = mine
                mine.setOwner(owner)
                mine.owner_changed += 1

        # Update last_seen time 
        # Note: This information is used when looking for mines to scan
        self.mines[minePoint].last_seen = time.time()

    # Update owned mine count and set time
    # Note: This information is used when looking for mines to scan
    def updateOwnedCount(self, owned_count):
        if self.owned_count != owned_count:
            self.owned_count = owned_count
            self.owned_time = time.time()

    # Return the next mine to scan, or None
    def getMineToScan(self, x, y):

        # If owned_mines length matches with scoreboard count, no work to do
        if len(self.owned_mines) == self.owned_count:
            return None
            
        # Get all mines for which last seen time < last scoreboard update
        outdated_mines = [(k, v) for k, v in self.owned_mines.items() \
                if v.last_seen < self.owned_time]

        # Sort by distance
        outdated_mines = sorted(outdated_mines, \
                key=lambda item: item[1].distance(x, y))

        # If no outdated mines, we have nothing to do
        if len(outdated_mines) == 0:
            return None

        # If there is only one outdated mine, we no longer own it
        elif len(outdated_mines) == 1:
            minePoint, mine = outdated_mines[0]
            mine.setOwner(UNKNOWN_OWNER)
            del self.owned_mines[minePoint]
            return None

        # Return the closest outdated mine
        else:
            return outdated_mines[0][1]

    # Return closest available mine to target, or None
    def getClosestAvailable(self, x, y):
        bestMine = None
        bestDistance = 20000
        for minePoint in self.mines:
            mine = self.mines[minePoint]

            # Criteria:
            # 1) We do not own mine
            # 2) Mine was found at least TIME_THRESHOLD ago
            # 3) Either owner changed fewer than three times or we've seen
            #        at least 5 mines (prevents bad early loop)
            if mine.owner != self.username and \
                    time.time() - mine.found_time > TIME_THRESHOLD and \
                    (mine.owner_changed < 3 or len(self.mines) >= 5):
                distance = mine.distance(x, y)
                if distance < bestDistance:
                    bestDistance = distance
                    bestMine = mine
        return bestMine, bestDistance
