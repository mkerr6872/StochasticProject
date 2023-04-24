import numpy as np
import time
import string
import random
import praw
import re

startHolder = "azaaaa"
endHolder = "zazzzz"
transitionMatrixSize = 35000


def nOrderChain(order):
    transitionForwards= np.zeros((transitionMatrixSize,transitionMatrixSize)) 
    wordList = []
    countForward = np.zeros(transitionMatrixSize)
    #Open file
    fileptr = open("test2.txt", "r")
    for line in fileptr:
        firstToken = []
        firstToken.append(startHolder)
        #Remove punctuation
        tempLine = re.sub(r"[,.;@#?!&$]+\ *", " ", line)
        wordCount = len(tempLine.split())
        if wordCount > order:
            for count,word in enumerate(tempLine.split()):
                wordCount = len(tempLine.split())
                #All lowercase to reduce duplicates
                tempWord = word.lower()   
                if count < order-2:
                    firstToken.append(tempWord)
                elif count == order-2:
                    firstToken.append(tempWord)
                    if firstToken not in wordList:
                        wordList.append(list(firstToken))
                    token = list(firstToken)
                    lastTokenIndex = wordList.index(token)
                    countForward[lastTokenIndex]+=1
                elif count < wordCount-1:
                    token +=[token.pop(0)]
                    token[order-1] = tempWord
                    if token not in wordList:    
                        wordList.append(list(token))
                    tokenIndex = wordList.index(token)
                    countForward[tokenIndex]+=1
                    transitionForwards[lastTokenIndex, tokenIndex]+=1
                    lastTokenIndex = tokenIndex
                else:
                    token +=[token.pop(0)]
                    token[order-1] = tempWord
                    if token not in wordList:   
                        wordList.append(list(token))
                    tokenIndex = wordList.index(token)
                    countForward[tokenIndex]+=1
                    transitionForwards[lastTokenIndex, tokenIndex]+=1
                    lastTokenIndex = tokenIndex
                    token +=[token.pop(0)]
                    token[order-1] = endHolder
                    if token not in wordList: 
                        wordList.append(list(token))
                    tokenIndex = wordList.index(token)
                    transitionForwards[lastTokenIndex, tokenIndex]+=1                    

    return wordList, transitionForwards, countForward

def nOrderSentenceGenerator(wordList, transitionForwards, countForward, order):
    while True:
        sentence = ""
        tempSentence = ""
        sentFlag = False
        inputFlag = False

        # Check if the word is in the list
        while inputFlag == False:
            seedWord = input("Please enter a seed word.\n")
            seedWord = seedWord.lower()
            if any(seedWord in x for x in wordList):
                startChoice = [seedWord in x for x in wordList]
                startChoice = [i for i, x in enumerate(startChoice) if x]
                print(startChoice)
                token = wordList[random.choice(startChoice)]
                print(token)
                inputFlag = True
            else: 
                print("Please select another seed word\n")

        if token[0] == startHolder:
            for i in range(order-2):
                sentence = f"{sentence} {token[i+1]}"
        elif token[1] == endHolder:
            for i in range(order-2):
                sentence = f"{sentence} {token[i]}"
        else:
            for i in range(order-1):
                sentence = f"{sentence} {token[i]}"

        print(sentence) 


def commentScraper():
    rDataCars = open("carsData.txt", "w")
    reddit = praw.Reddit(client_id='VtNzPEQvBnXPraApATXWFg', client_secret='ZPIRrZ5XWNbgWgFvkKPhsVdfVGpTfw', user_agent='Stochastic Project')
    hot_posts = reddit.subreddit('cars').top(limit=25)
    for post in hot_posts:
        post.comments.replace_more(limit=0)
        for top_level_comment in post.comments:
            rDataCars.write(top_level_comment.body)

if __name__ == '__main__':
    #commentScraper()
    #wList, tForward, tbackwards, cForward = firstOrderChain()
    #print(len(wList))
    #firstOrderSentenceGenerator(wList, tForward, tbackwards, cForward)
    #wList, tForward, tbackwards, cForward = secondOrderChain()
    #print(len(wList))
    #secondOrderSentenceGenerator(wList, tForward, tbackwards, cForward)
    wList, tForward, cForward = nOrderChain(3)
    nOrderSentenceGenerator(wList, tForward, cForward, 3)



