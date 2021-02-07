import math
import pickle
import sys
from Functions import Functions

def main(i, stopWords):
    """
    i is the name of the file containing the documents (tweets)
    stopWords is the name of the file containing the list of stop words
    This script takes in a file of documents and creates a dictionary
    and an inverted index from the words in the documents.
    It then outputs the inverted index as a pickle file.

    The inputted file of documents must be a text file and must have each tweet in the following format:
    **tweet_id**    **tweet**

    Each document must be separated by a new line.

    The inputted file of stop words must be a text file and
    each stop word must be separated by a new line.
    """
    dictionary = []
    functions = Functions()
    index = {}
    lineCount = 0
    tweets = open(i, encoding="utf-8").read().split('\n')
    wordCount = {}

    for tweet in tweets:
        lineCount += 1
        # preprocess the tweet
        tokened = functions.preprocess(tweet, stopWords)
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

    # NOTE: uncomment the following to print the dictionary in alphabetical order to a txt file called Dictionary.txt
    # dictionary = sorted(dictionary)
    # with open('Dictionary.txt', 'w') as filehandle:
    #     for item in dictionary:
    #         filehandle.write('%s\n' % item)

    # calculate the idf
    for word in dictionary:
        idf = math.log2(lineCount / wordCount[word])
        index[word][0] = idf
    #save to pickle file
    f = open("Index.p", "wb")
    pickle.dump(index, f)
    f.close()

if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]))
