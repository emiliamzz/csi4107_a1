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

    The inputted file of results must be a text file and must have each result in the following format:
    **topic_id** Q0 **tweet_id** **rank** **cosSim** PyGER

    Each result must be separated by a new line.

    The inputted file of documents must be a text file and must have each tweet in the following format:
    **tweet_id**    **tweet**

    Each document must be separated by a new line.

    The inputted file of queries must be a text file and it must have each query in the following format:
    <top>
    <num> Number: MB**topic_id** </num>
    <title> **query** </title>
    <querytime> **query_time** </querytime>
    <querytweettime> **query_tweet_time** </querytweettime>
    </top>

    Each query must be separated by a double new line.

    Please note that this does take around an hour and a half to run.
    """
    # Open all relevant files
    results = open(resultss, encoding="utf-8").read().split("\n")
    t = open(tweetss, encoding="utf-8").read().split("\n")
    queries = open(queriess, encoding="utf-8").read().split("</top>\n\n<top>")
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
        # Vectorize the query
        vectorizer.bert([search])
        queryVector = vectorizer.vectors[0]
        # Create dictionary / lists for the output
        relevantResults = {}
        queryNums = []
        queryTweets = []
        for r in results:
            liner = r.split()
            # For each result for the current query, place the tweet and its id in lists
            if int(liner[0]) == topicId:
                queryTweets.append(tweets[liner[2]])
                queryNums.append(liner[2])
                results.pop(r)
            elif int(liner[0]) > topicId:
                break
        # Vectorize the tweets
        vectorizer.bert(queryTweets)
        tweetVector = vectorizer.vectors
        # For each tweet, calculate the distance between it and the query
        for i in range(len(queryNums)):
            distance = spatial.distance.cosine(queryVector, tweetVector[i])
            relevantResults[queryNums[i]] = distance
        # Sort by most relevant to least relevant
        relevantResults = dict(sorted(relevantResults.items(), key=operator.itemgetter(1), reverse=True))
        # Print the results for the current query to a text file
        f = open("Results-1.txt", "w", encoding="utf-8")
        count = 0
        for result in relevantResults:
            count += 1
            line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(relevantResults[result]) + " PyGER\n"
            f.write(line)
    f.close()
    

if __name__ == "__main__":
    # main("./Results.txt", "./Trec_microblog11.txt", "./topics_MB1-49.txt")
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
