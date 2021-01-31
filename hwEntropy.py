#!/usr/bin/env python3

import math as m
import random as r
import sys
import operator as o


# This function gets the name of file as a program argument and returns the array of words

def getData(filename=None):
    if filename is None:
        filename = sys.argv[1]
    myFile = open(filename, "r", encoding="iso-8859-2")
    words = []
    for word in myFile.read().split("\n"):
        if len(word) > 0:
            words.append(word.strip())

    myFile.close()
    return words


def createWordAndCharDictionaries(listOfWords, wordDict, CharDict):
    for word in listOfWords:
        if word in wordDict:
            wordDict[word] = wordDict[word] + 1
        else:
            wordDict[word] = 1
        for char in word:
            if char in CharDict:
                CharDict[char] = CharDict[char] + 1
            else:
                CharDict[char] = 1
    return wordDict, CharDict

##this method is used in next solution
def createBigrams(words):

    bigrams = {}

    prevWord = "<s>"
    for word in words:

        if word + "|" + prevWord in bigrams:
            bigrams[word + "|" + prevWord] += 1
        else:
            bigrams[word + "|" + prevWord] = 1
        prevWord = word


    return bigrams


##this method is used in next solution
def createUnigrams(words):
    unigramCounts = {}
    for word in words:
        if word in unigramCounts:
            unigramCounts[word] += 1
        else:
            unigramCounts[word] = 1
    unigramCounts["<s>"] = 1
    return unigramCounts

def getEntrophy(dictOfBigrams, dictOfUnigrams):
    entropy = 0
    unigramValues = sum(dictOfUnigrams.values())


    for bigram in dictOfBigrams:
        joinedProbability = dictOfBigrams[bigram] / unigramValues
        conditionalProbability = dictOfBigrams[bigram] / dictOfUnigrams[bigram.split("|")[1]]
        entropy -= (joinedProbability * m.log2(conditionalProbability))
    return entropy


def getPerplexity(entropy):
    return 2 ** entropy



def runTheWholeScript(name):
    # Here I create all the dictionaries and lists of words and chars that I could use.
    #Basic set of the script
    listOfWords = getData(name + ".txt")
    dictOfChars = {}
    dictOfWords = {}
    dictOfWords, dictOfChars = createWordAndCharDictionaries(listOfWords, dictOfWords, dictOfChars)
    #getEntrophy(createBigrams(listOfWords), createUnigrams(listOfWords))

    listOfUniqueChars = list(dictOfChars.keys())
    listOfUniqueWords = list(dictOfWords.keys())
    numOfIterations = 10
    messUpProbs = [0.1, 0.05, 0.01, 0.001, 0.0001, 0.00001]





    with open(name + "RESULTS.txt", "w", encoding="utf-8") as f:

        for messup in ["characters", "words"]:
            print("Program is now messing up " + messup)
            f.write("=============================================\n")
            f.write("Program is now messing up " + messup + "\n")
            for currProb in messUpProbs:
                listOfEntropies = []
                listOfWCounts = []
                listOfCCounts = []
                listOfBiggestFrequencies = []
                listOfUniqFrequency = []
                dictOfUnigrams = {}
                dictOfBigrams = {}
                newListOfWords = []

                for iter in range(numOfIterations):
                    print("num of iter = ",iter)
                    dictOfBigrams.clear()
                    dictOfUnigrams.clear()
                    newListOfWords.clear()
                    listOfUniqFrequency.clear()
                    prevWord = "<s>"
                    dictOfUnigrams["<s>"] = 1
                    for word in listOfWords:
                        currentWord = word
                        if messup == "words":
                            if r.random() <= currProb:
                                currentWord = r.choice(listOfUniqueWords)
                        else:
                            currentWord = list(currentWord)
                            for i in range(0, len(currentWord)):
                                if r.random() <= currProb:
                                    currentWord[i] = r.choice(listOfUniqueChars)
                            currentWord = ''.join(currentWord)


                        if currentWord in dictOfUnigrams:
                            dictOfUnigrams[currentWord] += 1
                        else:
                            dictOfUnigrams[currentWord] = 1


                        if (currentWord + "|" + prevWord) not in dictOfBigrams:
                            dictOfBigrams[(currentWord + "|" + prevWord)] = 1
                        else:
                            dictOfBigrams[(currentWord + "|" + prevWord)] += 1


                        newListOfWords.append(currentWord)
                        if not currentWord in dictOfUnigrams:
                            dictOfUnigrams[currentWord] = 1
                        else:
                            dictOfUnigrams[currentWord] += 1

                        prevWord = currentWord

                    print("End of messing up, now counting")

                   #Entrophy
                    entr = getEntrophy(dictOfBigrams, dictOfUnigrams)
                    listOfEntropies.append(entr)
                   #Word counts
                    listOfWCounts.append(len(dictOfUnigrams))
                   #char counts
                    numChars = 0
                    for x in newListOfWords:
                        numChars += len(x)
                    listOfCCounts.append(numChars)
                    # biggest frequency
                    listOfBiggestFrequencies.append(max(dictOfUnigrams.items(), key=o.itemgetter(1))[1])
                    #unique frequencies
                    howMany = 0
                    for i in dictOfUnigrams:
                        if dictOfUnigrams[i] == 1:
                            howMany += 1
                    listOfUniqFrequency.append(howMany)

                f.write("--------------------------------------------------------\n")
                f.write("Messup: " + str(currProb) + "\n")
                f.write("Entropies: " + str(listOfEntropies))

                f.write("\n\tAverrage: " + str(sum(listOfEntropies) / len(listOfEntropies)) + "\n")
                f.write("M:" + str(currProb) + ":E:" + messup + ":A:" + str(sum(listOfEntropies) / len(listOfEntropies)) +
                        ":Min:" + str(min(listOfEntropies)) + ":Max:" + str(max(listOfEntropies))+":\n")
                f.write("Perplexity: " + str([getPerplexity(x) for x in listOfEntropies]))
                f.write("\n\tAverrage: " + str(sum([getPerplexity(x) for x in listOfEntropies]) / len(listOfEntropies)) + "\n")
                f.write("M:" + str(currProb) + ":P:" + messup + ":A:" + str(sum([getPerplexity(x) for x in listOfEntropies]) )+ ":\n")
                f.write("Word count: " + str(listOfWCounts))
                f.write("\n\tAverrage: " + str(sum(listOfWCounts) / len(listOfWCounts)) + "\n")
                f.write("M:" + str(currProb) + ":WC:" + messup + ":A:" + str(sum(listOfWCounts) / len(listOfWCounts)) + ":\n")

                f.write("Number of characters: " + str(listOfCCounts))
                f.write("\n\tAverrage: " + str(sum(listOfCCounts) / len(listOfCCounts)) + "\n")
                f.write("M:" + str(currProb) + ":NC:" + messup + ":A:" + str(sum(listOfCCounts) / len(listOfCCounts)) + ":\n")

                f.write("Number of characters per word: " + str([x / len(newListOfWords) for x in listOfCCounts if len(newListOfWords) > 0]))
                f.write("\n\tAverrage: " + str(sum([x / len(newListOfWords) for x in listOfCCounts]) / len(
                    [x / len(newListOfWords) for x in listOfCCounts])) + "\n")
                f.write("M:" + str(currProb) + ":NCPW:" + messup + ":A:" + str(sum([x / len(newListOfWords) for x in listOfCCounts]) / len(
                    [x / len(newListOfWords) for x in listOfCCounts])) + ":\n")

                f.write("Biggest frequency: " + str(listOfBiggestFrequencies))
                f.write("\n\tAverrage: " + str(sum(listOfBiggestFrequencies) / len(listOfBiggestFrequencies)) + "\n")
                f.write("M:" + str(currProb) + ":BF:" + messup + ":A:" + str(sum(listOfBiggestFrequencies) / len(listOfBiggestFrequencies)) +":\n")

                f.write("Words with frequency 1: " + str(len(listOfUniqFrequency)))
                f.write("\n\tAverrage: " + str(sum(listOfUniqFrequency) / len(listOfUniqFrequency)) + "\n")
                f.write("M:" + str(currProb) + ":UF:" + messup + ":A:" + str(sum(listOfUniqFrequency) / len(listOfUniqFrequency)) + ":\n")
                f.write("\n\n")

                listOfEntropies.clear()
                listOfBiggestFrequencies.clear()
                listOfCCounts.clear()
                listOfWCounts.clear()
                newListOfWords.clear()
                dictOfUnigrams.clear()
                dictOfBigrams.clear()

for i in ["TEXTEN1", "TEXTCZ1", "TEXTOBA"]:
    runTheWholeScript(i)
