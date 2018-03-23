####
#wordsearch.py
#HW8
#####

from wordsearchclasses import *
from trie import *
import sys

def main():
    """Drives the user interaction loop of a word search game"""
    width = int(sys.argv[1])
    height = int(sys.argv[2])

    ws = WordSearch(width, height, 'wordList.txt')

    print("Word Search!")
    ws.printGrid()

    #The number of words the user has successfully found
    numWords = 0
    #Use a trie to keep track of the words the user has already gotten
    wordsSoFar = Trie()

    done = False
    while not done:
        userWord = input("Enter a word (or press Enter to quit): ")
        
        if userWord == '':
            done = True
        else:
            if wordsSoFar.search(userWord):
                print("You already guessed that word!")
            elif not ws.checkWord(userWord):
                print("That's not in the dictionary!")
            elif not ws.verifyWord(userWord):
                print("That word isn't in the grid!")
            else:
                numWords += 1
                wordsSoFar.add(userWord)
                print("Congratulations! Your score is now: " + str(numWords))

    remainingWords = ws.findRemainingWords(wordsSoFar)
    print("The words you missed were:")
    for w in remainingWords:
        print(w)
    print("You found " + str(numWords) + " out of " + str(numWords + len(remainingWords)) + " words.")

main()