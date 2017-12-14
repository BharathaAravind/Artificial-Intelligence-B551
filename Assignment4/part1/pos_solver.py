###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
# Aravind Bharatha and abharath
# Nawaz Hussain K and nawazkh
# Rahul Pochampally and rpochamp

# (Based on skeleton code by D. Crandall)
#
#
####
# Report:
# For Training:
# 1) We trained the data got the dictionary of words(P(w1|S), transition of words(P(N|N)) and POS probabilities (P(N)).
#
# For Simplified:
# 1) We just check the dictionary of word frequency for a particular words with all POS and return the maximum one.
# 2) FOr the ones we don't have any freq or in case of tie we return NOun as default.
#
# For Variable Elimination:
# We have implemented only forward elimination sequense.
# we caluclated Tow values for the previous words and summed the previous state Tow values and picked the maximum among the current state.
# si*() = arg max P(Si = si|W)
#
# For Viterbi:
# We defined a 2*2 matrix which has all the (S^2 * T)
# We calculate the value for each cell using the previous columns values and keep track of the maximum value POS.
# Our each cell is of this form [probability, PrevMaxValue]
# once we fill our veterbi matrix we backtack and print the sequence
#
# For Posterior Probability:
# We used P(S|W) = P(S) * P(W|S)
#
# References:
# Canvas Slides
# Piazza Posts
####

import random
import math
import operator

import copy
# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label, dictOfWordFreq, POSprob):
        sum = 0
        for word in list(sentence):
            for pos in label:
                if dictOfWordFreq.has_key(word+">"+pos):
                    sum = sum + (math.log10(dictOfWordFreq[word+">"+pos]) + math.log10(POSprob[pos]))
        return sum

    # Do the training!
    #
    def train(self, data):

        print 'Train data'
        dictOfWordFreq = {}
        freqDict = {}
        POSprobabilities = {}
        for i in data:
            for j in range(0, len(i[0])):
                if(POSprobabilities.has_key(i[1][j])):
                    count = POSprobabilities[i[1][j]]
                    count = count+1
                    POSprobabilities[i[1][j]] = count
                else:
                    POSprobabilities[i[1][j]] = 1



                if dictOfWordFreq.has_key(i[0][j] + '>' + i[1][j]):
                    count = dictOfWordFreq[i[0][j] + '>' + i[1][j]]
                    count = count + 1
                    dictOfWordFreq[i[0][j] + '>' + i[1][j]] = count
                else:
                    dictOfWordFreq[i[0][j] + '>' + i[1][j]] = 1

        total = sum(dictOfWordFreq.values())
        for key in dictOfWordFreq.keys():
            dictOfWordFreq[key] = dictOfWordFreq[key]/float(POSprobabilities[key.split(">")[1]])

        total = sum(POSprobabilities.values())

        for key in POSprobabilities.keys():
            POSprobabilities[key] = POSprobabilities[key]/float(total)

        # print POSprobabilities
        # total = sum(dictOfWordFreq.values())
        # for key in dictOfWordFreq.keys():
        #     dictOfWordFreq[key] = dictOfWordFreq[key]/float(total)

        transitionDict = {}
        pos = []
        totalMap = {}
        for i in range(0,len(data)):
            # print data
            dummy = data[i][1]

            for j in range(0,len(dummy)-1):

                if totalMap.has_key(dummy[j]):
                    totalMap[dummy[j]] = totalMap[dummy[j]] + 1
                else:
                    totalMap[dummy[j]] = 1
                pos.append(dummy[j])
                pos.append(dummy[j+1])
                if(transitionDict.has_key(dummy[j]+'>'+dummy[j+1])):
                    count = transitionDict[dummy[j]+'>'+dummy[j+1]];
                    count = count+1
                    transitionDict[dummy[j] + '>' + dummy[j + 1]] = count;
                else:
                    transitionDict[dummy[j]+'>'+dummy[j+1]] = 1

        # total = sum(transitionDict.values())

        for key in transitionDict.keys():
            transitionDict[key] = transitionDict[key]/float(totalMap[key.split(">")[1]])

        return [dictOfWordFreq,transitionDict,POSprobabilities]

    # Functions for each algorithm.
    #

    def simplified(self, sentence, dictOfWordFreq,POSprobabilities):
        l = ["noun"] * len(sentence)
        index = 0
        for word in sentence:
            max = 0
            for pos in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                if dictOfWordFreq.has_key(word + ">" + pos):
                    if max < dictOfWordFreq[word + ">" + pos] * POSprobabilities[pos]:
                        max = dictOfWordFreq[word + ">" + pos] * POSprobabilities[pos]
                        l[index] = pos
            index = index + 1
        return l

    def hmm_ve(self, sentence, dictOfWordFreq,transitionProb,POSprobs):

        l = ["noun"] * len(sentence)
        index = 0
        firstWord = sentence[0]
        max = 0

        temp = {}
        temp1 = {}
        #for first word
        for pos in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
            if dictOfWordFreq.has_key(firstWord + ">" + pos):
                temp[pos+">0"] = dictOfWordFreq[firstWord + ">" + pos]*POSprobs[pos]
                if max < dictOfWordFreq[firstWord + ">" + pos]*POSprobs[pos]:
                    max = dictOfWordFreq[firstWord + ">" + pos]*POSprobs[pos]
                    l[0] = pos
        sumPorbs = 0

        #for calculating the elimination sequnce tow:
        for i in range(1, len(sentence)):
            mm = 0
            for posCurrent in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                sumPorbs = 0
                for posPrevious in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                    if transitionProb.has_key(posPrevious+">"+posCurrent) and dictOfWordFreq.has_key(sentence[i-1]+">"+posPrevious):
                        sumPorbs = sumPorbs + transitionProb[posPrevious+">"+posCurrent]*POSprobs[posPrevious]*dictOfWordFreq[sentence[i-1]+">"+posPrevious]
                temp[posCurrent+">"+str(i)] = sumPorbs

        for i in range(len(sentence)-2,0,-1):
            for posCurrent in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                sumPorbs = 0
                for posPrevious in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                    if transitionProb.has_key(posPrevious+">"+posCurrent) and dictOfWordFreq.has_key(sentence[i]+">"+posCurrent):
                        sumPorbs = sumPorbs+transitionProb[posPrevious+">"+posCurrent]*POSprobs[posCurrent]*dictOfWordFreq[sentence[i]+">"+posCurrent]
                temp1[posPrevious+">"+str(i)] = sumPorbs


        for i in range(1, len(sentence)):
            max = 0
            for posCurrent in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                sum1 = 0
                for posPrev in ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']:
                    if temp.has_key((posPrev+">"+str(i-1))):
                        sum1 = sum1 + temp[posPrev+">"+str(i-1)]
                if dictOfWordFreq.has_key(sentence[i] + ">" + posCurrent):
                    if max < dictOfWordFreq[sentence[i] + ">" + posCurrent]*POSprobs[posCurrent] * sum1:
                        max = dictOfWordFreq[sentence[i] + ">" + posCurrent]*POSprobs[posCurrent] * sum1
                        l[i] = posCurrent
        return l

    def hmm_viterbi(self, sentence, dictOfWordFreq,transitionProb,POSprobs):
        # print dictOfWordFreq

        l = ["noun"] * len(sentence)
        viterbiMatrix = []
        for i in range(0,12):
            temp = []
            for word in sentence:
                temp.append([0,''])
            viterbiMatrix.append(temp)
        posList = ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']

        for word in range(0,1):
            row = 0
            for currentPOS in range(0,len(posList)):
                if dictOfWordFreq.has_key(sentence[word]+">"+posList[currentPOS]):
                    viterbiMatrix[row][0] = [-math.log10(dictOfWordFreq[sentence[word]+">"+posList[currentPOS]]*POSprobs[posList[currentPOS]]),'q1']
                row = row+1

        for word in range(1,len(sentence)):
            for currentPOS in range(0,len(posList)):
                temp = {}
                for previousPOS in range(0,len(posList)):
                    if dictOfWordFreq.has_key(sentence[word]+">"+posList[currentPOS]) and transitionProb.has_key(posList[previousPOS]+">"+posList[currentPOS]):
                        temp[previousPOS] = viterbiMatrix[previousPOS][word-1][0]-math.log10(dictOfWordFreq[sentence[word]+">"+posList[currentPOS]])-math.log10(transitionProb[posList[previousPOS]+">"+posList[currentPOS]])
                    else:
                        if not dictOfWordFreq.has_key(sentence[word]+">"+posList[currentPOS]):
                            if transitionProb.has_key(posList[previousPOS]+">"+posList[currentPOS]):
                                temp[previousPOS] = viterbiMatrix[previousPOS][word-1][0] - math.log10(transitionProb[posList[previousPOS]+">"+posList[currentPOS]]) + 9
                            else:
                                temp[previousPOS] = viterbiMatrix[previousPOS][word - 1][0]  + 15
                        else:
                            if not transitionProb.has_key(posList[previousPOS]+">"+posList[currentPOS]):
                                temp[previousPOS] = viterbiMatrix[previousPOS][word - 1][0] - math.log10(dictOfWordFreq[sentence[word]+">"+posList[currentPOS]]) + 6
                            else:
                                temp[previousPOS] = viterbiMatrix[previousPOS][word - 1][0] + 15
                min = math.pow(10,100)
                minKey = ''
                for key in temp.keys():
                    if min>temp[key]:
                        min = temp[key]
                        minKey = posList[key]

                viterbiMatrix[currentPOS][word] = [min,minKey]


        min = math.pow(10,10)
        for row in range(0,len(posList)):
            if min>viterbiMatrix[row][len(sentence)-1][0]:
                l[len(sentence)-1] = posList[row]
                min = viterbiMatrix[row][len(sentence)-1][0]
        poss = {
            'adv':0, 'noun':1, 'adp':2, 'pron':3, 'det':4, 'num':5, '.':6, 'prt':7, 'verb':8, 'x':9, 'conj':10, 'adj':11
        }
        for col in range(len(sentence)-1,0,-1):
            l[col-1] = viterbiMatrix[poss[l[col]]][col][1]

        min = math.pow(10,10)
        for row in range(0,len(posList)):
            if min>viterbiMatrix[row][0][0] and viterbiMatrix[row][0][0]!=0:
                l[0] = posList[row]
                min = viterbiMatrix[row][0][0]

        return l


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence, dictOfWordFreq,transitionProb,POSprobs):
        if algo == "Simplified":
            return self.simplified(sentence, dictOfWordFreq,POSprobs)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence, dictOfWordFreq,transitionProb,POSprobs)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence, dictOfWordFreq,transitionProb,POSprobs)
        else:
            print "Unknown algo!"
