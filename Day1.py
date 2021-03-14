# Input:
# - Results.txt
# - Trec_microblog11.txt (tweets)
# - topics_MB1-49.txt (queries)

# Output:
# - Modified Results.txt (let's name it Results-1.txt?)

from sent2vec.vectorizer import Vectorizer
from scipy import spatial

def main(resultss, tweetss, queriess):
    vectorizer = Vectorizer()
    # grab query from queries file
    queries = open(queriess, encoding="utf-8").read().split("</top>\n\n<top>")
    results = open(resultss, encoding="utf-8").read().split("\n")
    t = open(tweetss, encoding="utf-8").read().split("\n")
    tweets = {}
    for tweet in t:
        tw = split("/t")
        tweets[tw[0]] = tw[1]
    for query in queries:
        topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
        search = query.split("<title> ")[1].split(" </title")[0]
        # grab results for that query
        relevantResults = {}
        relevantTweets = []
        relevantIds = []
        for r in results:
            liner = r.split()
            if int(liner[0]) == topicId:
                relevantResults[liner[2]] = None # None is going to be replaced by similarity score
                relevantTweets.append(tweets[liner2])
                relevantIds.append(liner[2])
        # vectorize the query
        queryVector = vectorizer.bert([search])
        # vectorize the relevant tweets
        tweetsVector = vectorizer.bert(relevantTweets)
        # calculate the distance between each tweet and the query
        for tweet in tweetsVector:
            distance = spatial.distance.cosine(queryVector[0], tweet)
            index = tweetsVector.index(tweet)
            relevantResults[relevantIds[index]] = distance
    # return

if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
