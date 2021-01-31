#!/usr/bin/env python3

import math
import sys


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

#creates group of words due to the rules
def getThreeGroups(words):
    testData = words[-20000:]
    heldoutData = words[-60000:-20000]
    trainingData = words[:-60000]

    return testData, heldoutData, trainingData

#we can get some info from subtexts
def corporaInfo(testData, trainData, heldoutData):
    p = [testData, trainData, heldoutData]
    for i in p:

        print("Number of words = " + str(len(i)))
        dictW = {}
        for word in i:
            if i in dictW:
                dictW[i] += 1
            else:
                dictW[i] = 1
        print("Number of unique words = " + str(len(dictW.keys())))


def uniformProbabilityCon(unigrams):
    return 1 / len(unigrams)


def unigramProbabilityCon(word, unigrams, trainingData):
    if word not in unigrams:
        return 0
    return unigrams[word] / len(trainingData)


def bigramProbabilityCon(word, prevWord, unigrams, bigrams):
    if (not word + "|" + prevWord in bigrams) and (prevWord not in unigrams):
        return uniformProbabilityCon(unigrams)
    if prevWord not in unigrams:
        return 0
    if not word + "|" + prevWord in bigrams:
        return 0
    return bigrams[word + "|" + prevWord] / unigrams[prevWord]


def trigramProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams):
    if bigramProbabilityCon(word, prevWord1, unigrams, bigrams) == 0:
        return uniformProbabilityCon(unigrams)
    if word + "|" + prevWord1 not in bigrams:
        return 0
    if word + "|" + prevWord1 + " " + prevWord2 not in trigrams:
        return 0
    return trigrams[word + "|" + prevWord1 + " " + prevWord2] / bigrams[prevWord1 + "|" + prevWord2]


def countCrossEntropy(testData, trainingData, unigrams, bigrams, trigrams, lambdas):
    #    unigrams = createDictOfUnigrams(trainingData)
    #    bigrams = createDictOfBigrams(trainingData)
    #    trigrams = creteDictOfTrigrams(trainingData)

    crossEntropy = 0
    prevWord1 = "<s>"
    prevWord2 = "<s>"

    for word in trainingData:
        crossEntropy -= math.log2(
            smoothedProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams, lambdas, trainingData))

        prevWord2 = prevWord1
        prevWord1 = word

    return crossEntropy / len(testData)


def smoothedProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams, lambdas, trainingData):
    prob = 0.000000000000000001
    prob += lambdas[0] * uniformProbabilityCon(unigrams)
    prob += lambdas[1] * unigramProbabilityCon(word, unigrams, trainingData)
    prob += lambdas[2] * bigramProbabilityCon(word, prevWord1, unigrams, bigrams)
    prob += lambdas[3] * trigramProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams)
    return prob




def EMAlgorithm(Data, lambdas, unigrams, bigrams, trigrams, trainingData):
    prevWord1 = "<s>"
    prevWord2 = "<s>"
    lambdasNew = [0, 0, 0, 0]

    lambdasAreEqual = False
    while not lambdasAreEqual:

        for word in Data:
            smoothedProb = smoothedProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams, lambdas,
                                               trainingData)

            lambdasNew[0] += lambdas[0] * uniformProbabilityCon(unigrams) / smoothedProb

            lambdasNew[1] += lambdas[1] * unigramProbabilityCon(word, unigrams, trainingData) / smoothedProb
            lambdasNew[2] += lambdas[2] * bigramProbabilityCon(word, prevWord1, unigrams, bigrams) / smoothedProb
            lambdasNew[3] += lambdas[3] * trigramProbability(word, prevWord1, prevWord2, unigrams, bigrams, trigrams)

            prevWord2 = prevWord1
            prevWord1 = word

            for i in range(0, len(lambdasNew)):
                lambdasNew[i] *= lambdas[i]
            for i in range(0, len(lambdasNew)):
                lambdasNew[i] /= sum(lambdasNew)
        return lambdasNew


# FOR THE WHILE-LOOP TO STOP
def checkLambdas(lambdas, lambdasNew, gate=None):
    if gate is None:
        gate = 0.001

    if abs(lambdasNew[0] - lambdas[0]) < gate and abs(lambdasNew[1] - lambdas[1]) < gate and \
            abs(lambdasNew[3] - lambdas[3]) < gate and abs(lambdasNew[2] - lambdas[2]) < gate:
        return True
    else:
        return False


def createDictOfUnigrams(words):
    unigrams = {}
    for word in words:
        if not word in unigrams:
            unigrams[word] = 1
        else:
            unigrams[word] = unigrams[word] + 1
    unigrams['<s>'] = 1
    return unigrams


def createDictOfBigrams(words):
    bigrams = {}
    prevWord = '<s>'
    for word in words:
        if word + "|" + prevWord in bigrams:
            bigrams[word + "|" + prevWord] += 1
        else:
            bigrams[word + "|" + prevWord] = 1
        prevWord = word
    bigrams["<s>|<s>"] = 1
    return bigrams


def creteDictOfTrigrams(words):
    trigrams = {}
    prevWord2 = '<s>'
    prevWord1 = '<s>'
    for word in words:
        key = word + "|" + prevWord1 + " " + prevWord2
        if key not in trigrams:
            trigrams[key] = 1
        else:
            trigrams[key] += 1
        prevWord2 = prevWord1
        prevWord1 = word
    return trigrams


def optimizeLambdas(heldoutData, lambdas, unigrams, bigrams, trigrams, trainingData):
    while True:
        newL = EMAlgorithm(heldoutData, lambdas, unigrams, bigrams, trigrams, trainingData)
        if checkLambdas(newL, lambdas, 0.001):
            break
        lambdas = newL
    return lambdas


#main method of the program, each step has one paragraph
def runProgram():
    for i in ["TEXTCZ1.txt", "TEXTEN1.txt"]:
        words = getData(i)
        testData, heldoutData, trainingData = getThreeGroups(words)

        unigrams = createDictOfUnigrams(trainingData)
        bigrams = createDictOfBigrams(trainingData)
        trigrams = creteDictOfTrigrams(trainingData)

        lambdas = optimizeLambdas(heldoutData, [0.25, 0.25, 0.25, 0.25], unigrams,
                                  bigrams, trigrams, trainingData)

        '''
        ask for lambdas of training data and than forget it

        lambdas = optimizeLambdas(trainingData, [0.25, 0.25,0.25, 0.25], createDictOfUnigrams(trainingData),
                    createDictOfBigrams(trainingData), creteDictOfTrigrams(trainingData), trainingData)

        [0.9651377538770145, 6.145559214242029e-17, 0.03410393208402081, 4.1095022546902367e-07]
        Cross Entrophy with those lambdas: 75.92532293114601

        '''

        testLambdas(testData, trainingData, unigrams, bigrams, trigrams,lambdas, i)


def modifyLambdas(lambdas, difference):
    newLambdas = [0,0,0,0]
    for i in range(4):
        newLambdas[i] = lambdas[i] - difference * lambdas[i] / sum(lambdas[:3])

    # can be positive or negative
    newLambdas[3] = lambdas[3] + difference
    return newLambdas


def increaseLambdas(lambdas, float):
    return modifyLambdas(lambdas, (1 - lambdas[3]) * float)


def decreaseLambdas(lambdas, float):
    return modifyLambdas(lambdas, (-1) * lambdas[3] * (1 - float))



def testLambdas(testData, trainingData, unigrams, bigrams, trigrams,lambdas, i):
    increase = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
    decrease = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
    with open("LambdaResults" + i, "w") as lr:
        for dec in decrease:
            lr.write("Decrease " + str(dec) + " entropy" + str(
                countCrossEntropy(testData, trainingData, unigrams, bigrams, trigrams, decreaseLambdas(lambdas, dec))) + " with lambdas: " \
                + str(decreaseLambdas(lambdas, dec)))
            lr.write("\n")
        lr.write("\n")
        lr.write("Normal : entropy = " + str(countCrossEntropy(testData, trainingData, unigrams, bigrams, trigrams,lambdas)) + " with lambdas: " + str(lambdas))
        lr.write("\n")
        for inc in increase:
            lr.write("Increase " + str(inc) + " entropy" + str(
                countCrossEntropy(testData, trainingData, unigrams, bigrams, trigrams,(decreaseLambdas(lambdas, dec)))) + " with lambdas: " + str(
                increaseLambdas(lambdas, inc)))
            lr.write("\n")



runProgram()