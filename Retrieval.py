import math
import operator
import pickle
from Functions import Functions

# Can we somehow save the inverted index to a text file so that we don't have to constantly go through the above?

# For each query, your system will produce a ranked list of documents, starting with the most similar to the
# query and ending with the least similar. For the query terms, you can use a modified tf-idf weighting scheme
# w_iq = (0.5 + 0.5 tf_iq)∙idf_i
# Retrieval and Ranking:  Use the inverted index (from step 2) to find the limited set of documents that
# contain at least one of the query words. Compute the similarity scores between a query and each document
# (using cosine or other method). 

 

# •       Input: One query and the Inverted Index (from Step2)

# •       Output: Similarity values between the query and each of the documents.
#                 Rank the documents in decreasing order of similarity scores.



tweets = open("Tweets.txt", encoding="utf-8").read().split('\n')
functions = Functions()
# Open index from pickle file
f = open("Index.p", "rb")
index = pickle.load(f)
f.close()
# Get user input
query = input("Enter query: ")
# Calculate query weight
# w_iq = (0.5 + 0.5 tf_iq)∙idf_i
# tf = wordCount / totalWords
# idf = index[word][0]
preproQ = functions.preprocess(query)
length = len(preproQ)
queryDict = {}
documents = []
for word in preproQ:
    # check if word is in index
    if word in index:
        tf = preproQ.count(word) / float(length)
        idf = index[word][0]
        w = (0.5 + 0.5 * tf) * idf
        queryDict[word] = w
        documents += index[word][1].keys()
    else:
        preproQ.remove(word)
if len(preproQ) == 0:
    print("No results match your search")
    exit()
documents = list(dict.fromkeys(documents))
cosDict = {}
# Rank the similarity using cosine method
# CosSim(d_j, q) = sum(w_ij * w_iq) / sqrt(sum((w_ij)^2) * bqw)
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
f = open("Output.txt", "w")
count = 0
for item in cosDict:
    if count == 1000:
        break
    tweet = tweets[int(item)-1].decode(encoding="UTF-8")
    f.write(tweet + "\n")
    count += 1
f.close()
