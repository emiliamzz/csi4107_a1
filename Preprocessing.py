from Functions import Functions

# import file
tweets = open("Tweets.txt", encoding="utf-8").read()
functions = Functions()
dictionary = functions.preprocess(tweets)
# put the dictionary into a text file
with open('Dictionary.txt', 'w') as filehandle:
    for item in dictionary:
        filehandle.write('%s\n' % item)
