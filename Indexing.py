import math
import pickle
from Functions import Functions

dictionary = []
functions = Functions()
index = {}
lineCount = 0
tweets = open("Tweets.txt", encoding="utf-8").read().split('\n')
wordCount = {}

for tweet in tweets:
    lineCount += 1
    # preprocess the tweet
    tokened = functions.preprocess(tweet)
    # create another array of the tweet removing all duplicates
    noDup = list(dict.fromkeys(tokened))
    # calculate the length of the tweet
    length = len(tokened)
    for word in noDup:
        # calculate the tf and store it
        tf = tokened.count(word) / float(length)
        # put it into the dictionary without overlap
        if word not in dictionary:
            dictionary.append(word)
            index[word] = [None, {}]
            wordCount[word] = 0
        index[word][1][str(lineCount)] = tf
        # add 1 to the number of tweets that uses this word
        wordCount[word] += 1
# put in alphabetical order
dictionary = sorted(dictionary)
# put the dictionary into a text file
with open('Dictionary.txt', 'w') as filehandle:
    for item in dictionary:
        filehandle.write('%s\n' % item)
# calculate the idf
for word in dictionary:
    idf = math.log2(lineCount / wordCount[word])
    index[word][0] = idf
#save to pickle file
f = open("Index.p", "wb")
pickle.dump(index, f)
f.close()
