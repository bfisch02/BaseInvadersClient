#!/opt/bb/bin/python2.7

import sys
import telnetlib

from biparser import BIParser

class BIRequestHandler(object):
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.parser = BIParser()

    def initialize(self):
        tn = None
        try:
            tn = initializeTcpConnection(self.username, self.password, self.host, self.port)
        except Exception as e:
            sys.stderr.write("Error establishing tcp connection: " + str(e) + "\n")
        if tn:
            self.tn = tn
        return tn != None

    def status(self):
        response = executeCommand(self.tn, "STATUS")
        return self.parser.parseStatus(response)

    def accelerate(self, radians, speed):
        command = " ".join(["ACCELERATE", str(radians), str(speed)])
        response = executeCommand(self.tn, command)
        return self.parser.parseAccelerate(response)

    def drive(self, radians, speed):
        command = " ".join(["DRIVE", str(radians), str(speed)])
        response = executeCommand(self.tn, command)
        return self.parser.parseDrive(response)

    def mines(self):
        response = executeCommand(self.tn, "MINES")
        return self.parser.parseMines(response)

    def brake(self):
        response = executeCommand(self.tn, "BRAKE")
        return self.parser.parseBrake(response)

    def bomb(self, x, y, t = None):
        command = " ".join(["BOMB", str(x), str(y)])
        if t:
            command += " " + str(t)
        response = executeCommand(self.tn, command)
        return self.parser.parseBomb(response)

    def scan(self, x, y):
        command = " ".join(["SCAN", str(x), str(y)])
        response = executeCommand(self.tn, command)
        return self.parser.parseScan(response)
    
    def scoreboard(self):
        response = executeCommand(self.tn, "SCOREBOARD")
        return self.parser.parseScoreboard(response)

    def configurations(self):
        response = executeCommand(self.tn, "CONFIGURATIONS")
        return self.parser.parseConfigurations(response)

def initializeTcpConnection(username, password, host, port):
    tn = telnetlib.Telnet(host, port=port)
    tn.write(username + " " + password + "\n")
    return tn

def executeCommand(tn, cmd):
    tn.write(cmd + "\n")
    rVal = tn.read_until("\n")
    return rVal

