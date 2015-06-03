#python3
import nltk
from nltk.corpus.reader import WordListCorpusReader
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
    enWd = open('text_files/wordsEn.txt', 'r')
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

def name_features(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count(%s)" % letter] = name.lower().count(letter)
        features["has(%s)" % letter] = (letter in name.lower())
    for i in range(len(name)-1):     # letter bigrams
        features["has({}-{})".format(name[i].lower(), name[i+1].lower())] = True
    if len(name) < 6:
        features["name len"] = 'short'
    else:
        features["name len"] = 'long'
    return features


def hvClassifier(namesReader):
    """ Create and return a hero vs. villain classifier. """
    heroes = namesReader.words('heroes.txt') # from http://babynames.net/list/heroic-names
    villains = namesReader.words('villains.txt')
    labeled_hero_villain = ([(line.rstrip('\n'), 'hero') for line in heroes] +
                            [(line.rstrip('\n'), 'villain') for line in villains])
    random.shuffle(labeled_hero_villain)
    featuresets = [(name_features(n), hv) for (n, hv) in labeled_hero_villain]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    hvClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(hvClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(hvClassifier, test_set))
    return hvClassifier


def mfClassifier(namesReader):
    """ Create and return a masculine vs. feminine classifier. """
    female = namesReader.words('female.txt')
    male = namesReader.words('male.txt')
    labeled_fem_masc = ([(line.rstrip('\n'), 'feminine') for line in female] +
            [(line.rstrip('\n'), 'masculine') for line in male])
    random.shuffle(labeled_fem_masc)
    featuresets = [(name_features(n), fm) for (n, fm) in labeled_fem_masc]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    mfClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(mfClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(mfClassifier, test_set))
    return mfClassifier


def adClassifier(namesReader):
    """ Create and return an angel vs. demon classifier. """
    angels = namesReader.words('angels.txt')
    demons = namesReader.words('demons.txt')
    labeled_ang_dem = ([(line.rstrip('\n'), 'angel') for line in angels] +
                        [(line.rstrip('\n'), 'demon') for line in demons])
    random.shuffle(labeled_ang_dem)
    featuresets = [(name_features(n), ad) for (n, ad) in labeled_ang_dem]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    adClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(adClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(adClassifier, test_set))
    return adClassifier

def pdClassifier(namesReader):
    """ Create and return an pokemon vs. digimon classifier. """
    pokemon = namesReader.words('pokemon.txt')
    digimon = namesReader.words('digimon.txt')
    labeled_pok_dig = ([(line.rstrip('\n'), 'pokemon') for line in pokemon] +
                        [(line.rstrip('\n'), 'digimon') for line in digimon])
    random.shuffle(labeled_pok_dig)
    featuresets = [(name_features(n), pd) for (n, pd) in labeled_pok_dig]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    pdClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(pdClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(pdClassifier, test_set))
    return pdClassifier


def userClassifier(namesReader, userNames):
    """ Create and return a classifier based on user-provided names. """
    names = namesReader.words('names.txt') #name data from: https://github.com/hadley/data-baby-names
    namesList = [line for line in names]
    random.shuffle(namesList)
    shorterNamesList = [] #This list is a list of random names equal in length to the number of names the user inputted. For comparative classification.
    i = 0
    while (len(shorterNamesList) <= len(userNames)) :
        shorterNamesList.append(namesList[i].rstrip('\n'))
        i = i + 1
    labeled_user_names = ([(name, 'good') for name in userNames] +
            [(badName, 'bad') for badName in shorterNamesList])
    random.shuffle(labeled_user_names)
    featuresets = [(name_features(n), g) for (n, g) in labeled_user_names]
    train_set, test_set = featuresets[int(len(featuresets)/4):], featuresets[:int(len(featuresets)/4)]
    userClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(userClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(userClassifier, test_set))
    return userClassifier


def multiClassifier(name, parameters, classifiers):
    """ Return labels for a name using the appropriate classifiers.

    Match each non-None element of parameters to the appropriate classifier
    and return the overall classification. """
    classification = set()
    for i in range(len(parameters)):
        if parameters[i] is not None:
            classification.add(classifiers[i].classify(name_features(name)))
    gb = classifiers[len(parameters)].classify(name_features(name))
    classification.add(gb)
    return classification


def main():

    # Arguments: directory and the fileids
    namesReader = WordListCorpusReader(
                './names_corpus',
                ['angels.txt', 'demons.txt', 'digimon.txt', 'fantasyNames.txt',
                 'female.txt', 'female2.txt', 'heroes.txt', 'male.txt',
                 'male2.txt', 'names.txt', 'pokemon.txt', 'villains.txt']
            )

    # Will prompt user if they want to force a male or female name, if so outputs come from male.txt or female.txt instead of names.txt
    forceMale = False
    forceFemale = False

    forceFantasy = False

     # Initialize list for user provided names. Both names from text files and from command line are listed in userNames.
    userNames = []

    # input: read text file. Find names through Named Entity Recognition
    inputFile = input("**Enter the name of a text file containing a story you've written (hit enter to skip).\n")
    print()
    if (inputFile is not "" and os.path.exists(inputFile)) : #if user doesn't enter anything, skip this.
    	i = open(inputFile, 'r')
    	userNames.extend(process(i.read()))
    	i.close()
    	print("Names from the text file provided: ")
    	print(userNames)
    	print()
    else :
    	print("Text file input not used.")
    	print()

    # input: names directly from user
    inputNames = input("**Enter some names you like, separated by commas. Hit enter when finished.\n")
    print()
    if(inputNames is not "") :
    	inputList = [name.strip() for name in inputNames.split(',')]
    	userNames.extend(inputList)

    # input: desired traits
    traitsList = []
    traits1 = input("**Enter which name traits you desire: Hero, Villain, Angel, Demon, Pokemon, Digimon, Masculine, Feminine.\n" + \
                    "**Type 0 or more separated by commas: \n")
    print()

    traits2 = [name.strip().lower() for name in traits1.split(',')]
    traitsList.extend(traits2)


    if ("yes" in input("**Force a candidate name from a fantasy list? If so you cannot force a gender. (Type 'yes' do to so)\n").lower()) :
        forceFantasy = True
    elif ("yes" in input("**Force a male name? (type 'yes' do to so)\n").lower()) :
        forceMale = True
    elif ('yes' in input("**Force a female name? (type 'yes' do to so)\n").lower()) :
        forceFemale = True
    print()

    # Run classifier on 'names.txt' or male.txt/female.txt if specified by user. Output 20 suggested names
    if (forceFantasy) :
        fantasy = namesReader.words('fantasyNames.txt') #from http://www.creative-role-playing.com/fantasy-sounding-names/
        namesList = [fanName for fanName in fantasy]
    elif (forceMale) :
        male = namesReader.words('male2.txt')
        namesList = [mName for mName in male]
    elif (forceFemale) :
        female = namesReader.words('female2.txt')
        namesList = [fmName for fmName in female]
    else:
        names = namesReader.words('names.txt')
        namesList = [name for name in names]


    # Run classifiers on each name from names.txt until n names are found that match classifications from all relevant classifiers
    n = input("**How many suggested names would you like? Pick a number greater than 20.\n")
    if n is "":
    	n = "20"
    n = int(n)
    while n < 20:
        n = int(input("**Please pick a number greater than 20.\n"))
    print()
    print("Suggested Names ({}): ".format(n))
    random.shuffle(namesList)

    # Create the list of classifiers
    classifiers = [hvClassifier(namesReader), mfClassifier(namesReader),
            adClassifier(namesReader), pdClassifier(namesReader),
            userClassifier(namesReader, userNames)]

    # parameters starts as a list of Nones (as many as there are classifiers) and elements are updated
    parameters = [None]*(len(classifiers)-1)
    if ("hero" in traitsList) :
        parameters[0] = 'hero'
    if ("villain" in traitsList) :
        parameters[0] = 'villain'
    if ("masculine" in traitsList) :
        parameters[1] = 'masculine'
    if ("feminine" in traitsList) :
        parameters[1] = 'feminine'
    if ("angel" in traitsList):
        parameters[2] = 'angel'
    if ("demon" in traitsList):
        parameters[2] = 'demon'
    if ("pokemon" in traitsList) :
    	parameters[3] = 'pokemon'
    if ("digimon" in traitsList) :
        parameters[3] = 'digimon'

    # onParameters contains only the relevant ones
    onParameters = set([x for x in parameters if x is not None])
    #print("parameters: {}".format(parameters))
    #print("onParameters: {}".format(onParameters))


    # Pass multiClassifier the entire set of parameters and print a name if
    # the classification matches the desired traits.
    i = 0
    j = 0
    while j < n and i < len(namesList):
        classification = multiClassifier(namesList[i], parameters, classifiers)
        if onParameters.issubset(classification):
            print(namesList[i])
            j = j+1
        i = i+1

main()
