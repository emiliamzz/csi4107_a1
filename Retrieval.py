import math
import operator
import pickle
from Functions import Functions

cosDict = {}
documents = []
functions = Functions()
queryDict = {}
tweets = open("Tweets.txt", encoding="utf-8").read().split('\n')
# Open index from pickle file
f = open("Index.p", "rb")
index = pickle.load(f)
f.close()
# Get user input
query = input("Enter query: ")
# Preprocess the query
preproQ = functions.preprocess(query)
length = len(preproQ)
# Calculate the query weight
for word in preproQ:
    # Check if word is in index
    if word in index:
        tf = preproQ.count(word) / float(length)
        idf = index[word][0]
        w = (0.5 + 0.5 * tf) * idf
        queryDict[word] = w
        documents += index[word][1].keys()
    else:
        # Remove the word from the query
        preproQ.remove(word)
# Quit on an invalid query
if len(preproQ) == 0:
    print("No results match your search")
    exit()
# Remove duplicate document IDs
documents = list(dict.fromkeys(documents))
# Rank the similarity using cosine method
bqw = 0
for value in queryDict.values():
    bqw += pow(value, 2)
for document in documents:
    top = 0
    for word in preproQ:
        if document in index[word][1]:
            top += queryDict[word] * index[word][0] * index[word][1][document]
    tweet = functions.preprocess(tweets[int(document)-1])
    bdw = 0
    for word in tweet:
        bdw += pow(index[word][0] * index[word][1][document], 2)
    bottom = math.sqrt(bdw * bqw)
    cos = top / bottom
    cosDict[document] = cos
# Sort by similarity
cosDict = dict(sorted(cosDict.items(), key=operator.itemgetter(1), reverse=True))
# Print out the top 1000 documents into a text file
f = open("Output.txt", "w", encoding="utf-8")
count = 0
for item in cosDict:
    if count == 1000:
        break
    tweet = tweets[int(item)-1]
    f.write(tweet + "\n")
    count += 1
f.close()
