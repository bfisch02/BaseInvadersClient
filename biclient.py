#!/usr/bin/python

import sys
from argparse import ArgumentParser

# Custom modules
from birequests import BIRequestHandler
from bicontroller import BIController

def passLogger(text):
    pass

def printLogger(text):
    print text

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False)
    parser.add_argument('-u', '--username', action='store', dest='username', required=True)
    parser.add_argument('-p', '--password', action='store', dest='password', required=True)
    parser.add_argument('--host', action='store', dest='host', default="34.225.107.187")
    parser.add_argument('--port', action='store', dest='port', default="17429")
    return parser.parse_args()

def main():
    args = parseArgs()

    # Set logger
    logger = passLogger
    if args.verbose:
        logger = printLogger

    rh = BIRequestHandler(args.username, args.password, args.host, args.port)
    if not rh.initialize():
        sys.stderr.write("Unable to initialize tcp connection. Exiting.\n")
        sys.exit(1)
    else:
        logger("Successfully initialized tcp connection")
    controller = BIController(rh, args.username, logger)
    controller.start()

if __name__ == '__main__':
    main()
