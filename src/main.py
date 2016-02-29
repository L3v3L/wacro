#!/usr/bin/env python
import sys, argparse, logging, re
from StringOperations import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printSelections(body,iteratorArray):
    """prints the current contents of iteratorArray"""
    logging.debug("start printSelections")
    for i in iteratorArray:
        print body[i[0]:i[1]]

def printInputTextWithSelections(body, iteratorArray):
    """prints out the inputted text with the current selections"""
    logging.debug("start printInputTextWithSelections")
    last = 0
    output=""
    for i in iteratorArray:
        output+= body[last:i[0]]
        output+= (bcolors.OKGREEN + body[i[0]:i[1]] + bcolors.ENDC)
        last = i[1]

    output+=  body[last:]
    print output
   
def tests():
    """running a few tests"""
    logging.debug("start tests")
    #Testing Vars
    original = "this is a test text that will serve to test this code out on text operations"
    
    commandTests =[]
    #find and replace
    commandTests.append("[f=text,fi=ex,r=cena]")

    #Error Handling
    commandTests.append("")
    commandTests.append("[")
    commandTests.append("[]")
    commandTests.append("[,,,]")
    commandTests.append("salkjdh")
    commandTests.append("[ss]")
    commandTests.append("[f=text,ss,r=cena]")
    commandTests.append("[f=,fi=,r=a]")
    
    for test in commandTests:
        runCommands(test,original)
    return

def runCommands(commands,inputText):
    """running a commands"""
    logging.debug("start runCommands")
    
    #print "Text to be Wacrod: " + inputText

    #remove casing
    if commands[0] == "[":
        if commands[-1]== "]":
            commands = commands[1:-1]
        else:
            print "Error in capsulating"
            return inputText

    #split commands
    commandArray = commands.split(",")

    #run commands
    newiteratorArray = []
    for c in commandArray:
        cSplit = c.split("=")
        if len(cSplit) == 2:
            para = cSplit[1]
        fun = cSplit[0]
        if fun == "f" or fun=="find":
            newiteratorArray = find(para,inputText)
        if fun == "r" or fun == "replace":
            inputText = replace(para,newiteratorArray,inputText)
        if fun == "ss" or fun == "start":
           newiteratorArray = selectionAtStart(newiteratorArray)
        if fun == "se" or fun == "end":
            newiteratorArray = selectionAtEnd(newiteratorArray)
        if fun == "ms" or fun == "move":
            newiteratorArray = moveSelection(int(para),newiteratorArray)
        if fun == "es" or fun == "expand":
            newiteratorArray = expandSelection(int(para),newiteratorArray)
        if fun == "fs" or fun == "fix":
            newiteratorArray = fixSelections(inputText, newiteratorArray)
        if fun == "fi" or fun == "inside":
            newiteratorArray = findInsideSelection(para, inputText, newiteratorArray)
        if fun == "sl" or fun == "line":
            newiteratorArray = selectAllCurrentLine(inputText, newiteratorArray)
        if fun == "ps" or fun == "print_selection":
            printSelections(inputText, newiteratorArray)
        if fun == "p" or fun == "print ":
            printInputTextWithSelections(inputText, newiteratorArray)
    return inputText


def loadInputFile(path):
    """load input file"""
    logging.debug("start loadInputFile")
    with open(path, 'r') as myfile:
        data=myfile.read()
    return data

def loadCommandFile(path):
    """load commands from file"""
    logging.debug("start loadCommands")
    with open(path, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

def main(args, loglevel):
    """main function"""
    logging.debug("start main")

    #run tests
    if args.test:
        tests()
        return
    
    commands = ""
    inputText = ""

    if args.inputfile:
        inputText = loadInputFile(args.inputfile)
    if args.input:
        inputText = args.input
    if args.commandsfile:
        commands = loadCommandFile(args.commandsfile)
    if args.commands:
        commands = args.commands

    if commands and inputText:
        runCommands(commands,inputText)
    else:
        print "missing input text and/or commands"

    if args.terminal:
        flag = 0
        while(flag == 0):
            inp = raw_input(bcolors.OKBLUE+"\nwacro > "+bcolors.ENDC)
            if inp == "exit":
                flag = 1
            else:
                runCommands(inp,inputText)
            
if (__name__ == '__main__'):
    #if len(sys.argv) < 2:
    #    sys.argv.append("-v")

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


    args = parser.parse_args()
  
    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.log:
        logging.basicConfig(format="%(levelname)s: %(message)s",filename="log.txt",level=loglevel)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    main(args, loglevel) 
