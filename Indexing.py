# Indexing:  Build an inverted index, with an entry for each word in the vocabulary. You can use any appropriate data
# structure (hash table, linked lists, Access database, etc.). An example of possible index is presented below. 

# •       Input: Tokens obtained from the preprocessing module

# •       Output: An inverted index for fast access 

# For weighting, you can use the tf-idf weighting scheme (w_ij = tf_ij x idf_i). For each query, your system will produce
# a ranked list of documents, starting with the most similar to the query and ending with the least similar. For the query
# terms, you can use a modified tf-idf weighting scheme w_iq = (0.5 + 0.5 tf_iq)∙idf_i

# Notes:
# - Inverted index: keyword -> list of docs containing it
# - What data structure do we want to use for the inverted index?
# - How will we specify the docs?
# - My suggestion for both: put the tweet into some form of structure where we can easily retrieve the tweet by using
#     its ID. We can then have another structure for each word in the dictionary that links to the IDs of the tweet
#     using the word. This inverted index will have the list of tweet IDs in ranked order.
# - To weigh it we'll use the TF-IDF ranking scheme as the assignment suggests (we should probably save the ranked score
#     as well)

#- id of the tweet will be by line number in the txt file
import math
from Functions import Functions

tweets = open("Tweets.txt", encoding="utf-8")
# open our dictionary of words
dictionary = open("Dictionary.txt", "r")
functions = Functions()
idfDict = {}
tfDict = {}
for word in dictionary:
    idfDict[word] = 0
    line = 0
    # calculate the tf for each word
    for tweet in tweets:
        # preprocess the tweet
        tokened = functions.preprocess(tweet)
        # calculate the length
        length = len(tokened)
        # if the word from the dictionary is in the tweet, calculate the tf and add 1 for the idf
        if tokened.count(word) > 0:
            tfDict[word, line] = tokened.count(word)/float(length)
            idfDict[word] += 1
        line += 1
    # calculate the idf
    idf = math.log2(line / idfDict[word])
        