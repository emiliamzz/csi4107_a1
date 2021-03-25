import operator
import sys
from scipy import spatial
from sent2vec.vectorizer import Vectorizer

def main(resultss, tweetss, queriess):
    """
    resultss is the file containing the returned results.
    tweetss is the file containing the documents (tweets).
    queriess is the file containing the queries.
    This script takes in a file of results and re-ranks them using a distilled version of BERT through the use of the sent2vec python library.
    It then outputs the re-ranked results file.

    Please note that this does take around an hour and a half to run.
    """
    # Open all relevant files
    results = open(resultss, encoding="utf-8").read().split("\n")
    t = open(tweetss, encoding="utf-8").read().split("\n")
    queries = open(queriess, encoding="utf-8").read().split("</top>\n\n<top>")
    f = open("Results-1.txt", "w", encoding="utf-8")
    vectorizer = Vectorizer()
    # Remove the first character from tweets bc it's weird
    t[0] = t[0][1:len(t[0])]
    # Place all the tweets in a dictionary
    tweets = {}
    for tweet in t:
        if tweet:
            tw = tweet.split("\t")
            tweets[tw[0]] = tw[1]
    for query in queries:
        # Extract the necessary info from the query
        topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
        search = query.split("<title> ")[1].split(" </title")[0]
        # Create dictionary / lists for the output
        relevantResults = {}
        queryNums = []
        queryTweets = [search]
        for r in results:
            if r:
                liner = r.split()
                # For each result for the current query, place the tweet and its id in lists
                if int(liner[0]) == topicId:
                    queryTweets.append(tweets[liner[2]])
                    queryNums.append(liner[2])
                elif int(liner[0]) > topicId:
                    break
        # Vectorize the tweets and the query
        vectorizer.bert(queryTweets)
        tweetVector = vectorizer.vectors
        # For each tweet, calculate the distance between it and the query
        for i in range(len(queryNums)):
            current = queryTweets[i+1]
            distance = spatial.distance.cosine(tweetVector[0], tweetVector[i+1])
            relevantResults[queryNums[i]] = 1 - distance
        # Sort by most relevant to least relevant
        relevantResults = dict(sorted(relevantResults.items(), key=operator.itemgetter(1), reverse=True))
        # Print the results for the current query to a text file
        count = 0
        for result in relevantResults:
            count += 1
            line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(relevantResults[result]) + " PyGER\n"
            f.write(line)
    f.close()
    

if __name__ == "__main__":
    # main("./Results.txt", "./Trec_microblog11.txt", "./topics_MB1-49.txt")
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
