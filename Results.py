from Functions import Functions

functions = Functions()
# Import TestQueries.txt
queries = open("TestQueries.txt", encoding="utf-8").read().split("</top>\n\n<top>")
# Open text file to write to
f = open("Results.txt", "w", encoding="utf-8")
# Loop through each test query, get the important info
# This includes the topic_id (between <num>) and the query (between <title>)
for query in queries:
    topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
    search = query.split("<title> ")[1].split(" </title")[0]
# When each query runs through the retrieval, we should only be inputting the query
# The output should be a dictionary (sorted by value) with the key as the tweet ID
# (not our personal IDs that we gave it but the actual tweet ID) and its cosSim score
# (to three decimal points)
    dictionary = functions.retrieve(search)
# We then print it into Results.txt in the following format:
# topic_id Q0 tweet_id rank score tag
    count = 0
    for result in dictionary:
        count += 1
        line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(dictionary[result]) + " PyGER\n"
        f.write(line)
f.close()
