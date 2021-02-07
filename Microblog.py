from Functions import Functions

functions = Functions()
# Import TestQueries.txt
queries = open("TestQueries.txt", encoding="utf-8").read().split("</top>\n\n<top>")
# Open text file to write to
f = open("Results.txt", "w", encoding="utf-8")
# Loop through each test query, get the important info
for query in queries:
    topicId = int(query.split("<num> Number: MB")[1].split(" </num>")[0])
    search = query.split("<title> ")[1].split(" </title")[0]
    # Retrieve the top 1000 searches for the query
    dictionary = functions.retrieve(search)
    # Print the results to Results.txt
    count = 0
    for result in dictionary:
        count += 1
        line = str(topicId) + " Q0 " + result + " " + str(count) + " " + str(dictionary[result]) + " PyGER\n"
        f.write(line)
f.close()
