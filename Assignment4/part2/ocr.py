#!/usr/bin/python
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: (insert names here)
# Your names and user ids:
# Aravind Bharatha and abharath
# Nawaz Hussain K and nawazkh
# Rahul Pochampally and rpochamp
#
# Report:
# For Training:
# 1) We trained the data got the dictionary of chars(P(w1|S), transition of chars(P(N|N)).
# 2) FOr emission probabilities we used hit and miss ratio.
# 3) If out 14 * 25 has more than 340 blank spaces we assign a high prbabilty forspace
# 4) for other characters we divide the hit/miss and then normalize the data by dividing with the total of the sum of all the values.
#   This is done to avoid the probabilites to go over 1.
# 5) FOr transition prbabilities we add a high number and divide a low number to normalize the values. This is done to avoid the domination of transition in our answers.
#    The idea was taken from a paper mentioned in refernces.
#   We noticed that the transition probabilties were dominating so we changed to this.
#
# For Simplified:
# 1) We just check the hit/miss ratio for a particular char and returned the maximum one
# 2) For spaces if the no.of chars is greater than 340 we send a high probability to space
# 3) We take only the top 3 emission probabilities for the given state. By doing this we got better results
#
# For Variable Elimination:
# We have implemented only forward elimination sequence. We used a matrix and formed a tow table
# we take the sum of all the Tow values of previous column and multiply with the emission and fill the consecutive column.
# 3) We take only the top 3 emission probabilities for the given state. By doing this we got better results
#
# For Viterbi:
# We defined a 2*2 matrix which has all the (S^2 * T)
# We also added weights to our transition variables and giving max weight to the emission to get better results.
# We calculate the value for each cell using the previous columns values and keep track of the maximum value POS.
# Our each cell is of this form [probability, PrevMaxValue]
# once we fill our veterbi matrix we back track and print the sequence
#
#
# References:
# Canvas Slides
# Piazza Posts
# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.141.7177&rep=rep1&type=pdf
####

import math

from PIL import Image, ImageDraw, ImageFont
import sys
import operator

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    # print im.size
    # print int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work.
# You can delete them and put your own code here!


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print "\n".join([ r for r in train_letters['a'] ])

# Same with test letters. Here's what the third letter of the test data
#  looks like:
# print "\n".join([ r for r in test_letters[2] ])

# for letters in test_letters:
#     print "\n".join([r for r in letters])


def read_data():
    fname = train_txt_fname
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w for w in line.split()])
        # exemplars += [ (data[0::2], data[1::2]), ]
        exemplars += [[data]]
    return exemplars

def train():

    exemplars = read_data()
    trasitionsDict = {}
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    for data in exemplars:
        # print data[0]
        s = (" ").join(data[0])
        # print s
        for i in range(0,len(s)-1):
            if (s[i] in TRAIN_LETTERS) and (s[i+1] in TRAIN_LETTERS) and trasitionsDict.has_key(s[i]+">"+s[i+1]):
                trasitionsDict[s[i] + ">" + s[i + 1]] = trasitionsDict[s[i] + ">" + s[i + 1]]+1
            else:
                if (s[i] in TRAIN_LETTERS) and (s[i+1] in TRAIN_LETTERS):
                    trasitionsDict[s[i] + ">" + s[i + 1]] = 1


    trasitionsSum = {}
    for i in range(0,len(TRAIN_LETTERS)):
        sumP = 0
        for key in trasitionsDict.keys():
            if(TRAIN_LETTERS[i]==key.split('>')[0]):
                sumP = sumP+trasitionsDict[key]
        if sumP !=0:
            trasitionsSum[TRAIN_LETTERS[i]] = sumP

    for key in trasitionsDict.keys():
        trasitionsDict[key] = (trasitionsDict[key]) / (float(trasitionsSum[key.split(">")[0]]))
        #trasitionsDict[key] = (trasitionsDict[key] + math.pow(10,10)) / (float(trasitionsSum[key.split(">")[0]]) + math.pow(10, 10))

    # print trasitionsDict
    firstCharFeq = {}
    total = sum(trasitionsDict.values())
    for key in trasitionsDict.keys():
        trasitionsDict[key] = trasitionsDict[key] / float(total)
    # print trasitionsDict
    for data in exemplars:
        # print data[0]
        for word in data[0]:
            if word[0] in TRAIN_LETTERS:
                if firstCharFeq.has_key(word[0]):
                    firstCharFeq[word[0]] = firstCharFeq[word[0]] + 1
                else:
                    firstCharFeq[word[0]] = 1

    # print firstCharFeq
    total = sum(firstCharFeq.values())
    for key in firstCharFeq.keys():
        firstCharFeq[key] = firstCharFeq[key]/float(total)
    # print firstCharFeq

    totalChars = 0
    dictOfCharFreq = {}
    for data in exemplars:
        # print data[0]
        s = (" ").join(data[0])
        for char in s:
            if char in TRAIN_LETTERS:
                totalChars = totalChars+1
                if dictOfCharFreq.has_key(char):
                    dictOfCharFreq[char] = dictOfCharFreq[char] + 1
                else:
                    dictOfCharFreq[char] = 1
    # print dictOfCharFreq
    # print totalChars

    for key in dictOfCharFreq.keys():
        dictOfCharFreq[key] = (dictOfCharFreq[key]+math.pow(10,10))/(float(totalChars)+math.pow(10,10))
    # print dictOfCharFreq
    total = sum(dictOfCharFreq.values())

    for key in dictOfCharFreq.keys():
        dictOfCharFreq[key] = dictOfCharFreq[key]/float(total)
    # print dictOfCharFreq
    return [dictOfCharFreq,trasitionsDict,firstCharFeq]

#Compares the lists and returns the hit/miss ratio of a character
def compareLists(testLetter):

    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    possibleLetter = {}
    for i in TRAIN_LETTERS:
        count = 0
        miss = 1
        spaceCount = 0
        for index in range(0, len(testLetter)):
            for imageBits in range(0, len(testLetter[index])):
                if testLetter[index][imageBits] == ' ' and train_letters[i][index][imageBits] == ' ':
                    spaceCount = spaceCount + 1
                    pass
                else:
                    if testLetter[index][imageBits] == train_letters[i][index][imageBits]:
                        count = count + 1
                    else:
                        miss = miss + 1
        possibleLetter[' '] = 0.3
        if spaceCount > 340:
            possibleLetter[i] = spaceCount / float(14*25)
        else:
            possibleLetter[i] = count/float(miss)

    # total =0
    # for key in possibleLetter.keys():
    #     if key!=" ":
    #         total = total + possibleLetter[key]
    #     else:
    #         total = total + 1
    # for key in possibleLetter.keys():
    #     if key!=" ":
    #         possibleLetter[key]= possibleLetter[key]/float(total)


    return max(possibleLetter.iteritems(), key=operator.itemgetter(1))[0]

# compares train and test letter based on hit and miss ratio this is used in ve and viterbi
# Returns the top 3 letter with hugh miss and hit ratio
def compareLists_map(testLetter,flag):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    possibleLetter = {}
    for i in TRAIN_LETTERS:
        count = 0
        miss = 1
        spaceCount = 0
        for index in range(0, len(testLetter)):
            for imageBits in range(0, len(testLetter[index])):
                if testLetter[index][imageBits] == ' ' and train_letters[i][index][imageBits] == ' ':
                    spaceCount = spaceCount + 1
                    pass
                else:
                    if testLetter[index][imageBits] == train_letters[i][index][imageBits]:
                        count = count + 1
                    else:
                        miss = miss + 1
            possibleLetter[' '] = 0.3
            if spaceCount > 340:
                possibleLetter[i] = spaceCount# / float(14 * 25)
            else:
                possibleLetter[i] = count / float(miss)

    total = 0
    for key in possibleLetter.keys():
        if key != " ":
            total = total + possibleLetter[key]
        else:
            total = total + 2
    for key in possibleLetter.keys():
        if key != " ":
            if possibleLetter[key] != 0:
                possibleLetter[key] = possibleLetter[key] / float(total)
            else:
                possibleLetter[key] = 0.0000001
    # print possibleLetter
    if flag==0:
        returnLetter = dict(sorted(possibleLetter.iteritems(), key=operator.itemgetter(1), reverse=True)[:3])
    if flag==1:
        returnLetter = possibleLetter
    # print returnLetter
    return returnLetter


#SImplified algo code
def simplified(test_letters):
    l = ''
    for letters in test_letters:
        l = l + compareLists(letters)
    return  l

#Variable eliminiation code
def hmm_ve(test_letters):
    l = ['0'] * len(test_letters)

    veMatrix = []
    for i in range(0, len(TRAIN_LETTERS)):
        temp = []
        for j in range(0, len(test_letters)):
            temp.append(0)
        veMatrix.append(temp)

    firstletter = compareLists_map(test_letters[0],0)
    for row in range(0, len(TRAIN_LETTERS)):
        if firstCharFeq.has_key(TRAIN_LETTERS[row]) and firstletter.has_key(TRAIN_LETTERS[row]) and firstletter[
            TRAIN_LETTERS[row]] != 0:
            veMatrix[row][0] = - math.log10(firstletter[TRAIN_LETTERS[row]])

    for col in range(1, len(test_letters)):
        possibleLetter = compareLists_map(test_letters[col],0)
        if possibleLetter.has_key(' '):
            l[col] = ' '
        # currentRow = 0
        for key in possibleLetter.keys():
            temp = {}
            sum1 = 0
            for row in range(0, len(TRAIN_LETTERS)):
                if trasitionsDict.has_key(TRAIN_LETTERS[row] + ">" + key) and possibleLetter.has_key(key):
                    temp[TRAIN_LETTERS[row]] = veMatrix[row][col - 1] - math.log10(
                        trasitionsDict[TRAIN_LETTERS[row] + ">" + key]) - math.log10(possibleLetter[key])
            for key1 in temp.keys():
                sum1 = sum1 + temp[key1]

            if dictOfCharFreq.has_key(TRAIN_LETTERS[TRAIN_LETTERS.index(key)]):
                veMatrix[TRAIN_LETTERS.index(key)][col] = sum1 - math.log10(dictOfCharFreq[TRAIN_LETTERS[TRAIN_LETTERS.index(key)]])
            else:
                veMatrix[TRAIN_LETTERS.index(key)][col] = veMatrix[TRAIN_LETTERS.index(key)][col - 1]

    # rowCount = 0
    # for row in veMatrix:
    #     dummy = ''
    #     for col in row:
    #         dummy = dummy + str(col) + " "
    #     print TRAIN_LETTERS[rowCount] + " " + dummy
    #     rowCount = rowCount + 1
    # print 'after'

    # for col in range(len(test_letters) - 1, 0,-1):
    #     previousHighPOS = ''
    #     min = math.pow(10, 100)
    #     for row in range(0, len(TRAIN_LETTERS)):
    #         if previousHighPOS == '':
    #             if min > viterbiMatrix[row][col] and viterbiMatrix[row][col] != 0:
    #                 min = viterbiMatrix[row][col]
    #                 previousHighPOS = TRAIN_LETTERS[row]
    #     if trasitionsDict.has_key(TRAIN_LETTERS[row] + ">" + previousHighPOS):
    #         viterbiMatrix[row][col] = viterbiMatrix[row][col] - math.log10(trasitionsDict[TRAIN_LETTERS[row] + ">" + previousHighPOS])

    max = math.pow(10, 101)
    for row in range(0, len(TRAIN_LETTERS)):
        if max > veMatrix[row][0] and veMatrix[row][0] != 0:
            max = veMatrix[row][0]
            l[0] = TRAIN_LETTERS[row]
    #
    for col in range(1, len(test_letters)):
        min = math.pow(10, 100)
        for row in range(0, len(TRAIN_LETTERS)):
            if veMatrix[row][col] != 0 and veMatrix[row][col] < min and row != len(TRAIN_LETTERS) - 1 and l[col]!=' ':
                min = veMatrix[row][col]
                l[col] = TRAIN_LETTERS[row]
    #
    #print 'VE'
    return "".join(l)

    # for col in range(len(test_letters) - 2, 0, -1):
    #     previousHighPOS = ''
    #     min = math.pow(10, 100)
    #     for currentRow in range(0, len(TRAIN_LETTERS)):
    #         for row in range(0, len(TRAIN_LETTERS)):
    #             if previousHighPOS == '':
    #                 if min > viterbiMatrix[row][col] and viterbiMatrix[row][col] != 0:
    #                     min = viterbiMatrix[row][col]
    #                     previousHighPOS = TRAIN_LETTERS[row]
    #         if trasitionsDict.has_key(TRAIN_LETTERS[currentRow] + ">" + previousHighPOS):
    #             viterbiMatrix[currentRow][col] = viterbiMatrix[currentRow][col] - math.log10(
    #                 trasitionsDict[TRAIN_LETTERS[currentRow] + ">" + previousHighPOS])
    #
    # max = math.pow(10, 101)
    # for row in range(0, len(TRAIN_LETTERS)):
    #     if max > viterbiMatrix[row][0] and viterbiMatrix[row][0] != 0:
    #         max = viterbiMatrix[row][0]
    #         l[0] = TRAIN_LETTERS[row]
    # #
    # for col in range(1, len(test_letters)):
    #     min = math.pow(10, 100)
    #     for row in range(0, len(TRAIN_LETTERS)):
    #         if viterbiMatrix[row][col] != 0 and viterbiMatrix[row][col] < min and row != len(TRAIN_LETTERS) - 1:
    #             min = viterbiMatrix[row][col]
    #             l[col] = TRAIN_LETTERS[row]
    # #
    # print 'after'
    # print "".join(l)

    rowCount = 0
    # for row in veMatrix:
    #     dummy = ''
    #     for col in row:
    #         dummy = dummy + str(col) + " "
    #     print TRAIN_LETTERS[rowCount] + " " + dummy
    #     rowCount = rowCount + 1

# Viterbi algorithm code
def hmm_map(test_letters):

    l = ['0']*len(test_letters)

    viterbiMatrix = []
    for i in range(0, len(TRAIN_LETTERS)):
        temp = []
        for j in range(0, len(test_letters)):
            temp.append([0,''])
        viterbiMatrix.append(temp)

    firstletter = compareLists_map(test_letters[0],0)
    for row in range(0,len(TRAIN_LETTERS)):
        if firstCharFeq.has_key(TRAIN_LETTERS[row]) and firstletter.has_key(TRAIN_LETTERS[row]) and firstletter[TRAIN_LETTERS[row]]!=0:
            viterbiMatrix[row][0] = [- math.log10(firstletter[TRAIN_LETTERS[row]]),'q1']

    for col in range(1,len(test_letters)):
        possibleLetter = compareLists_map(test_letters[col],0)
        #print possibleLetter
        if possibleLetter.has_key(' '):
            l[col] = " "
        #currentRow = 0
        for key in possibleLetter.keys():
            temp = {}
            for row in range(0,len(TRAIN_LETTERS)):
                if trasitionsDict.has_key(TRAIN_LETTERS[row]+">"+key) and possibleLetter.has_key(key):
                    temp[TRAIN_LETTERS[row]] = 0.1 * viterbiMatrix[row][col-1][0]- math.log10(trasitionsDict[TRAIN_LETTERS[row]+">"+key])- 10 * math.log10(possibleLetter[key])
            kjhm = 0
            Maxkey = ''
            for i in temp.keys():
                if kjhm < temp[i]:
                    kjhm = temp[i]
                    Maxkey = i
            if Maxkey != '':
                viterbiMatrix[TRAIN_LETTERS.index(key)][col] = [temp[Maxkey],Maxkey]

                    # if dictOfCharFreq.has_key(TRAIN_LETTERS[TRAIN_LETTERS.index(key)]):
            #     viterbiMatrix[TRAIN_LETTERS.index(key)][col] = [temp[Maxkey] - math.log10(dictOfCharFreq[TRAIN_LETTERS[TRAIN_LETTERS.index(key)]]),Maxkey]
            # else:
            #     viterbiMatrix[TRAIN_LETTERS.index(key)][col] = [viterbiMatrix[TRAIN_LETTERS.index(key)][col - 1],Maxkey]
            # # if temp.has_key(Maxkey):
            #     viterbiMatrix[TRAIN_LETTERS.index(key)][col] = temp[Maxkey]
            # else:
            #     if not temp.has_key(Maxkey):
            #         if dictOfCharFreq.has_key(TRAIN_LETTERS[TRAIN_LETTERS.index(key)]):
            #             viterbiMatrix[TRAIN_LETTERS.index(key)][col] = viterbiMatrix[TRAIN_LETTERS.index(key)][col-1]-math.log10(dictOfCharFreq[TRAIN_LETTERS[TRAIN_LETTERS.index(key)]])
            #         else:
            #             viterbiMatrix[TRAIN_LETTERS.index(key)][col] = viterbiMatrix[TRAIN_LETTERS.index(key)][col - 1] + 500
            #     else:
            #         if not dictOfCharFreq.has_key(TRAIN_LETTERS[TRAIN_LETTERS.index(key)]):
            #             viterbiMatrix[TRAIN_LETTERS.index(key)][col] = viterbiMatrix[TRAIN_LETTERS.index(key)][col - 1] + 500
            #         else:
            #             viterbiMatrix[TRAIN_LETTERS.index(key)][col] = viterbiMatrix[TRAIN_LETTERS.index(key)][col - 1] - math.log10(dictOfCharFreq[TRAIN_LETTERS[TRAIN_LETTERS.index(key)]])


                        #currentRow = currentRow + 1

    rowCount = 0
    # for row in viterbiMatrix:
    #     dummy = ''
    #     for col in row:
    #         dummy = dummy + str(col) + " "
    #     print TRAIN_LETTERS[rowCount] + " " + dummy
    #     rowCount = rowCount + 1

    # for col in range(len(test_letters) - 1, 0,-1):
    #     previousHighPOS = ''
    #     min = math.pow(10, 100)
    #     for row in range(0, len(TRAIN_LETTERS)):
    #         if previousHighPOS == '':
    #             if min > viterbiMatrix[row][col] and viterbiMatrix[row][col] != 0:
    #                 min = viterbiMatrix[row][col]
    #                 previousHighPOS = TRAIN_LETTERS[row]
    #     if trasitionsDict.has_key(TRAIN_LETTERS[row] + ">" + previousHighPOS):
    #         viterbiMatrix[row][col] = viterbiMatrix[row][col] - math.log10(trasitionsDict[TRAIN_LETTERS[row] + ">" + previousHighPOS])

    max = math.pow(10, 101)
    for row in range(0, len(TRAIN_LETTERS)):
        if max > viterbiMatrix[row][0][0] and viterbiMatrix[row][0][0] != 0:
            max = viterbiMatrix[row][0][0]
            l[0] = TRAIN_LETTERS[row]
    #
    for col in range(1, len(test_letters)):
        min = math.pow(10, 100)
        for row in range(0, len(TRAIN_LETTERS)):
            if viterbiMatrix[row][col][0] != 0 and viterbiMatrix[row][col][0] < min and row != len(TRAIN_LETTERS)-1 and l[col]!=' ':
                min = viterbiMatrix[row][col][0]
                l[col] = TRAIN_LETTERS[row]
    #
    #print 'before'
    #print "".join(l)
#    l = ['0']*len(test_letters)
    for col in range(1, len(test_letters)):
        min = math.pow(10, 100)
        for row in range(0, len(TRAIN_LETTERS)):
            if viterbiMatrix[row][col][0] != 0 and viterbiMatrix[row][col][0] < min and row != len(TRAIN_LETTERS) - 1 and l[col]!=' ':
                min = viterbiMatrix[row][col][0]
                l[col] = TRAIN_LETTERS[row]

    max = math.pow(10, 101)
    for row in range(0, len(TRAIN_LETTERS)):
        if max > viterbiMatrix[row][0][0] and viterbiMatrix[row][0][0] != 0:
            max = viterbiMatrix[row][0][0]
            l[0] = TRAIN_LETTERS[row]

    # for col in range(len(test_letters) - 1, 0, -1):
    #     l[col - 1] = viterbiMatrix[TRAIN_LETTERS.index(TRAIN_LETTERS[col])][col][1]

    for col in range(len(test_letters)-2,0,-1):
         previousHighPOS = ''
         min = math.pow(10, 100)
         for currentRow in range(0, len(TRAIN_LETTERS)):
             for row in range(0,len(TRAIN_LETTERS)):
                 if previousHighPOS == '':
                     if min > viterbiMatrix[row][col][0] and viterbiMatrix[row][col][0] != 0:
                         min = viterbiMatrix[row][col][0]
                         previousHighPOS = TRAIN_LETTERS[row]
             if trasitionsDict.has_key(TRAIN_LETTERS[currentRow] + ">" + previousHighPOS):
                viterbiMatrix[currentRow][col][0] = viterbiMatrix[currentRow][col][0] - math.log10(trasitionsDict[TRAIN_LETTERS[currentRow]+">"+previousHighPOS])

    #
    #
    #print 'after'
    return "".join(l)

    rowCount = 0
    # for row in viterbiMatrix:
    #     # dummy = ''
    #     # for col in row:
    #     #     dummy = dummy + str(col) + " "
    #     # print TRAIN_LETTERS[rowCount]+ " " + dummy
    #     # rowCount = rowCount + 1

TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
[dictOfCharFreq, trasitionsDict, firstCharFeq] = train()
print " Simple: " + simplified(test_letters)
print " HMM VE: " + hmm_ve(test_letters)
print "HMM MAP: " + hmm_map(test_letters)