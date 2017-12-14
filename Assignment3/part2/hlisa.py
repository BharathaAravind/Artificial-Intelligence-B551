import re

cities = set()
bagOfWords = {}
bostonMap = {}
sanDiegoMap = {}
houstonMap = {}
philadelphiaMap = {}
orlandoMap = {}
washingtonMap = {}
atlantaMap = {}
chicagoMap = {}
torantoMap = {}
sanFransicoMap = {}
laMap = {}
nyMap = {}

def readingTweetData():
    with open('tweets.train.txt') as inputfile:
        for line in inputfile:

            list = line.split(' ')
            cities.add(list[0])
            city = list.pop(0)

            for words in list:
                words = re.sub('[^A-Za-z0-9]+', '', words)
                if words == '':
                    continue
                if words in bagOfWords:
                    bagOfWords[words.strip().lower()] = bagOfWords[words.strip().lower()] + 1
                else:
                    bagOfWords[words.strip().lower()] = 1

            if city == 'Chicago,_IL':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in chicagoMap:
                        chicagoMap[words.strip().lower()] = chicagoMap[words.strip().lower()] + 1
                    else:
                        chicagoMap[words.strip().lower()] = 1
            elif city == 'Boston,_MA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in bostonMap:
                        bostonMap[words.strip().lower()] = bostonMap[words.strip().lower()] + 1
                    else:
                        bostonMap[words.strip().lower()] = 1
            elif city == 'San_Diego,_CA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in sanDiegoMap:
                        sanDiegoMap[words.strip().lower()] = sanDiegoMap[words.strip().lower()] + 1
                    else:
                        sanDiegoMap[words.strip().lower()] = 1
            elif city == 'Houston,_TX':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in houstonMap:
                        houstonMap[words.strip().lower()] = houstonMap[words.strip().lower()] + 1
                    else:
                        houstonMap[words.strip().lower()] = 1

            elif city == 'Philadelphia,_PA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in philadelphiaMap:
                        philadelphiaMap[words.strip().lower()] = philadelphiaMap[words.strip().lower()] + 1
                    else:
                        philadelphiaMap[words.strip().lower()] = 1
            elif city == 'Orlando,_FL':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in orlandoMap:
                        orlandoMap[words.strip().lower()] = orlandoMap[words.strip().lower()] + 1
                    else:
                        orlandoMap[words.strip().lower()] = 1
            elif city == 'Washington,_DC':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in washingtonMap:
                        washingtonMap[words.strip().lower()] = washingtonMap[words.strip().lower()] + 1
                    else:
                        washingtonMap[words.strip().lower()] = 1
            elif city == 'Atlanta,_GA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in atlantaMap:
                        atlantaMap[words.strip().lower()] = atlantaMap[words.strip().lower()] + 1
                    else:
                        atlantaMap[words.strip().lower()] = 1
            elif city == 'Toronto,_Ontario':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in torantoMap:
                        torantoMap[words.strip().lower()] = torantoMap[words.strip().lower()] + 1
                    else:
                        torantoMap[words.strip().lower()] = 1
            elif city == 'San_Francisco,_CA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in sanFransicoMap:
                        sanFransicoMap[words.strip().lower()] = sanFransicoMap[words.strip().lower()] + 1
                    else:
                        sanFransicoMap[words.strip().lower()] = 1
            elif city == 'Los_Angeles,_CA':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in laMap:
                        laMap[words.strip().lower()] = laMap[words.strip().lower()] + 1
                    else:
                        laMap[words.strip().lower()] = 1
            elif city == 'Manhattan,_NY':
                for words in list:
                    words = re.sub('[^A-Za-z0-9]+', '', words)
                    if words == '':
                        continue
                    if words in nyMap:
                        nyMap[words.strip().lower()] = nyMap[words.strip().lower()] + 1
                    else:
                        nyMap[words.strip().lower()] = 1


readingTweetData()
'''
#print bagOfWords
#print chicagoMap
#print bostonMap
print houstonMap
print sanDiegoMap
print sanFransicoMap
print laMap
print torantoMap
print atlantaMap
print washingtonMap
print orlandoMap
print nyMap
print philadelphiaMap
'''
with open('boston.txt', 'w') as f:
    for key, value in sorted(bostonMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('chicago.txt', 'w') as f:
    for key, value in sorted(chicagoMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('houston.txt', 'w') as f:
    for key, value in sorted(houstonMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('sandiego.txt', 'w') as f:
    for key, value in sorted(sanDiegoMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('SanFrancis.txt', 'w') as f:
    for key, value in sorted(sanFransicoMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('la.txt', 'w') as f:
    for key, value in sorted(laMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('atlanta.txt', 'w') as f:
    for key, value in sorted(atlantaMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('wash.txt', 'w') as f:
    for key, value in sorted(washingtonMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('ny.txt', 'w') as f:
    for key, value in sorted(nyMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('toronto.txt', 'w') as f:
    for key, value in sorted(torantoMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('philly.txt', 'w') as f:
    for key, value in sorted(philadelphiaMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
with open('orlando.txt', 'w') as f:
    for key, value in sorted(orlandoMap.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        f.write('%s:%s\n' % (key, value))
