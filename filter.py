# Uses the probability equation we used in each class. Looks at prob of word in spam, then in ham
# then iterates to next word

import json
import math
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

stopWordsSet = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

"""
This method returns the P(key|d1), determines the numerator & denominator, then returns numerator / denominator
@:param d1, the first dictionary that you are determining probability of the key in
@:param d2, the second dictionary only used for the |V| or total unique words along both dictionaries
@:param key, the word which we are determining probability of
@:param denom, doing the math for the denominator in the other method, to improve efficiency and not do it 1000x per file
"""
def keyProbability(d1, d2, key, denom):
    # determining the numerator, count (w,c) + 1
    if key not in d1:
        numerator = 1
    else:
        numerator = d1[key] + 1

    # had the code for the denominator here originally, moved it to separate method

    return numerator / denom


"""
Returns the denominator according to the probability equation, the count(c) + |v|
@:param classA the first dictionary of the class you're testing probability of
@:param classB second dictionary, just used for |v| of the equation
"""
def denominator(classA, classB):
    totalSum = 0
    for k in classA:
        totalSum = totalSum + classA[k]

    # Total # of words/keys in both dictionaries, need to avoid repeats
    keySum = 0
    for k in classA:
        # If the word isn't in the other dictionary (and is the first) add one
        if k not in classB:
            keySum = keySum + 1
        # Increment for every word in the second d
    for k in classB:
        keySum = keySum + 1
    denom = totalSum + keySum
    return denom

"""
Determines if a file is class A or class B based off of probability, P(word|class)
Returns a boolean based off if the probability of classA is >= classB
@:param file the file we are working with
@:param classA the dictionary of the word counts of class A, the first class we are working with
@:param classB the dictionary of the word counts of class B, the second class we are working with
@:param classALength length of classA dictionary
@:param classBLength length of classB dictionary
@:param stopwords, boolean for if we are using stopwords improvement
@:param lemmatization, boolean for if we are using stopwords improvement
"""
def fileProbability(file, classA, classB, classALength, classBLength, stopWords, lemmatization):
    # Since the count(c) + |v| is the same for every key in P(key|class), we are determining once for classA and once
    # for class B, for efficiency purposes
    classADenom = denominator(classA, classB)
    classBDenom = denominator(classB, classA)

    with open(file, 'r', errors="ignore") as f:
        # Sets 2 lists with the probabilities, starting the P(classA) and P(classB)
        probabilityList1 = [classALength / (classALength + classBLength)]
        probabilityList2 = [classBLength / (classALength + classBLength)]

        # Find probability of each word of the current file being in classA, and classB
        # Also uses stop words and lemmatization
        tokenized_word = word_tokenize(f.read())
        if stopWords and lemmatization:
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                if lemWord not in stopWordsSet:
                    probabilityList1.append(keyProbability(classA, classB, lemWord, classADenom))
                    probabilityList2.append(keyProbability(classB, classA, lemWord, classBDenom))
        elif stopWords:
            for word in tokenized_word:
                if word not in stopWordsSet:
                    probabilityList1.append(keyProbability(classA, classB, word, classADenom))
                    probabilityList2.append(keyProbability(classB, classA, word, classBDenom))
        elif lemmatization:
            for word in tokenized_word:
                lemWord = lemmatizer.lemmatize(word)
                probabilityList1.append(keyProbability(classA, classB, lemWord, classADenom))
                probabilityList2.append(keyProbability(classB, classA, lemWord, classBDenom))
        else:
            for word in tokenized_word:
                probabilityList1.append(keyProbability(classA, classB, word, classADenom))
                probabilityList2.append(keyProbability(classB, classA, word, classBDenom))

        # Sum up the total probability for classA, with underflow protection
        probA = 0
        for j in probabilityList1:
            probA = probA + math.log10(j)

        # Sum up the total probability for classA, with underflow protection`
        probB = 0
        for j in probabilityList2:
            probB = probB + math.log10(j)

        # Check what prob is higher, and print what class the file is
        if probA >= probB:
            return True
        else:
            return False


# ------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Opening json files
    with open('knowledgeHam.json') as infile:
        ham = json.load(infile)
        #print(ham)

    with open('knowledgeSpam.json') as infile:
        spam = json.load(infile)
        #print(spam)

    # Removes and saves the amt of files / length
    hamLength = ham.pop("FolderFileLength")
    spamLength = spam.pop("FolderFileLength")

    # Flags, enables and disables stop words and lemmatization
    stopWords = False
    lemmatization = True

    # Ham ----------------------------------- enron2
    path = "/Users/matt/Downloads/enron2/ham"
    os.chdir(path)
    fileNames = os.listdir(path)
    length = len(fileNames)

    correct = 0
    incorrect = 0
    for i in fileNames:
        if fileProbability(i, ham, spam, hamLength, spamLength, stopWords, lemmatization):
            # In this case if the function returns true, it is ham
            correct = correct + 1
            # print("This file is Ham. Algorithm outputted: Ham")
        else:
            incorrect = incorrect + 1
            # print("This file is Ham. Algorithm outputted: Spam")

    print("Enron2, ham. In ", end="")
    print(length, end="")
    print(" files, the algorithm determined this many correct: ", end="")
    print(correct, end="")
    print(" and this many incorrect: ", end="")
    print(incorrect)

    # Spam ----------------------------------- enron2
    path = "/Users/matt/Downloads/enron2/spam"
    os.chdir(path)
    fileNames = os.listdir(path)
    length = len(fileNames)

    correct = 0
    incorrect = 0
    for i in fileNames:
        if fileProbability(i, spam, ham, hamLength, spamLength, stopWords, lemmatization):
            # In this case if the function returns true, it is ham
            correct = correct + 1
            # print("This file is Spam. Algorithm outputted: Spam")
        else:
            incorrect = incorrect + 1
            # print("This file is Spam. Algorithm outputted: Ham")

    print("Enron2, spam. In ", end="")
    print(length, end="")
    print(" files, the algorithm determined this many correct: ", end="")
    print(correct, end="")
    print(" and this many incorrect: ", end="")
    print(incorrect)

    # Ham ----------------------------------- enron3
    path = "/Users/matt/Downloads/enron3/ham"
    os.chdir(path)
    fileNames = os.listdir(path)
    length = len(fileNames)

    correct = 0
    incorrect = 0
    for i in fileNames:
        if fileProbability(i, ham, spam, hamLength, spamLength, stopWords, lemmatization):
            # In this case if the function returns true, it is ham
            correct = correct + 1
            #print("This file is Ham. Algorithm outputted: Ham")
        else:
            incorrect = incorrect + 1
            #print("This file is Ham. Algorithm outputted: Spam")

    print("Enron3, ham. In ", end="")
    print(length, end="")
    print(" files, the algorithm determined this many correct: ", end="")
    print(correct, end="")
    print(" and this many incorrect: ", end="")
    print(incorrect)

    # Spam ----------------------------------- enron3
    path = "/Users/matt/Downloads/enron3/spam"
    os.chdir(path)
    fileNames = os.listdir(path)
    length = len(fileNames)

    correct = 0
    incorrect = 0
    for i in fileNames:
        if fileProbability(i, spam, ham, hamLength, spamLength, stopWords, lemmatization):
            # In this case if the function returns true, it is ham
            correct = correct + 1
            #print("This file is Spam. Algorithm outputted: Spam")
        else:
            incorrect = incorrect + 1
            #print("This file is Spam. Algorithm outputted: Ham")

    print("Enron3, spam. In ", end="")
    print(length, end="")
    print(" files, the algorithm determined this many correct: ", end="")
    print(correct, end="")
    print(" and this many incorrect: ", end="")
    print(incorrect)

print("In this trial, stopwords: ", end="")
print(stopWords, end="")
print(" and lemmitization: ", end="")
print(lemmatization, end="")