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

def findInsideSelection(selector, body, iteratorArray):
    """finding inside a selection"""
    logging.debug("start findInsideSelection")
    newiteratorArray = []
    for i in iteratorArray:
        findResult = find(selector,body[i[0]:i[1]])
        for j in findResult:
            newiteratorArray.append([j[0]+i[0],j[1]+i[0]])
    return newiteratorArray

def seekForward(selector, body, iteratorArray):
    """seeks forward for the next occurence of an input"""
    logging.debug("start seekForward")
    newiteratorArray = []

    for i in iteratorArray:
        findResult = find(selector,body[i[1]:])
        if(findResult):
            newiteratorArray.append([findResult[0][0]+i[1],findResult[0][1]+i[1]])
       
    return newiteratorArray

def seekBack(selector, body, iteratorArray):
    """seeks back for the next occurence of an input"""
    logging.debug("start seekBack")
    newiteratorArray = []

    for i in iteratorArray:
        findResult = find(selector,body[:i[0]])
        if(findResult):
            newiteratorArray.append([findResult[-1][0],findResult[-1][1]])

    return newiteratorArray
