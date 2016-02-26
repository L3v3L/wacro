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

def findInsideSelection(iteratorArray, body, selector):
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
    selector = "text"
    xselector = "ex"
    replacer = "cena"
    
    
    #select all occurences of selector in original
    findResult = find(selector, original)
    #inside each selection, now select all occurences of xselector
    findResult = findInsideSelection(findResult, original, xselector)
    #replace all selections with replacer
    replaceResult =  replace(replacer,findResult,original)
    logging.info(replaceResult)
    return

# Gather our code in a main() function
def main(args, loglevel):
    """main function"""
    logging.debug("start main")
    logging.info('wacro')

    #run tests
    if args.test:
        tests()
        return

if (__name__ == '__main__'):
    #if len(sys.argv) < 2:
    #    sys.argv.append("-v")

    parser = argparse.ArgumentParser( 
                                    description = "String macro operations")
    parser.add_argument(
        "-v",
        "--verbose",
        help ="increase output verbosity",
        default = False,
        action="store_true")

    parser.add_argument(
        "-l",
        "--load",
        type=str,
        help ="load commands from file")

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help ="load text from file")
    
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help ="output results to file")

    parser.add_argument(
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
    
