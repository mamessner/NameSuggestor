#python3
import nltk
import random
import re
import os

def process(document):
    """ Reurn the named entities in a document using Named Entity Recognition """
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    namedEnt = [nltk.ne_chunk(sent) for sent in sentences]
    names = []

    # Make list of words in english to compare names to. Name not counted as a name if it's found as an English word.
    # This causes some actual names to be left off, but also eliminates things that were improperly classified as names by nltk.
    enWd = open('wordsEn.txt', 'r')
    wordsList = [word.title() for word in enWd.read().split()]
    enWd.close()

    # Pick out words tagged as "PERSON" from the tree. Uses regular expressions.
    for ent in namedEnt :
        for line in ent :
            line = str(line)
            m = re.search('(?<=PERSON )\w+', line)
            if m is not None and str(m.group(0)) not in names and str(m.group(0)) not in wordsList:
                names.append(str(m.group(0)))
    return names

userNames = []
h = open('heroes.txt', 'r') # from http://babynames.net/list/heroic-names
v = open('villains.txt', 'r')
labeled_hero_villain = ([(line.rstrip('\n'), 'hero') for line in h] +
                            [(line.rstrip('\n'), 'villain') for line in v])
h.close()
v.close()
f = open('female.txt', 'r')
m = open('male.txt', 'r')
labeled_fem_masc = ([(line.rstrip('\n'), 'feminine') for line in f] + [(line.rstrip('\n'), 'masculine') for line in m])
f.close()
m.close()
a = open('angels.txt', 'r')
d = open('demons.txt', 'r')
labeled_ang_dem = ([(line.rstrip('\n'), 'angel') for line in a] +
                    [(line.rstrip('\n'), 'demon') for line in d])
a.close()
d.close()
p = open('pokemon.txt', 'r')
d = open('digimon.txt', 'r')
labeled_pok_dig = ([(line.rstrip('\n'), 'pokemon') for line in p] +
                    [(line.rstrip('\n'), 'digimon') for line in d])
p.close()
d.close()

inputFile = "HarryPotter.txt"
i = open(inputFile, 'r')
userNames.extend(process(i.read()))
i.close()
inputNames = "Joe, John, Kim, Jill, Jen, Kira, Dave, Gaby, Dylan, Melanie, Stephanie, Kimberly"
inputList = [name.strip() for name in inputNames.split(',')]
userNames.extend(inputList)
n = open('names.txt', 'r') #name data from: https://github.com/hadley/data-baby-names
namesList = [line for line in n]
n.close()

def name_features(name):
    features = {}
    #1
    features["first_letter"] = name[0].lower()
    #2
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count(%s)" % letter] = name.lower().count(letter) #3
        features["has(%s)" % letter] = (letter in name.lower()) #4
    for i in range(len(name)-1):      # adjacent letters feature
        features["has({}-{})".format(name[i].lower(), name[i+1].lower())] = True #5
    features["name len"] = len(name) #6
    return features


def hvClassifier():
    """ Create and return a hero vs. villain classifier. """
    random.shuffle(labeled_hero_villain)
    featuresets = [(name_features(n), hv) for (n, hv) in labeled_hero_villain]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    hvClassifier = nltk.NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(hvClassifier, test_set)

def mfClassifier():
    """ Create and return a masculine vs. feminine classifier. """
    random.shuffle(labeled_fem_masc)
    featuresets = [(name_features(n), fm) for (n, fm) in labeled_fem_masc]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    mfClassifier = nltk.NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(mfClassifier, test_set)

def adClassifier():
    """ Create and return an angel vs. demon classifier. """
    random.shuffle(labeled_ang_dem)
    featuresets = [(name_features(n), ad) for (n, ad) in labeled_ang_dem]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    adClassifier = nltk.NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(adClassifier, test_set)

def pdClassifier():
    """ Create and return an pokemon vs. digimon classifier. """
    random.shuffle(labeled_pok_dig)
    featuresets = [(name_features(n), pd) for (n, pd) in labeled_pok_dig]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    pdClassifier = nltk.NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(pdClassifier, test_set)


def userClassifier(userNames):
    """ Create and return a classifier based on user-provided names. """
    random.shuffle(namesList)
    shorterNamesList = [] #This list is a list of random names equal in length to the number of names the user inputted. For comparative classification.
    i = 0
    while (len(shorterNamesList) <= len(userNames)) :
        shorterNamesList.append(namesList[i].rstrip('\n'))
        i = i + 1
    labeled_user_names = ([(name, 'good') for name in userNames] + [(badName, 'bad') for badName in shorterNamesList])
    random.shuffle(labeled_user_names)
    featuresets = [(name_features(n), g) for (n, g) in labeled_user_names]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    userClassifier = nltk.NaiveBayesClassifier.train(train_set)
    return nltk.classify.accuracy(userClassifier, test_set)

def main() :

    n = 0
    hvAcc = 0
    mfAcc = 0
    adAcc = 0
    pdAcc = 0
    userAcc = 0


    while n < 100 :
        hvAcc = hvAcc + hvClassifier()
        mfAcc = mfAcc + mfClassifier()
        adAcc = adAcc + adClassifier()
        pdAcc = pdAcc + pdClassifier()
        userAcc = userAcc + userClassifier(userNames)
        n = n + 1
        print(n)

    print("hvAcc: ")
    print(hvAcc / 100)
    print("mfAcc: ")
    print(mfAcc / 100)
    print("adAcc: ")
    print(adAcc / 100)
    print("pdAcc: ")
    print(pdAcc / 100)
    print("userAcc: ")
    print(userAcc / 100)

main()
