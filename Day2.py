import gensim
import itertools
import operator
import string
import sys
import unidecode
from rank_bm25 import BM25Okapi
from Stemmer import PorterStemmer

def process(s, stopWords):
    """
    s is a string.
    stopWords is a list where each string is a word.
    This function takes in a string and processes it, returning it as a list.
    """
    # Switch to roman alphabet
    s = unidecode.unidecode(s)
    # Remove punctuation
    s = s.translate(str.maketrans('', '', string.punctuation))
    # Make everything lowercase
    s = s.lower()
    # Split into a list
    words = s.split()
    # Remove stop words
    words = list(set(words)-set(stopWords))
    return words

def retrieve(query, processedTweets, tweets):
    """
    query is a list where each string is a word in the query.
    processedTweets is a list of lists where each list is a tweet and each string is a word in that tweet.
    tweets is a list where each string is a tweet.
    This function uses BM25 to rank how similar a tweet is to the query and returns the top 1000 results.
    """
    # Calculate the similarity scores using BM25
    bm25 = BM25Okapi(processedTweets)
    scores = bm25.get_scores(query)
    # Put the results in a dictionary
    result = {}
    for i in range(len(scores)):
        score = scores[i]
        if score > 0:
            id = tweets[i].split("\t")[0]
            result[id] = score
    # Sort by most to least relevant
    result = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    # Keep only the 1000 most relevant results
    result = dict(itertools.islice(result.items(), 1000))
    return result

def main(queriess, stopWords, binary, i):
    """
    queriess is the file containing the queries.
    stopWords is the file containing the stop words.
    binary is the file for the binary model.
    i is the file containing the documents (tweets).
    This script takes in a file of queries and expands it by adding synonyms for each word in the query.
    It then outputs the top 1000 results for each query.
    """
    # Open the model and the relevant files
    queries = open(queriess, encoding="utf-8").read().split("</top>\n\n<top>")
    stop = open(stopWords).read().split()
    model = gensim.models.KeyedVectors.load_word2vec_format(binary, binary=True)
    tweets = open(i, encoding="utf-8").read().split('\n')
    f = open("Results-2.txt", "w", encoding="utf-8")
    porter = PorterStemmer()
    # Remove the first character because it's weird
    tweets[0] = tweets[0][1:len(tweets[0])]
    # Process the tweets and create a list of lists
    processedTweets = []
    for tweet in tweets:
        if tweet:
            t = tweet.split("\t")[1]
            t = process(t, stop)
            t = [porter.stem(word, 0, len(word)-1) for word in t]
            processedTweets.append(t)
    for query in queries:
        # Get the topicId and the query
        topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
        search = query.split("<title> ")[1].split(" </title")[0]
        # Format the query
        words = process(search, stop)
        # Expand the query
        expandedQuery = []
        for word in words:
            if word not in expandedQuery:
                expandedQuery.append(word)
                try:
                    synonyms = model.most_similar([word], [], topn=3)
                    for synonym in synonyms:
                        if synonym not in expandedQuery:
                            expandedQuery.append(synonym[0])
                # Ignore errors if the model doesn't recognize the word
                except KeyError:
                    pass
        # Stem the words and remove duplicates
        expandedQuery = [porter.stem(word, 0, len(word)-1) for word in expandedQuery]
        expandedQuery = list(dict.fromkeys(expandedQuery))
        # Retrieve the 1000 relevant documents for the query
        dictionary = retrieve(expandedQuery, processedTweets, tweets)
        # Print to the file
        count = 0
        for result in dictionary:
            count += 1
            line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(dictionary[result]) + " PyGER\n"
            f.write(line)
    f.close()

if __name__ == "__main__":
    # main("./topics_MB1-49.txt", "./StopWords", "./GoogleNews-vectors-negative300.bin", "./Trec_microblog11.txt")
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
