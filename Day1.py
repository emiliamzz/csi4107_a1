# Input:
# - Results.txt
# - Trec_microblog11.txt (tweets)
# - topics_MB1-49.txt (queries)

# Output:
# - Modified Results.txt (let's name it Results-1.txt?)

import operator
import sys
from sent2vec.vectorizer import Vectorizer
from scipy import spatial

def main(resultss, tweetss, queriess):
    vectorizer = Vectorizer()
    # grab query from queries file
    queries = open(queriess, encoding="utf-8").read().split("</top>\n\n<top>")
    results = open(resultss, encoding="utf-8").read().split("\n")
    t = open(tweetss, encoding="utf-8").read().split("\n")
    f = open("Results-1.txt", "w", encoding="utf-8")
    t[0] = t[0][1:len(t[0])]
    tweets = {}
    for tweet in t:
        if tweet:
            tw = tweet.split("\t")
            tweets[tw[0]] = tw[1]
    for query in queries:
        topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
        search = query.split("<title> ")[1].split(" </title")[0]
        # grab results for that query
        relevantResults = {}
        # vectorize the query
        vectorizer.bert([search])
        queryVector = vectorizer.vectors[0]
        queryNums = []
        queryTweets = []
        for r in results:
            liner = r.split()
            if int(liner[0]) == topicId:
                queryTweets.append(tweets[liner[2]])
                queryNums.append(liner[2])
            elif int(liner[0]) > topicId:
                break
        vectorizer.bert(queryTweets)
        for i in range(len(queryNums)):
            tweetVector = vectorizer.vectors
            distance = spatial.distance.cosine(queryVector, tweetVector[i])
            relevantResults[queryNums[i]] = distance
        relevantResults = dict(sorted(relevantResults.items(), key=operator.itemgetter(1), reverse=True))
        # print to results
        count = 0
        for result in relevantResults:
            count += 1
            line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(relevantResults[result]) + " PyGER\n"
            f.write(line)
    f.close()
    

if __name__ == "__main__":
    main("./Results.txt", "./Trec_microblog11.txt", "./topics_MB1-49.txt")
    #main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
