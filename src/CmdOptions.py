import sys, argparse, logging, re

def createArgParser():
    parser = argparse.ArgumentParser( description = "Wacro, String macro operations")
    
    parser.add_argument(
        "-v",
        "--verbose",
        help ="increase output verbosity",
        default = False,
        action="store_true")

    parser.add_argument(
        "-c",
        "--commands",
        type=str,
        help ="commands string, syntax: [f=hello,r=Doom]")

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help ="input string")

    parser.add_argument(
        "-cf",
        "--commandsfile",
        type=str,
        help ="commands file, syntax: [f=hello,r=Doom]")

    parser.add_argument(
        "-if",
        "--inputfile",
        type=str,
        help ="input file")
    
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help ="output results to file")

    parser.add_argument(
        "-l",
        "--log",
        help ="logs to file",
        default = False,
        action="store_true")

    parser.add_argument(
        "--test",
        help ="runs tests",
        default=False,
        action="store_true")

    parser.add_argument(
        "-t",
        "--terminal",
        help ="starts wacro terminal",
        default=False,
        action="store_true")
    return parser
