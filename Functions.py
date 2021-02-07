import math
import operator
import pickle
import re
import string
import unidecode
from Stemmer import PorterStemmer

class Functions:

    # s is the string to preprocess
    # This function takes in a string and returns an array of words that have been preprocessed
    def preprocess(self, s):
        # remove links
        s = re.sub(r'https?:\/\/.\S*', '', s, flags=re.MULTILINE)
        s = re.sub(r'www.\S*', '', s, flags=re.MULTILINE)
        s = re.sub(r'\S*.html', '', s, flags=re.MULTILINE)
        # switch to roman alphabet
        s = unidecode.unidecode(s)
        # remove punctuation, digits
        s = s.translate(str.maketrans('', '', string.punctuation))
        s = s.translate(str.maketrans('', '', string.digits))
        # make everything lowercase
        s = s.lower()
        # split into array
        dictionary = s.split()
        # stem using the porter stemmer
        porter = PorterStemmer()
        dictionary = [porter.stem(word, 0, len(word)-1) for word in dictionary]
        # remove stop words
        stop = open("StopWords.txt").read().split()
        dictionary = list(set(dictionary)-set(stop))
        return dictionary

    # query is a string
    # This function takes in a query as an input and returns an array of the top 1000 documents for it
    def retrieve(self, query):
        cosDict = {}
        documents = []
        queryDict = {}
        tweets = open("Tweets.txt", encoding="utf-8").read().split('\n')
        # Remove the first character because it's weird
        tweets[0] = tweets[0][1:len(tweets[0])]
        # Open index from pickle file
        f = open("Index.p", "rb")
        index = pickle.load(f)
        f.close()
        # Preprocess the query
        preproQ = self.preprocess(query)
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
            tweet = self.preprocess(tweets[int(document)-1])
            bdw = 0
            for word in tweet:
                bdw += pow(index[word][0] * index[word][1][document], 2)
            bottom = math.sqrt(bdw * bqw)
            cos = top / bottom
            cosDict[document] = cos
        # Sort by similarity
        cosDict = dict(sorted(cosDict.items(), key=operator.itemgetter(1), reverse=True))
        # Create a dictionary with the tweet ID and the cosSim to three decimal places
        output = {}
        count = 0
        for item in cosDict:
            if count == 1000:
                break
            tweetId = tweets[int(item)-1].split("\t")[0]
            cosSim = float("%0.3f" % (cosDict[item]))
            output[tweetId] = cosSim
            count += 1
        return output
