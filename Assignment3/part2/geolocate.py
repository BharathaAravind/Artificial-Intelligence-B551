# Implement a Naive Bayes classier for this problem.
# For a given tweet D, we'll need to evaluate
# P(L = l|w1,w2,...,wn), the posterior probability that a tweet was taken
# at one particular location (e.g., l = Chicago) given the words in that tweet.
# Make the Naive Bayes assumption, which says that for any i 6= j, wi is
# independent from wj given L.
#
# ---------------------------------------------------------------------------
# 1 collect all words and other tokens that occur in Examples
#     Vocabulary <-- all distinct words and other tokens in Examples
# 2 Calculate the required P(vj) and P(wk|vj) probability terms
#   For each target value vj in V do:
#       docs <-- subset of Examples for which the target value is Vj
#       P(vj) <-- Value(docs)/Value(Examples)
#       Textj <-- a single document created by concatenating all members of docsj
#       n <-- total number of words in Textj (counting duplicate words multiple times)
#       for each word Wk in Vocabulary
#               nk <-- number of times word Wk occurs in Textj
#               P(Wk|Vj) <-- (nk + 1)/(n + Value(Vocabulary))
# ---------------------------------------------------------------------------
from __future__ import division
import sys
import re
import operator

# accepts the training file and returns the list of cities with their count
def count_cities(training_file):
    list_cities = {}
    total_count = 0
    temp_city = ''
    with open(training_file) as inputFile:#opened the file
        for lines in inputFile:#read rest of the lines
            line = lines.lower().strip().split()
            try:
                if line[0] in list_cities:
                    list_cities[line[0]] = (list_cities[line[0]][0] + 1, list_cities[line[0]][1])
                    temp_city = line[0]
                else:
                    list_cities[line[0]] = (1,line[0].split(',')[0],0)
                    temp_city = line[0]
            except IndexError:
                list_cities[temp_city] = (1,line,0)

    for cities in list_cities:
        total_count += list_cities[cities][0]
    for cities in list_cities:
        list_cities[cities] = (list_cities[cities][0],list_cities[cities][1],(list_cities[cities][0]/total_count))
    return list_cities
# accepts the trainng file and returns the lists of individual list with their tweets
def count_tweets(training_file,list_cities):
    orlando = {}; orlando_count = 0
    boston = {}; boston_count = 0
    san_diego = {}; san_diego_count = 0
    philadelphia = {}; philadelphia_count = 0
    washington = {}; washington_count = 0
    toronto = {}; toronto_count = 0
    atlanta = {}; atlanta_count = 0
    san_francisco = {}; san_francisco_count = 0
    houston = {};houston_count = 0
    chicago = {};chicago_count = 0
    los_angeles = {};los_angeles_count = 0
    manhattan = {};manhattan_count = 0
    all_words = {};all_words_count = 0

    with open(training_file) as inputFile:#opened the file
        for lines in inputFile:#read rest of the lines
            line = lines.lower().strip().split()
            for word in line[1:]:
                temp = re.sub(r'[^$0-9$|^a-z|^a-z\-a-z|^0-9/0-9|^0-9:0-9|^a-z_]+',r'', word)
                if list_cities[line[0]][1] == 'orlando':
                    if temp in orlando:
                        orlando[temp] = (orlando[temp][0] + 1, word,0)# increment the counter
                    else:
                        orlando[temp] = (1,word,0)# word not present in the Chicago set# add it to the set
                elif list_cities[line[0]][1] == "boston":
                    if temp in boston:
                        boston[temp] = (boston[temp][0] + 1,word,0)
                    else:
                        boston[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "san_diego":
                    if temp in san_diego:
                        san_diego[temp] = (san_diego[temp][0] + 1,word,0)
                    else:
                        san_diego[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "philadelphia":
                    if temp in philadelphia:
                        philadelphia[temp] = (philadelphia[temp][0] + 1,word,0)
                    else:
                        philadelphia[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "washington":
                    if temp in washington:
                        washington[temp] = (washington[temp][0] + 1,word,0)
                    else:
                        washington[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "toronto":
                    if temp in toronto:
                        toronto[temp] = (toronto[temp][0] + 1,word,0)
                    else:
                        toronto[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "atlanta":
                    if temp in atlanta:
                        atlanta[temp] = (atlanta[temp][0] + 1,word,0)
                    else:
                        atlanta[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "san_francisco":
                    if temp in san_francisco:
                        san_francisco[temp] = (san_francisco[temp][0] + 1,word,0)
                    else:
                        san_francisco[temp] = (1,word,0)
                elif list_cities[line[0]][1] == "houston":
                    if temp in houston:
                        houston[temp] = (houston[temp][0] + 1,word,0)
                    else:
                        houston[temp] = (1, word,0)
                elif list_cities[line[0]][1] == "chicago":
                    if temp in chicago:
                        chicago[temp] = (chicago[temp][0] + 1,word,0)
                    else:
                        chicago[temp] = (1, word)
                elif list_cities[line[0]][1] == "los_angeles":
                    if temp in los_angeles:
                        los_angeles[temp] = (los_angeles[temp][0] + 1,word,0)
                    else:
                        los_angeles[temp] = (1, word,0)
                elif list_cities[line[0]][1] == "manhattan":
                    if temp in manhattan:
                        manhattan[temp] = (manhattan[temp][0] + 1,word,0)
                    else:
                        manhattan[temp] = (1, word,0)
                if temp in all_words:
                    all_words[temp] = (all_words[temp][0] + 1,word,0)
                else:
                    all_words[temp] = (1, word,0)
    for word in orlando:
        orlando_count += orlando[word][0]# this is n
    for word in boston:
        boston_count += boston[word][0]# this is n
    for word in san_diego:
        san_diego_count += san_diego[word][0]# this is n
    for word in philadelphia:
        philadelphia_count += philadelphia[word][0]# this is n
    for word in washington:
        washington_count += washington[word][0]# this is n
    for word in toronto:
        toronto_count += toronto[word][0]# this is n
    for word in atlanta:
        atlanta_count += atlanta[word][0]# this is n
    for word in san_francisco:
        san_francisco_count += san_francisco[word][0]# this is n
    for word in houston:
        houston_count += houston[word][0]# this is n
    for word in chicago:
        chicago_count += chicago[word][0]# this is n
    for word in los_angeles:
        los_angeles_count += los_angeles[word][0]# this is n
    for word in manhattan:
        manhattan_count += manhattan[word][0]# this is n
    total_occurence = len(all_words)   # this is vocabulary
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = orlando[word][0]
            orlando[word] = (orlando[word][0],orlando[word][1],((word_occurence + 1)/(orlando_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            orlando[word] = (0,word,((word_occurence + 1)/(orlando_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = boston[word][0]
            boston[word] = (boston[word][0],boston[word][1],((word_occurence + 1)/(boston_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            boston[word] = (0,word,((word_occurence + 1)/(boston_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = san_diego[word][0]
            san_diego[word] = (san_diego[word][0],san_diego[word][1],((word_occurence + 1)/(san_diego_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            san_diego[word] = (0,word,((word_occurence + 1)/(san_diego_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = philadelphia[word][0]
            philadelphia[word] = (philadelphia[word][0],philadelphia[word][1],((word_occurence + 1)/(philadelphia_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            philadelphia[word] = (0,word,((word_occurence + 1)/(philadelphia_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = washington[word][0]
            washington[word] = (washington[word][0],washington[word][1],((word_occurence + 1)/(washington_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            washington[word] = (0,word,((word_occurence + 1)/(washington_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = toronto[word][0]
            toronto[word] = (toronto[word][0],toronto[word][1],((word_occurence + 1)/(toronto_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            toronto[word] = (0,word,((word_occurence + 1)/(toronto_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = atlanta[word][0]
            atlanta[word] = (atlanta[word][0],atlanta[word][1],((word_occurence + 1)/(atlanta_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            atlanta[word] = (0,word,((word_occurence + 1)/(atlanta_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = san_francisco[word][0]
            san_francisco[word] = (san_francisco[word][0],san_francisco[word][1],((word_occurence + 1)/(san_francisco_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            san_francisco[word] = (0,word,((word_occurence + 1)/(san_francisco_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = houston[word][0]
            houston[word] = (houston[word][0],houston[word][1],((word_occurence + 1)/(houston_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            houston[word] = (0,word,((word_occurence + 1)/(houston_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = chicago[word][0]
            chicago[word] = (chicago[word][0],chicago[word][1],((word_occurence + 1)/(chicago_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            chicago[word] = (0,word,((word_occurence + 1)/(chicago_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = los_angeles[word][0]
            los_angeles[word] = (los_angeles[word][0],los_angeles[word][1],((word_occurence + 1)/(los_angeles_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            los_angeles[word] = (0,word,((word_occurence + 1)/(los_angeles_count + total_occurence)))
    for word in all_words:
        word_occurence = 0
        try:
            word_occurence = manhattan[word][0]
            manhattan[word] = (manhattan[word][0],manhattan[word][1],((word_occurence + 1)/(manhattan_count + total_occurence)))
        except KeyError:
            word_occurence = 0
            manhattan[word] = (0,word,((word_occurence + 1)/(manhattan_count + total_occurence)))
    return orlando,boston,san_diego,philadelphia,washington,toronto,atlanta,san_francisco,houston,chicago,los_angeles,manhattan,all_words

def estimate_tweets(testing_file,orlando,boston,san_diego,philadelphia,washington,toronto,atlanta,san_francisco,houston,chicago,los_angeles,manhattan,all_words,list_cities):
    output = {}
    counter = 0
    analyzed_tweets = {}
    values = {}
    temp_value = 0
    temp_value_orlando = 1; temp_value_boston = 1
    temp_value_san_diego = 1; temp_value_philadelphia = 1
    temp_value_washington = 1; temp_value_toronto = 1
    temp_value_atlanta = 1; temp_value_san_francisco = 1
    temp_value_houston = 1; temp_value_chicago = 1
    temp_value_los_angeles = 1; temp_value_manhattan = 1
    pattern = re.compile('^[a-zA-Z]+$')
    #temp_city = ''
    with open(testing_file) as inputFile:#opened the file
        for lines in inputFile:#read rest of the lines

            temp_value_orlando = 1; temp_value_boston = 1
            temp_value_san_diego = 1; temp_value_philadelphia = 1
            temp_value_washington = 1; temp_value_toronto = 1
            temp_value_atlanta = 1; temp_value_san_francisco = 1
            temp_value_houston = 1; temp_value_chicago = 1
            temp_value_los_angeles = 1; temp_value_manhattan = 1
            line = lines.lower().strip().split()
            #print line[0]
            try:
                if line[0] in list_cities:
                    #print list_cities
                    #temp_city = line[0]
                    pass
                else:
                    #line.append(line[0])
                    #pass
                    continue
            except IndexError:
                continue

            temp_value = (0,"none")
            estimated_value = (0,"none")
            for word in line[1:]:
                temp = re.sub(r'[^$0-9$|^a-z|^a-z\-a-z|^0-9/0-9|^0-9:0-9|^a-z_]+',r'', word)
                # calculate the weight for each word and then guess the city.
                # for each word in the tweet, calc the probability

                # guess that the tweet is from orlando
                if(len(temp) > 1 and temp not in ("","and","the","but","if","as","he","she","his","our","at","amp","of","you","ave","job","to","in","st","dr","rd","for","our","im","my","be","it","job:","here:","we","about","me","by","you:")):
                    #if(temp == "the" or temp == "and" or)
                    pass
                else:
                    continue
                try:
                    temp_value_orlando = temp_value_orlando * (orlando[temp][2])
                except KeyError:
                    temp_value_orlando = temp_value_orlando * 1
                    pass
                try:
                    temp_value_boston = temp_value_boston * (boston[temp][2])
                except KeyError:
                    temp_value_boston = temp_value_boston * 1
                    pass
                try:
                    temp_value_san_diego = temp_value_san_diego * (san_diego[temp][2])
                except KeyError:
                    temp_value_san_diego = temp_value_san_diego * 1
                    pass
                try:
                    temp_value_philadelphia = temp_value_philadelphia * (philadelphia[temp][2])
                except KeyError:
                    temp_value_philadelphia = temp_value_philadelphia * 1
                    pass
                try:
                    temp_value_washington = temp_value_washington * (washington[temp][2])
                except KeyError:
                    temp_value_washington = temp_value_washington * 1
                    pass
                try:
                    temp_value_toronto = temp_value_toronto * (toronto[temp][2])
                except KeyError:
                    temp_value_toronto = temp_value_toronto * 1
                    pass
                try:
                    temp_value_atlanta = temp_value_atlanta * (atlanta[temp][2])
                except KeyError:
                    temp_value_atlanta = temp_value_atlanta * 1
                    pass
                try:
                    temp_value_san_francisco = temp_value_san_francisco * (san_francisco[temp][2])
                except KeyError:
                    temp_value_san_francisco = temp_value_san_francisco * 1
                    pass
                try:
                    temp_value_houston = temp_value_houston * (houston[temp][2])
                except KeyError:
                    temp_value_houston = temp_value_houston * 1
                    pass
                try:
                    temp_value_chicago = temp_value_chicago * (chicago[temp][2])
                except KeyError:
                    temp_value_chicago = temp_value_chicago * 1
                    pass
                try:
                    temp_value_los_angeles = temp_value_los_angeles * (los_angeles[temp][2])
                except KeyError:
                    temp_value_los_angeles = temp_value_los_angeles * 1
                    pass
                try:
                    temp_value_manhattan = temp_value_manhattan * (manhattan[temp][2])
                except KeyError:
                    temp_value_manhattan = temp_value_manhattan * 1
                    pass
                # print temp
                # print "temp_value_orlando",temp_value_orlando
                # print "temp_value_boston",temp_value_boston
                # print "temp_value_san_diego",temp_value_san_diego
                # print "temp_value_philadelphia",temp_value_philadelphia
                # print "temp_value_washington",temp_value_washington
                # print "temp_value_toronto",temp_value_toronto
                # print "temp_value_atlanta",temp_value_atlanta
                # print "temp_value_san_francisco",temp_value_san_francisco
                # print "temp_value_houston",temp_value_houston
                # print "temp_value_chicago",temp_value_chicago
                # print "temp_value_los_angeles",temp_value_los_angeles
                # print "temp_value_manhattan",temp_value_manhattan
                # print "---------------------"
            #if its from orlondo
            for city in ("orlando,_fl","boston,_ma","san_diego,_ca","philadelphia,_pa","washington,_dc","toronto,_ontario","atlanta,_ga","san_francisco,_ca","houston,_tx","chicago,_il","los_angeles,_ca","manhattan,_ny"):
                if(city == "orlando,_fl"):
                    temp_value = ((list_cities[city][2])*(temp_value_orlando),city)
                elif(city == "boston,_ma"):
                    temp_value = ((list_cities[city][2])*(temp_value_boston),city)
                elif(city == "san_diego,_ca"):
                    temp_value = ((list_cities[city][2])*(temp_value_san_diego),city)
                elif(city == "philadelphia,_pa"):
                    temp_value = ((list_cities[city][2])*(temp_value_philadelphia),city)
                elif(city == "washington,_dc"):
                    temp_value = ((list_cities[city][2])*(temp_value_washington),city)
                    #print ((list_cities[city][2])*(temp_value_washington),city)
                elif(city == "toronto,_ontario"):
                    temp_value = ((list_cities[city][2])*(temp_value_toronto),city)
                elif(city == "atlanta,_ga"):
                    temp_value = ((list_cities[city][2])*(temp_value_atlanta),city)
                elif(city == "san_francisco,_ca"):
                    temp_value = ((list_cities[city][2])*(temp_value_san_francisco),city)
                elif(city == "houston,_tx"):
                    temp_value = ((list_cities[city][2])*(temp_value_houston),city)
                elif(city == "chicago,_il"):
                    temp_value = ((list_cities[city][2])*(temp_value_chicago),city)
                elif(city == "los_angeles,_ca"):
                    temp_value = ((list_cities[city][2])*(temp_value_los_angeles),city)
                elif(city == "manhattan,_ny"):
                    temp_value = ((list_cities[city][2])*(temp_value_manhattan),city)
                if(temp_value[0] > estimated_value[0]):
                    estimated_value = temp_value
                    # print "temp_value",temp_value
                    # print "estimated_value",estimated_value
            parts = estimated_value[1].split(',')
            ending = parts[1].upper()
            starting = '_'.join(word[0].upper() + word[1:] for word in parts[0].split('_'))
            # start = ''
            # for i in range(len(starting)):
            #     start = ''.join(word[0].upper() + word[1:] for word in starting[i].split())
            output[counter] = (starting +','+ ending,lines)
            counter += 1
    return output

if __name__ == '__main__':
    # to accept training-file testing-file output-file
    training_file = sys.argv[1]
    testing_file = sys.argv[2]
    output_file = sys.argv[3]

    # Reading the input files
    line = []
    city = ''
    tweet = []
    orlando = {}
    boston = {}
    san_diego = {}
    philadelphia = {}
    washington = {}
    toronto = {}
    atlanta = {}
    san_francisco = {}
    houston = {}
    chicago = {}
    los_angeles = {}
    manhattan = {}
    all_words = {}
    list_cities = {}
    analyzed_tweets = {}
    # accepts the training file and returns the list of cities with their count
    list_cities = count_cities(training_file)
    # accepts the trainng file and returns the lists of individual list with their tweets and probabilities
    orlando,boston,san_diego,philadelphia,washington,toronto,atlanta,san_francisco,houston,chicago,los_angeles,manhattan,all_words = count_tweets(training_file,list_cities)

    file = open("orlando.txt", 'w')
    for key, value in sorted(orlando.iteritems(), key=lambda (k,v): (v,k)):
        file.write("\n")
        file.write("%s: %s" % (key, value))
    file.close()
    # call the testing file and check its probabilities and output it to a file
    #       -- accepts the all the sets as an input
    analyzed_tweets = estimate_tweets(testing_file,orlando,boston,san_diego,philadelphia,washington,toronto,atlanta,san_francisco,houston,chicago,los_angeles,manhattan,all_words,list_cities)


    #calculate probabilities of each city
    #list_cities = probability_cities(training_file)

    #----- writing into the file.----
    file = open(output_file, 'w')
    for key in analyzed_tweets:
        #file.write("\n")
        file.write(analyzed_tweets[key][0]+" "+analyzed_tweets[key][1])
    file.close()
    total_count = 0
    correctness_count = 0
    with open(output_file) as inputFile:#opened the file
        for lines in inputFile:
            parts = lines.lower().strip().split()
            total_count += 1
            if(parts[0] == parts[1]):
                correctness_count += 1
            # else:
            #     print parts[0],parts[1],' '.join(word[0].upper() + word[1:] for word in parts[2:])
    file = open("orlando.txt", 'w')
    for key, value in sorted(orlando.iteritems(), key=lambda (k,v): (v,k)):
        file.write("\n")
        file.write("%s: %s" % (key, value))
    file.close()

    print '*'*50
    orlando =  sorted(orlando.items(), key=operator.itemgetter(1), reverse=True)
    print 'orlando'
    count = 0
    for l in orlando[0:6]:
        if l[0] !='' and count<5:
            print l[0]
            count = count+1

    print '*' * 50
    chicago =  sorted(chicago.items(), key=operator.itemgetter(1), reverse=True)
    print 'chicago'
    count = 0
    for l in chicago[0:6]:
        if l[0] != '' and count<5:
            print l[0]
            count = count+1

    print '*' * 50
    manhattan = sorted(manhattan.items(), key=operator.itemgetter(1), reverse=True)
    print 'manhattan'
    count = 0
    for l in manhattan[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1

    print '*' * 50
    los_angeles = sorted(los_angeles.items(), key=operator.itemgetter(1), reverse=True)
    print 'los_angeles'
    count = 0
    for l in los_angeles[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1

    print '*' * 50
    houston = sorted(houston.items(), key=operator.itemgetter(1), reverse=True)
    print 'houston'
    count = 0
    for l in houston[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1

    print '*' * 50
    san_francisco = sorted(san_francisco.items(), key=operator.itemgetter(1), reverse=True)
    print 'san_francisco'
    count = 0
    for l in san_francisco[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    atlanta = sorted(atlanta.items(), key=operator.itemgetter(1), reverse=True)
    print 'atlanta'
    count = 0
    for l in atlanta[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    toronto = sorted(toronto.items(), key=operator.itemgetter(1), reverse=True)
    print 'toronto'
    count = 0
    for l in toronto[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    washington = sorted(washington.items(), key=operator.itemgetter(1), reverse=True)
    print 'washington'
    count = 0
    for l in washington[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    philadelphia = sorted(philadelphia.items(), key=operator.itemgetter(1), reverse=True)
    print 'philadelphia'
    count = 0
    for l in philadelphia[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    boston = sorted(boston.items(), key=operator.itemgetter(1), reverse=True)
    print 'boston'
    count = 0
    for l in boston[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
    print '*' * 50
    san_diego = sorted(san_diego.items(), key=operator.itemgetter(1), reverse=True)
    print 'boston'
    count = 0
    for l in san_diego[0:6]:
        if l[0] != '' and count < 5:
            print l[0]
            count = count + 1
