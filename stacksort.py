#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geoff
#
# Created:     07/10/2012
# Copyright:   (c) Geoff 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import random
import math
import time

commandStack = []
bufferStacks = []
numStacks = 8

def printResults(results):
    outputstring = ""

    for index in reversed(range(0, 60)):
        for index2 in range(0, 8):
            if len(bufferStacks[index2]) > index:
                outputstring = outputstring + str(bufferStacks[index2][index])
            outputstring = outputstring + "\t"
        print outputstring;
        outputstring = ""
    print "[1]\t[2]\t[3]\t[4]\t[5]\t[6]\t[7]\t[8]"

def initBufferStacks():
    for index in range(0, numStacks):
        bufferStacks.append([])
    bufferStacks[0] = range(0, 60)
    random.shuffle(bufferStacks[0])
    print bufferStacks[0]

def splitStacks(stackIndex, start, stop):
    #0 sizedstacks shouldn't get split
    if start == stop:
        return
    #if we have one item, move it to the last stack
    if start + 1 == stop:
        bufferStacks[len(bufferStacks) - 1].append(bufferStacks[stackIndex].pop())
        commandStack.append((stackIndex, len(bufferStacks) - 1))
        printResults([])
        time.sleep(1)
        return
    #make an array of pairs, (value, index in stack)
    #we can sort by value
    cardsToSplit = [(bufferStacks[stackIndex][start+ x], x) for x in range(0, stop - start)]
    #Figure out how many cards we're going to put in each stack
    #we can sort to all the stacks except the one we're pulling from
    numCardsPerStack = math.floor(len(cardsToSplit) / (numStacks - 1))
    #If we have more cards than evenly divide into stacks, keep track of how many should be 1 bigger
    numLargerStacks = len(cardsToSplit) - numCardsPerStack * (numStacks - 1)
    print cardsToSplit
    print numCardsPerStack
    print numLargerStacks
    #sort all the (value, index) pairs
    cardsToSplit.sort()
    #this is the arry of commands
    #there is one per card we're going to move
    localCommandStack = range(start, stop)
    stack = 0
    cardInStack = 0
    cardStack = 0
    recursiveStackIndices = []
    print cardsToSplit
    #If we have larger stacks, temporarily adjust the count per stack up
    if numLargerStacks > 0:
        numCardsPerStack = numCardsPerStack + 1
    for card in cardsToSplit:
        if cardInStack == numCardsPerStack:
            cardInStack = 0
            recursiveStackIndices.append((cardStack, numCardsPerStack))
            cardStack = cardStack + 1
            #keep track of the number of incremented stacks
            if numLargerStacks > 0:
                numLargerStacks = numLargerStacks - 1;
                #once we've done all the boosted stacks,
                #decrement the size so we do normal sized stacks
                if numLargerStacks == 0:
                    numCardsPerStack = numCardsPerStack - 1
        #We skip the current stack when divvying up the cards, since we can
        #only move to other stacks
        if cardStack == stackIndex:
            cardStack = cardStack + 1
        #Take the index out of the (value, index) card pair
        indexOfCard = card[1]
        #replace the command for this card with the (stack we're moving from, stack to move to)
        localCommandStack[indexOfCard] = (stackIndex, cardStack)
        cardInStack = cardInStack + 1

    recursiveStackIndices.append((cardStack, numCardsPerStack))
    print localCommandStack
    #do all the moves and prep for recursive call
    for moveIndex in reversed(range(0, len(localCommandStack))):
        commandStack.append(localCommandStack[moveIndex])
        bufferStacks[localCommandStack[moveIndex][1]].append(bufferStacks[localCommandStack[moveIndex][0]].pop())
        time.sleep(0.7)
        printResults(localCommandStack)
    #now, for each mini-stack we made, do a recursive call, starting with the largest
    recursiveStackIndices.reverse()
    for recursiveCall in recursiveStackIndices:
        splitStacks(recursiveCall[0], len(bufferStacks[recursiveCall[0]]) - int(recursiveCall[1]), len(bufferStacks[recursiveCall[0]]))
    return

def main():
    print 'Hello World'
    initBufferStacks()
    splitStacks(0, 0, 60)
    printResults([])

if __name__ == '__main__':
    main()
