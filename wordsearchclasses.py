###
#wordsearchclasses.py
#HW8
####

from trie import *
import random

class WordSearch:
    """A class representing a word search game"""
    def __init__(self, width, height, wordListFilename):
        """Generates a random grid of letters of the given dimensions. Also initializes a dictionary using the given file (should be a list of words, one-per-line"""
        #Create a random grid of letters
        self.grid = []
        for r in range(height):
            self.grid.append([])
            for c in range(width):
                randomASCII = random.randint(ord('a'), ord('z'))
                self.grid[r].append(chr(randomASCII))

        #Construct the dictionary
        #make a Trie
        self.dict = Trie()

        #open the file with the valid words in it
        file = open(wordListFilename, "r")

        #read one line (so it has something to enter the while loop with)
        currLine = file.readline()

        #keep reading while the line is longer than 2 (aka is more than just \n)
        while len(currLine) > 2:

            #add the word to the dictionary, without adding the endline characters
            self.dict.add(currLine[:-1])

            #read the next line to update the while loop
            currLine = file.readline()

    def printGrid(self):
        """Prints the word search grid to the shell"""
        for r in range(len(self.grid)):
            rowStr = ''
            for c in range(len(self.grid[r])):
                rowStr += self.grid[r][c] + " "
            print(rowStr)

    def checkWord(self, word):
        """Returns True if the word is in the dictionary, False otherwise"""

        return self.dict.search(word)

    def verifyWord(self, word):
        """Returns True if the given string can be found on the grid (i.e. the word corresponds to a path of adjacent letters on the grid where no square is used twice)"""

        #to keep track of the characters already used in the word
        usedTable = []

        #for each square in the grid (and to establish indices that can be passed to the helper function)
        for rowIdx in range(len(self.grid)):
            for chIdx in range(len(self.grid[rowIdx])):

                #saves as a variable so it doesn't just return, calls the helper function for the 0 idx of the word
                doesThisChWork = self.verifyHelper(0, word, (rowIdx, chIdx), usedTable)

                #allows it to return true as soon as the word can be found starting at some location
                if doesThisChWork == True:
                    return True

        return False



    def verifyHelper(self, wordIdx, word, gridIdx, usedTable):
        '''helper function for verifyWord, the recursive part'''

        #if the ch in the grid isn't equal to the ch at the wordIdx of word, this way won't make the word
        if self.grid[gridIdx[0]][gridIdx[1]] != word[wordIdx]:
            return False

        #when it's made it all the way to the last idx in the word, that means it makes the word
        elif wordIdx == len(word) - 1:
            return True

        #so the character matches, time to look at the surrounding squares
        else:
            #update usedTable so the gridIdx is in it because we know it matches
            usedTable.append(gridIdx)

            #list of directions to check
            directionsCheck = [(gridIdx[0]-1, gridIdx[1]-1), (gridIdx[0]-1, gridIdx[1]) , (gridIdx[0]-1, gridIdx[1]+1) , (gridIdx[0], gridIdx[1]-1) , (gridIdx[0], gridIdx[1]+1) , (gridIdx[0]+1, gridIdx[1]-1) ,(gridIdx[0]+1, gridIdx[1]) , (gridIdx[0]+1, gridIdx[1]+1)]

            #check all the surrounding squares
            for direction in directionsCheck:
                #but only if the square is in the grid and not already in usedTable
                if direction[0] >= 0 and direction[0] < len(self.grid) and direction[1] >=0 and direction[1] < len(self.grid[gridIdx[0]]) and direction not in usedTable:

                    #saves result from the recusive call (looking at the next letter in the word and the given direction's idx)
                    doesItWork = self.verifyHelper(wordIdx + 1, word, direction, usedTable)

                    #as soon as one of them works it can return True
                    if doesItWork == True:
                        return True


    def findRemainingWords(self, wordsSoFar):
        """Takes a trie of words found so far. Returns the list of all words in the grid that are not in the trie. Note: this function modifies the given trie!"""

        #makes empty list to add missed words to
        missedWords = []

        #for all of the squares in the grid
        for rowIdx in range(len(self.grid)):
            for chIdx in range(len(self.grid[rowIdx])):

                #each time it looks at a new start location usedTable should be empty
                usedTable = []

                #calls the helper function, which will update missedWords appropriately
                self.remainingHelper('', wordsSoFar, missedWords, (rowIdx, chIdx), usedTable)


        return missedWords

    def remainingHelper(self, currStr, wordsSoFar, missedWords, gridIdx, usedTable):
        '''helper function for findRemainingWords, does the recursion, updates missedWords'''

        #add the letter from the square it's checking to currStr
        currStr += self.grid[gridIdx[0]][gridIdx[1]]

        #only does anything if the current string is a prefix to some word in the dictionary
        #aka if no words start the way it currently would start it stops this branch of the recursion
        if self.dict.isPrefix(currStr):

            #if currStr is a word not already in wordsSoFar
            if self.checkWord(currStr) == True and wordsSoFar.search(currStr) == False:

                #add that word to missedWords and wordsSoFar
                missedWords.append(currStr)
                wordsSoFar.add(currStr)

            #list of all the directions to check
            directionsCheck = [(gridIdx[0]-1, gridIdx[1]-1), (gridIdx[0]-1, gridIdx[1]) , (gridIdx[0]-1, gridIdx[1]+1) , (gridIdx[0], gridIdx[1]-1) , (gridIdx[0], gridIdx[1]+1) , (gridIdx[0]+1, gridIdx[1]-1) ,(gridIdx[0]+1, gridIdx[1]) , (gridIdx[0]+1, gridIdx[1]+1)]

            #looks at squares in the grid that are not already in usedTable
            for direction in directionsCheck:
                if direction[0] >= 0 and direction[0] < len(self.grid) and direction[1] >=0 and direction[1] < len(self.grid[gridIdx[0]]) and direction not in usedTable:

                    #it will try to use this new square, so updates usedTable and then calls the recursion for that square
                    usedTable.append(gridIdx)
                    self.remainingHelper(currStr, wordsSoFar, missedWords, direction, usedTable)

                    #once the recursive path runs to the end, it removes the last square added to usedTable
                    usedTable.pop()


