import re
import string
import unidecode
from Stemmer import PorterStemmer

class Functions:

    # s is the string to preprocess
    # This function takes in a string and returns an array of words that have been preprocessed
    def preprocess(self, s):
        # remove links
        s = re.sub(r'https?:\/\/.\S*', '', s, flags=re.MULTILINE)
        s = re.sub(r'www.\S*', '', s, flags=re.MULTILINE)
        s = re.sub(r'\S*.html', '', s, flags=re.MULTILINE)
        # switch to roman alphabet
        s = unidecode.unidecode(s)
        # remove punctuation, digits
        s = s.translate(str.maketrans('', '', string.punctuation))
        s = s.translate(str.maketrans('', '', string.digits))
        # make everything lowercase
        s = s.lower()
        # split into array
        dictionary = s.split()
        # stem using the porter stemmer
        porter = PorterStemmer()
        dictionary = [porter.stem(word, 0, len(word)-1) for word in dictionary]
        # remove stop words
        dictionary = list(dict.fromkeys(dictionary))
        stop = open("StopWords.txt").read().split()
        # remove duplicates
        dictionary = list(set(dictionary)-set(stop))
        return dictionary
