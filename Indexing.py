import math
from Functions import Functions

tweets = open("Tweets.txt", encoding="utf-8").read().split('\n')
dictionary = open("Dictionary.txt", "r").read().split('\n')
functions = Functions()
indexFile = {}
for word in dictionary:
    count = 0
    line = 0
    tfDict = {}
    # calculate the tf for each word
    for tweet in tweets:
        # preprocess the tweet
        tokened = functions.preprocess(tweet)
        # calculate the length
        length = len(tokened)
        # if the word from the dictionary is in the tweet, calculate the tf and add 1 for the idf
        if word in tokened:
            tf = tokened.count(word) / float(length)
            tfDict[line] = tf
            count += 1
        line += 1
    idf = math.log2(line / count)
    indexFile[word] = [idf, tfDict]
