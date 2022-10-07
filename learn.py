# In the JSON file store a dictionary filled with counts of each word in spam & ham
# Different JSON file for normal, stopwords, lemmitization, etc

import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
stopWordsSet = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Control booleans for stop words and lemmatization
stopWord = True
lemmatization = True


# Setting the path to the specified path and changing the directory
path = "/Users/matt/Downloads/enron1/ham"
os.chdir(path)

fileNames = os.listdir(path)

# Loops through every file under the specified path
#counter = 1
hamDict = {}
for i in fileNames:
    with open(i, 'r', errors="ignore") as f:
        # Using both stop words and lemmatization
        if stopWord and lemmatization:
            tokenized_word = word_tokenize(f.read())
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                if lemWord not in stopWordsSet:
                    if lemWord not in hamDict:
                        hamDict[lemWord] = 0
                    hamDict[lemWord] = hamDict[lemWord] + 1
        # Using stopwords
        elif stopWord:
            tokenized_word = word_tokenize(f.read())
            for word in tokenized_word:
                if word not in stopWordsSet:
                    if word not in hamDict:
                        hamDict[word] = 0
                    hamDict[word] = hamDict[word] + 1
        # Using lemmatization
        elif lemmatization:
            tokenized_word = word_tokenize(f.read())
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                if lemWord not in hamDict:
                    hamDict[lemWord] = 0
                hamDict[lemWord] = hamDict[lemWord] + 1
        # Using neither
        else:
            tokenized_word = word_tokenize(f.read())
            for word in tokenized_word:
                if word not in hamDict:
                    hamDict[word] = 0
                hamDict[word] = hamDict[word] + 1
# print(hamDict)
# This adds the number of files in the folder / path to the end of the dictionary, as we will need it in the other file
# This key will be removed out of the dict later using regular expressions
hamDict["FolderFileLength"] = len(fileNames)

# --------------------------------------------------------------------------------------------------------

path = "/Users/matt/Downloads/enron1/spam"
os.chdir(path)

fileNames2 = os.listdir(path)

# Loops through every file under the specified path
spamDict = {}
for j in fileNames2:
    with open(j, 'r', errors="ignore") as n:
        # Using both stop words and lemmatization
        if stopWord and lemmatization:
            tokenized_word = word_tokenize(n.read())
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                if lemWord not in stopWordsSet:
                    if lemWord not in spamDict:
                        spamDict[lemWord] = 0
                    spamDict[lemWord] = spamDict[lemWord] + 1
        # Using stopwords
        elif stopWord:
            tokenized_word = word_tokenize(n.read())
            for word in tokenized_word:
                if word not in stopWordsSet:
                    if word not in spamDict:
                        spamDict[word] = 0
                    spamDict[word] = spamDict[word] + 1
        # Using lemmatization
        elif lemmatization:
            tokenized_word = word_tokenize(n.read())
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                if lemWord not in spamDict:
                    spamDict[lemWord] = 0
                spamDict[lemWord] = spamDict[lemWord] + 1
        # Using neither
        else:
            # Counter to see files
            # print("----------------Email number: ", end="")  # All these lines just to print
            # print(counter, end="")
            # print("----------------")
            # counter = counter + 1
            tokenized_word = word_tokenize(f.read())
            for word in tokenized_word:
                if word not in spamDict:
                    spamDict[word] = 0
                spamDict[word] = spamDict[word] + 1
# print(spamDict)
# This adds the number of files in the folder / path to the end of the dictionary, as we will need it in the other file
# This key will be removed out of the dict later using regular expressions
spamDict["FolderFileLength"] = len(fileNames2)

# --------------------------------------------------------------------------------------------------------

# Setting the path back to this python file
path = "/Users/matt/PycharmProjects/spamFilter"
os.chdir(path)

print(hamDict)
with open("knowledgeHam.json", "w") as outfile:
    json.dump(hamDict, outfile, indent=4)

with open("knowledgeSpam.json", "w") as outfile2:
    json.dump(spamDict, outfile2, indent=4)

