import numpy as np
import time
import string
import random
import praw
import re


startHolder = "azaaaa"
endHolder = "zazzzz"
transitionMatrixSize = 35000


def firstOrderChain():
    #Initialize transition matrix forward
    transitionForwards= np.zeros((transitionMatrixSize,transitionMatrixSize)) 
    #Initialize transition matrix back
    transitionBackwards = np.zeros((transitionMatrixSize,transitionMatrixSize)) 
    #Initialize token array
    wordList = []
    wordList.append(startHolder) #beginning of sentence
    wordList.append(endHolder) #end of sentence
    #Initialize forward count array
    countForward = np.zeros(transitionMatrixSize)
    #Open file
    fileptr = open("carsData.txt", "r")
    #Total words
    totalWords = 0

    for line in fileptr:
        #Remove punctuation
        tempLine = re.sub(r"[,.;@#?!&$]+\ *", " ", line)
        for count,word in enumerate(tempLine.split()):
            wordCount = len(tempLine.split())
            #All lowercase to reduce duplicates
            tempWord = word.lower()
            if tempWord in wordList:
                wordIndex = wordList.index(tempWord)
                countForward[wordIndex] +=1
                if count == 0: 
                    countForward[0] += 1
                    transitionForwards[0,wordIndex]+=1
                    transitionBackwards[wordIndex,0]+=1
                    lastWord = tempWord
                    lastWordIndex = wordList.index(lastWord)
                elif count == wordCount-1:
                    countForward[1]+=1
                    transitionForwards[wordIndex,1]+=1
                    transitionBackwards[1, wordIndex]
                    transitionForwards[lastWordIndex, wordIndex]+=1
                    transitionBackwards[wordIndex, lastWordIndex]+=1
                else: 
                    transitionForwards[lastWordIndex, wordIndex]+=1
                    transitionBackwards[wordIndex, lastWordIndex]+=1
                    lastWord = tempWord
                    lastWordIndex = wordList.index(lastWord)
            else:
                totalWords +=1
                wordList.append(tempWord)
                wordIndex = wordList.index(tempWord)
                countForward[wordIndex]+=1
                if count == 0:
                    countForward[0]+=1
                    transitionForwards[0,wordIndex]+=1
                    transitionBackwards[wordIndex,0]+=1
                    lastWord = tempWord
                    lastWordIndex = wordList.index(tempWord)
                elif count == wordCount-1:
                    countForward[1]+=1
                    transitionForwards[wordIndex,1]+=1
                    transitionBackwards[1,wordIndex]+=1
                    transitionForwards[lastWordIndex, wordIndex]+=1
                    transitionBackwards[wordIndex, lastWordIndex]+=1
                else:
                    transitionForwards[lastWordIndex, wordIndex]+=1
                    transitionBackwards[wordIndex, lastWordIndex]+=1
                    lastWord = tempWord
                    lastWordIndex = wordList.index(tempWord)
    return wordList, transitionForwards, transitionBackwards, countForward

def firstOrderSentenceGenerator(wordList, transitionForwards, transitionBackwards, countForward):
    while True:    
        sentence = ""
        tempSentence = ""
        sentFlag = False
        inputFlag = False
        while inputFlag == False:
            seedWord = input("Please enter a seed word.\n")
            seedWord = seedWord.lower()
            # Check if the word is in the list
            if seedWord not in wordList:
                print("Please select a different seed word.")
            else:
                inputFlag = True
        #Backwards
        tempWord = seedWord
        sentence = f"{tempWord}"
        while sentFlag == False:
            probFlag = False
            wordIndex = wordList.index(tempWord)
            probDenominator = countForward[wordIndex]
            randWord = random.randint(1,probDenominator)
            probSum = 0
            i = 0 
            while probFlag == False:
                probSum = probSum + transitionBackwards[wordIndex, i]
                if probSum >= randWord:
                    tempWord = wordList[i]
                    wordIndex = i
                    if wordIndex == 0:
                        probFlag = True
                        sentFlag = True
                    else:
                        sentence = f"{tempWord} {sentence}"
                        probFlag = True
                else:
                    i+=1
        #forwards
        tempWord = seedWord
        sentFlag = False
        while sentFlag == False:
            probFlag = False
            wordIndex = wordList.index(tempWord)
            probDenominator = countForward[wordIndex]
            randWord = random.randint(1,probDenominator)
            probSum = 0
            i = 0 
            while probFlag == False:
                probSum = probSum + transitionForwards[wordIndex, i]
                if probSum >= randWord:
                    tempWord = wordList[i]
                    wordIndex = i
                    if wordIndex == 1:
                        probFlag = True
                        sentFlag = True
                    else:
                        sentence = f"{sentence} {tempWord}"
                        probFlag = True
                else:
                    i+=1
        print(sentence)

def secondOrderChain():
    #Initialize transition matrix forward
    transitionForwards= np.zeros((transitionMatrixSize,transitionMatrixSize)) 
    #Initialize transition matrix back
    transitionBackwards = np.zeros((transitionMatrixSize,transitionMatrixSize)) 
    #Initialize token array
    wordList = []
    start = startHolder #beginning of sentence
    end = endHolder #end of sentence
    #Initialize forward count array
    countForward = np.zeros(transitionMatrixSize)
    #Initialize backwards count array
    countBackwards = np.zeros(transitionMatrixSize)
    #Open file
    fileptr = open("carsData.txt", "r")
    #Total words
    totalWords = 0

    for line in fileptr:
        #Remove punctuation
        tempLine = re.sub(r"[,.;@#?!&$]+\ *", " ", line)
        lastWord = start
        for count,word in enumerate(tempLine.split()):
            wordCount = len(tempLine.split())
            #All lowercase to reduce duplicates
            tempWord = word.lower()
            token = (lastWord, tempWord)
            lastToken = ()
            if token not in wordList:
                wordList.append(token)
            tokenIndex = wordList.index(token)
            countForward[tokenIndex]+=1
            if count == 0:           
                lastWord = tempWord
                lastToken = token
                lastTokenIndex = wordList.index(lastToken)
            elif count == wordCount-1:
                transitionForwards[lastTokenIndex, tokenIndex]+=1  
                transitionBackwards[tokenIndex, lastTokenIndex ]+=1                  
                lastTokenIndex = wordList.index(token)
                endToken = (tempWord, end)
                wordList.append(endToken)
                tokenIndex = wordList.index(endToken)
                transitionForwards[lastTokenIndex, tokenIndex]+=1
                transitionBackwards[tokenIndex, lastTokenIndex]+=1  
            else:
                transitionForwards[lastTokenIndex, tokenIndex]+=1
                transitionBackwards[tokenIndex, lastTokenIndex]+=1
                lastWord = tempWord
                lastTokenIndex = wordList.index(token)
    return wordList, transitionForwards, transitionBackwards, countForward

def secondOrderSentenceGenerator(wordList, transitionForwards, transitionBackwards, countForward):
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
                token = wordList[random.choice(startChoice)]
                inputFlag = True
            else: 
                print("Please select another seed word\n")
    
        if token[0] == startHolder:
            sentence = f"{token[1]}"
        elif token[1] == endHolder:
            sentence = f"{token[0]}"
        else:
            sentence = f"{token[0]} {token[1]}"

        tokenIndex = wordList.index(token)
        #backwards
        while sentFlag == False:
            probFlag = False
            probDenominator = countForward[tokenIndex]
            if probDenominator != 0:
                randWord = random.randint(1,probDenominator)
                probSum = 0
                i = 0 
                while probFlag == False:
                    probSum = probSum + transitionBackwards[tokenIndex, i]
                    if probSum >= randWord:
                        tempToken = wordList[i]
                        tokenIndex = i
                        if tempToken[0] == startHolder:
                            probFlag = True
                            sentFlag = True
                        else:
                           sentence = f"{tempToken[0]} {sentence}"
                           probFlag = True
                    else:
                       i+=1
            else:
                sentFlag = True        
    #forwards
        sentFlag = False
        tokenIndex = wordList.index(token)
        while sentFlag == False:
            probFlag = False
            probDenominator = countForward[tokenIndex]
            if probDenominator != 0:
                randWord = random.randint(1,probDenominator)
                probSum = 0
                i = 0 
                while probFlag == False:
                    probSum = probSum + transitionForwards[tokenIndex, i]
                    if probSum >= randWord:
                        tempToken = wordList[i]
                        tokenIndex = i
                        if tempToken[1] == endHolder:
                            probFlag = True
                            sentFlag = True
                        else:
                            sentence = f"{sentence} {tempToken[1]}"
                            probFlag = True
                    else:
                        i+=1
            else:
                sentFlag = True          
        print(sentence)

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
            for i in range(order-1):
                sentence = f"{sentence} {token[i+1]}"
        elif token[order-1] == endHolder:
            for i in range(order-1):
                sentence = f"{sentence} {token[i]}"
        else:
            for i in range(order):
                sentence = f"{sentence} {token[i]}"
        #Backwards
        tokenIndex = wordList.index(token)
        while sentFlag == False:
            probFlag = False
            probDenominator = countForward[tokenIndex]
            if probDenominator != 0:
                randWord = random.randint(1,probDenominator)
                probSum = 0
                i = 0 
                while probFlag == False:
                    probSum = probSum + transitionForwards[i, tokenIndex]
                    if probSum >= randWord:
                        tempToken = wordList[i]
                        tokenIndex = i
                        if tempToken[0] == startHolder:
                            probFlag = True
                            sentFlag = True
                        else:
                           sentence = f"{tempToken[0]} {sentence}"
                           probFlag = True
                    else:
                       i+=1
            else:
                sentFlag = True 
        sentFlag = False
        #forwards
        tokenIndex = wordList.index(token)
        while sentFlag == False:
            probFlag = False
            probDenominator = countForward[tokenIndex]
            if probDenominator != 0:
                randWord = random.randint(1,probDenominator)
                probSum = 0
                i = 0 
                while probFlag == False:
                    probSum = probSum + transitionForwards[tokenIndex, i]
                    if probSum >= randWord:
                        tempToken = wordList[i]
                        tokenIndex = i
                        if tempToken[order-1] == endHolder:
                            probFlag = True
                            sentFlag = True
                        else:
                            sentence = f"{sentence} {tempToken[1]}"
                            probFlag = True
                    else:
                        i+=1
            else:
                sentFlag = True          

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



