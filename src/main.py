#!/usr/bin/env python
import sys, argparse, logging, re

def find(selector, body):
    """find all occurences of selection"""
    logging.debug("start find")
    findArray = []
    for m in re.finditer(selector, body):
         findArray.append([m.start(), m.end()])
    return findArray

def replace(replacer,iteratorArray,body):
    """replace all selection with replacer"""
    logging.debug("start replace")
    #go to end of array
    b = iteratorArray[::-1]
    for i in b:
        body = body[:i[0]] + body[i[1]:]
        body = body[:i[0]] + replacer + body[i[0]:]
    return body

def selectionAtStart(iteratorArray):
    """shrink selection to start of selection"""
    logging.debug("start selectionAtStart")
    for i in iteratorArray:
        i[1] = i[0]
    return iteratorArray

def selectionAtEnd(iteratorArray):
    """shrink selection to end of selection"""
    logging.debug("start selectionAtEnd")
    for i in iteratorArray:
        i[0] = i[1]
    return iteratorArray

def moveSelection(amount,iteratorArray):
    """moves the cursors of current selection my amount"""
    logging.debug("start moveSelection")
    for i in iteratorArray:
        i[0]= i[0] + amount
        i[1]= i[1] + amount
    return iteratorArray

def expandSelection(amount,iteratorArray):
    """exapanding or contracting selections"""
    logging.debug("start expandSelection")
    for i in iteratorArray:
        i[0]= i[0] - amount
        i[1]= i[1] + amount
        if i[1] < i[0]:
            i[1] = i[0]
    return iteratorArray

def fixSelections(body, iteratorArray ):
    """fixing selections"""
    logging.debug("start fixSelections")
    #check if any iterator out of range
    for i in iteratorArray:
        if i[0] < 0 :
            i[0] = 0
        if i[1] < 0:
            i[1] = 0
        if i[0] >= len(body) :
            i[0] = len(body)
        if i[1] >= len(body):
            i[1] = len(body)
    #TODO check if overlapping
    return iteratorArray

def selectAllCurrentLine(body,iteratorArray):
    """Selects all of the current line"""
    logging.debug("start selectAllCurrentLine")

    for i in iteratorArray:
        flag = 0
        offset = 0
        while(flag == 0):
            selchar = body[i[0] - offset]
            #check if new line
            if(selchar == '\n'):
                i[0] = i[0] - offset
                break
            #check if start of document
            elif((i[0] - offset) == 0):
                i[0] = 0
                break
            
            offset+=1

        flag = 0
        offset = 0
        while(flag == 0):
            selchar = body[i[1] + offset]
            #check if new line
            if(selchar == '\n'):
                i[1] = i[1] + offset
                break
            #check if start of document
            elif((i[1] + offset) == (len(body)-1)):
                i[1] = i[1] + offset + 1
                break
            
            offset+=1

    return iteratorArray

def printSelections(body,iteratorArray):
    """prints the current contents of iteratorArray"""
    logging.debug("start printSelections")
    for i in iteratorArray:
        print body[i[0]:i[1]]
        
def findInsideSelection(selector, body, iteratorArray):
    """finding inside a selection"""
    logging.debug("start findInsideSelection")
    newiteratorArray = []
    for i in iteratorArray:
        findResult = find(selector,body[i[0]:i[1]])
        for j in findResult:
            newiteratorArray.append([j[0]+i[0],j[1]+i[0]])
    return newiteratorArray

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
    commands = commands[1:-1]

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
            print replace(para,newiteratorArray,inputText)
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
        "-t",
        "--test",
        help ="runs tests",
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
