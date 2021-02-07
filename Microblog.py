import sys
from Functions import Functions

def main(i, tweets, stopWords):
    """
    i is the name of the file containing test queries
    tweets is the name of the file containing the documents
    stopWords is the name of the file containing the stop words
    This script takes in a file of test queries to run and retrieve the 1000
    most relevant documents for that each query. It then outputs the results
    in a text file with each result in the following format:
    **topic_id** Q0 **tweet_id** **rank** **cosSim** PyGER

    Each result will be separated by a new line.

    The inputted file must be a text file and it must have each query in the following format:
    <top>
    <num> Number: MB**topic_id** </num>
    <title> **query** </title>
    <querytime> **query_time** </querytime>
    <querytweettime> **query_tweet_time** </querytweettime>
    </top>

    Each query must be separated by a double new line.

    Please ensure that Indexing.py has been run before this file.
    """
    functions = Functions()
    # Import TestQueries.txt
    queries = open(i, encoding="utf-8").read().split("</top>\n\n<top>")
    # Open text file to write to
    f = open("Results.txt", "w", encoding="utf-8")
    # Loop through each test query, get the important info
    for query in queries:
        topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
        search = query.split("<title> ")[1].split(" </title")[0]
        # Retrieve the top 1000 searches for the query
        dictionary = functions.retrieve(search, tweets, stopWords)
        # Print the results to Results.txt
        count = 0
        for result in dictionary:
            count += 1
            line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(dictionary[result]) + " PyGER\n"
            f.write(line)
    f.close()

if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
