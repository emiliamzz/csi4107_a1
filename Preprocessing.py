import re
import string
import unidecode
from Stemmer import PorterStemmer

# import file
filet = open("tweets.txt", encoding="utf-8")
tweets = filet.read()
filet.close()
# remove links
tweets = re.sub(r'https?:\/\/.\S*', '', tweets, flags=re.MULTILINE)
tweets = re.sub(r'www.\S*', '', tweets, flags=re.MULTILINE)
tweets = re.sub(r'\S*.html', '', tweets, flags=re.MULTILINE)
# switch to roman alphabet
tweets = unidecode.unidecode(tweets)
# remove punctuation, digits
tweets = tweets.translate(str.maketrans('', '', string.punctuation))
tweets = tweets.translate(str.maketrans('', '', string.digits))
# make everything lowercase
tweets = tweets.lower()
# split into array
dictionary = tweets.split()
# stem
porter = PorterStemmer()
dictionary = [porter.stem(word, 0, len(word)-1) for word in dictionary]
# remove stop words and duplicates from the stemmed array
dictionary = list(dict.fromkeys(dictionary))
stop = open("StopWords.txt").read().split()
dictionary = list(set(dictionary)-set(stop))
# put the dictionary into a text file
with open('dictionary.txt', 'w') as filehandle:
    for item in dictionary:
        filehandle.write('%s\n' % item)
        