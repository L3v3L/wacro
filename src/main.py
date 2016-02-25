import re

#Testing Vars
original = "this is a test text that will serve to test this code out on text operations"
selector = "text"
xselector = "ex"
replacer = "cena"


def find(selector, body):
    """find all occurences of selection"""
    findArray = []
    for m in re.finditer(selector, body):
         findArray.append([m.start(), m.end()])
    return findArray


def replace(replacer,iteratorArray,body):
    """replace all selection with replacer"""
    #go to end of array
    b = iteratorArray[::-1]
    for i in b:
        body = body[:i[0]] + body[i[1]:]
        body = body[:i[0]] + replacer + body[i[0]:]
    return body


def selectionAtStart(iteratorArray):
    """shrink selection to start of selection"""
    for i in iteratorArray:
        i[1] = i[0]
    return iteratorArray


def selectionAtEnd(iteratorArray):
    """shrink selection to end of selection"""
    for i in iteratorArray:
        i[0] = i[1]
    return iteratorArray

def moveSelection(amount,iteratorArray):
    for i in iteratorArray:
        i[0]= i[0] + amount
        i[1]= i[1] + amount
    return iteratorArray


def expandSelection(amount,iteratorArray):
    """exapanding or contracting selections"""
    for i in iteratorArray:
        i[0]= i[0] - amount
        i[1]= i[1] + amount
        if i[1] < i[0]:
            i[1] = i[0]
    return iteratorArray


def fixSelections(body, iteratorArray ):
    """fixing selections"""
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
    newiteratorArray = []
    for i in iteratorArray:
        findResult = find(selector,body[i[0]:i[1]])
        for j in findResult:
            newiteratorArray.append([j[0]+i[0],j[1]+i[0]])
    return newiteratorArray

def main():
    #select all occurences of selector in original
    findResult = find(selector, original)
    #inside each selection, now select all occurences of xselector
    findResult = findInsideSelection(findResult, original, xselector)
    #replace all selections with replacer
    replaceResult =  replace(replacer,findResult,original)
    print replaceResult

main()
