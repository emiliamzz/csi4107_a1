Student names:

Emilia Zielinska || 300018129
Gabrielle Naubert || 300015305
Robert Zhang || 300077171

----------------------------------------------------------------------------------------------------

How tasks were divided:

For this assignment, we met up online every Tuesday to edit the code together using Visual Studio
Code Live Share. Using this, it allowed us to work on coding simultaneously and work on the tasks
together. This is a system called pairing. The benefits of pairing are that it is clear to everyone
what has been done thus far and that we are forced to think critically by voicing our thoughts out
loud, allowing for better optimization of code and fewer errors.

----------------------------------------------------------------------------------------------------

Instructions to run the program:

Please ensure you have the latest version of Python installed. In your terminal:
- run `pip3 install unidecode`
- run `python3 Indexing.py <tweets> <stopWords>`
  where <tweets> is the file containing all of the documents and
  <stopWords> is the file containing all of the stop words
  Example: `python3 Indexing.py .\Trec_microblog11.txt .\StopWords`
- run `python3 Microblog.py <testQueries> <tweets> <stopWords>`
  where <testQueries> is the file containing the test queries,
  <tweets> is the file containing all of the documents, and
  <stopWords> is the file containing all of the stop words
  Example: `python3 Microblog.py .\topics_MB1-49.txt .\Trec_microblog11.txt .\StopWords`

----------------------------------------------------------------------------------------------------

Program funtionality:

Files -> Functions.py ; Indexing.py ; Microblog.py

Functions.py class -> Functions() 
Functions() methods -> preprocess(s) ; retrieve(query)
preprocess(s, stopWords) ->
	in: string of text, text file of stop words
	out: list of vocabulary for queries.

  The method starts by removing three types of links: links starting with "https://", links starting
  with "www.", and links ending with ".html" (only these three were chosen as there are too many
  domains to cover). It then uses unidecode on the string so that all words are in the Roman
  alphabet to make it easier for detection and processing. Afterward, it removes all numbers,
  punctuation, and any non-alpha characters as they are not useful. It then turns all letters into
  lowercase so that the same words with different capitalization are recognized as the same word.
  Then it will split the string into a list of words and stem them using the Porter Stemmer. Lastly,
  we remove stop words from the list alongside all duplicate words.

retrieve(query, i, stopWords)->
  in: user inputed query string, text file being searched, text file of stop words
	out: dictionary of the cosine similarity of each tweet found for the user's query input

  At the start of this method, we open the file to be searched and remove the first element due to
  it being a weird character that Windows creates. It then opens the Index.p pickle file that
  contains the inverted index. The user query will then be preprocessed using the preprocess()
  method to find the significant words. Each word in the preprocessed query is looped through for
  weight calculation. In this phase, we check with the inverted index to see if the word is part of
  the vocabulary. If it is there, the word's query weight is calculated using the modified tf-idf
  scheme ((0.5 + 0.5 * tf) * idf where tf => word frequency in query per total word amount in query;
  idf => from the inverted index). All document IDs containing that word are added to a list of
  possible outputs. If it is not in the vocabulary, the word is removed from the query. If
  everything is removed, that means that there are no relevant tweets, and thus "No results match
  your search" will be printed in the console.
  Once done weighing phase, all duplicate document IDs, added due to having more than one matching
  query term, will be removed. After removing duplicates, the cosine similarity ranking phase
  starts. As each document is looped through, it calculates the numerator by looping through each
  word and multiplying the document's weight for the word by the query's weight for the word, and
  adding all of the products together. The denominator is calculated by squaring the weights of each
  word in the current document and adding them up, and the same being done for the query. These two
  sums are then multiplied, giving us the denominator. The similarity is calculated by dividing the
  numerator by the denominator and then it is stored in a python dictionary. Afterward, the stored
  cosine similarity is sorted in descending order to show the most relevant documents at the top.
  Lastly, the top 1000 documents are stored in a separate python dictionary where the key is the
  tweet ID and the value is the cosine similarity, and that dictionary is returned.
  
Indexing.py
main(i, stopWords) ->
  in: text file of documents, text file of stop words

  The indexing file's main goal is to create an inverted index based on the list of documents/tweets
  given as input. It reads each document line by line in a 'for' loop. It creates a list of
  preprocessed words by using Functions.preprocess(), passing on the current document and the
  stopWords file as arguments. It then copies the result into another list, removing all duplicate
  words. For each word in the list with no duplicates, the tf is calculated by dividing the number
  of times the word appears by the total amount of words in the preprocessed document. Then it
  checks if the word exists in the current bag of words. If it doesn't, it is added to the bag of
  words. After the 'if' statement finishes, the tf is added to the dictionary containing the
  inverted index, and a separate dictionary keeping track of how many documents use the current word
  is updated.
  Once all documents/tweets have been run through, the idf for each word is calculated and added to
  the inverted index. A new file for the inverted index is created and the binary data is dumped
  into by using pickle. This file is called Index.p. An optional file called Dictionary.txt can be
  printed out by uncommenting lines [50, 53] in the code where it gives the bag of words in
  alphabetical order.

Microblog.py
main(i, tweets, stopWords) ->
  in: text files of test queries, text file of documents, text file of stop words

  This takes as an input the text file of queries and returns a list of relevant documents. The
  number of documents returned will depend on how many match the query up to the maximum value of
  1000 results per query, given to the user in order of most to least relevant. All results are
  added to a freshly created Result.txt file.
  Each query is looped through, saving the topic ID and the title as variables. The method
  Functions.retrieve() is used to create a dictionary of the top 1000 results for the query with the
  cosine similarity, inputting the title, the file of documents, and the file of stop words. The
  result is then formatted into the following:
  <topicId> Q0 <tweetId> <rank> <similarity> PyGER
  This is printed into the Results.txt file.

----------------------------------------------------------------------------------------------------

Algorithms, data structures, and optimizations:

We started off creating the IR system by doing everything one step at a time. When we first did step
1, it would run the code described in Functions.preprocess() to preprocess the whole file containing
the tweets and creating a bag of words outputted in a text file. When we initially did step 2, it
would take in the text file that was created in step 1. It would then loop through each word and
each tweet to calculate the weight. While the code was functional, our biggest issue was the amount
of time it took to run. Since step 2 was using a 'for' loop inside a 'for' loop, it took O(n*m) time
to run. When we tried to test it on the given documents file, it took so many hours to run that we
decided to cut its run short and merge steps 1 and 2.
Now, as can be seen in the description of Indexing.py, we have a 'for' loop that runs through each
tweet and preprocesses it, and also calculates the tf for each word in that tweet. The tf is stored
in a dictionary where each key is a word in our bag of words and the value is a list where the first
item is a None value and the second item is another dictionary, this time the key being the tweet id
and the value is the calculated tf. Once the 'for' loop finishes, another 'for' loop starts
replacing the None value mentioned two lines above with the calculated idf. Doing this helped reduce
our time to O(n+m). Our output for the inverted index is a pickle file that stores the binary of the
python dictionary that contained the calculated weights.
Step 3 was done as a helper function in Functions.py along with the preprocessing function. It opens
the pickle file from step 2 and uses python lists and dictionaries to help keep track of relevant
tweets and their similarity scores. This method is called by step 4 (Microblog.py) which then takes
the returned dictionary result, formats each line, and prints everything out to Results.txt.

----------------------------------------------------------------------------------------------------

Vocabulary:

The size of our dictionary after all the preprocessing done in Indexing.py
is 57099. The first 100 terms in the dictionary (in alphabetical order) are:
- aa,
- aaa,
- aaaaaa,
- aaaaaaa,
- aaaaaaaaaaaaaa,
- aaaaaaaaaaaaaaaaaaaaaaa,
- aaaaaaaaaaaaaah,
- aaaaaaaaaargh,
- aaaaah,
- aaaaaiiiii,
- aaaain,
- aaaaronnnn,
- aaaggghhh,
- aaah,
- aaahh,
- aaand,
- aaanniek,
- aaannnnddd,
- aaarghunknown,
- aaawwwwhhhh,
- aacon,
- aacraoorg,
- aadithama,
- aadukalam,
- aafaqu,
- aafia,
- aag,
- aaha,
- aahaha,
- aahahah,
- aahhahahahadio,
- aai,
- aaiisss,
- aain,
- aaj,
- aalbamcfli,
- aambc,
- aamco,
- aamcocarcar,
- aameen,
- aamer,
- aan,
- aanholt,
- aanhoudingen,
- aankleden,
- aankoopproc,
- aannnnyywhhere,
- aanstekelijk,
- aanunyu,
- aanval,
- aanzettten,
- aapkojashn,
- aapl,
- aargh,
- aarmaanta,
- aarmiinnniym,
- aaron,
- aaronbertrand,
- aaronfresh,
- aaronrodg,
- aarp,
- aarptx,
- aart,
- aartipaarti,
- aashiyana,
- aaup,
- aawayi,
- ab,
- aba,
- ababa,
- abadi,
- abajo,
- aban,
- abandon,
- abandonando,
- abandono,
- abang,
- abank,
- abankinferi,
- abarth,
- abatesnttt,
- abba,
- abbevil,
- abbeyniezgoda,
- abbi,
- abbigliamento,
- abbotsford,
- abbott,
- abbrevi,
- abc,
- abcalert,
- abcchicago,
- abccom,
- abcdefg,
- abcenviron,
- abcnew,
- abcnewsradio,
- abcnorebirth,
- abcpolit,
- abcric

----------------------------------------------------------------------------------------------------

First 10 answers for query 3:

3 Q0 32333726654398464 1 0.702 PyGER
3 Q0 29278582916251649 2 0.669 PyGER
3 Q0 32273316047757312 3 0.664 PyGER
3 Q0 29615296666931200 4 0.639 PyGER
3 Q0 29613127372898304 5 0.639 PyGER
3 Q0 32204788955357184 6 0.614 PyGER
3 Q0 32910196598636545 7 0.611 PyGER
3 Q0 33711164877701120 8 0.598 PyGER
3 Q0 35040428893937664 9 0.55 PyGER
3 Q0 35039337598947328 10 0.55 PyGER

----------------------------------------------------------------------------------------------------

First 10 answers for query 20:

20 Q0 33356942797701120 1 0.761 PyGER
20 Q0 32218912527482880 2 0.676 PyGER
20 Q0 31161931205181440 3 0.634 PyGER
20 Q0 34082003779330048 4 0.626 PyGER
20 Q0 34066620821282816 5 0.626 PyGER
20 Q0 34044932364705792 6 0.626 PyGER
20 Q0 33752688764125184 7 0.626 PyGER
20 Q0 33695252271480832 8 0.626 PyGER
20 Q0 33580510970126337 9 0.626 PyGER
20 Q0 32899186038935552 10 0.626 PyGER

----------------------------------------------------------------------------------------------------

Final results:

$ ./trec_eval.exe -m map -m P.10 ../Trec_microblog11-qrels.txt ../Results.txt
map                     all     0.2058
P_10                    all     0.2286
The above shows the result of the trec_eval script. Using the tf-idf weighting scheme and cosine
similarity score gave us a mean average precision of 20.58% and a precision of the first 10
documents for each query of 22.86%. These scores are not very high, meaning that only about 1/5 of
what is relevant is retrieved. When testing out the retrieval system, it surprised us that some
smaller tweets containing only one keyword were considered to be more relevant than larger tweets
containing all of the keywords. This was because of a fault in the similarity score method that we
used as it raised the score of these small tweets considering they didn't have many other words.
Different methods can be used to increase the trec_eval score, such as the IR system being able to
retrieve phrasal queries, however, that would require a lot more work for the inverted index.
