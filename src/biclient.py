#!/usr/bin/python2.7
import sys

# Custom modules
from src.birequests import BIRequestHandler
from src.bicontroller import BIController

HOST = "34.225.107.187"
PORT = 17429

def initialize(username, password, getDirection):
    if username == "username" or password == "password":
        sys.stderr.write("You did not provide a username or password! Exiting.\n")
        sys.exit(1)
    rh = BIRequestHandler(username, password, HOST, PORT)
    if not rh.initialize():
        sys.stderr.write("Unable to connect to game server! Exiting.\n")
        sys.exit(1)
    else:
        sys.stdout.write("Successfully connected to game server!\n")
    controller = BIController(rh, username, getDirection)
    controller.start()
