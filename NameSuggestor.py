#python3
import nltk
import random
import re

def name_features(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count(%s)" % letter] = name.lower().count(letter)
        features["has(%s)" % letter] = (letter in name.lower())
    for i in range(len(name)-1):      # adjacent letters feature
        features["has({}-{})".format(name[i].lower(), name[i+1].lower())] = True
    features["name len"] = len(name)
    return features


def hvClassifier():
    """ Create and return a hero vs. villain classifier. """
    h = open('heroes.txt', 'r') # from http://babynames.net/list/heroic-names
    v = open('villains.txt', 'r')
    labeled_hero_villain = ([(line.rstrip('\n'), 'hero') for line in h] +
                            [(line.rstrip('\n'), 'villain') for line in v])
    random.shuffle(labeled_hero_villain)
    featuresets = [(name_features(n), hv) for (n, hv) in labeled_hero_villain]
    train_set, test_set = featuresets[int(len(featuresets)/2):], featuresets[:int(len(featuresets)/2)]
    hvClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(hvClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(hvClassifier, test_set))
    h.close()
    v.close()
    return hvClassifier


def mfClassifier():
    """ Create and return a masculine vs. feminine classifier. """
    f = open('female.txt', 'r')
    m = open('male.txt', 'r')
    labeled_fem_masc = ([(line.rstrip('\n'), 'feminine') for line in f] + [(line.rstrip('\n'), 'masculine') for line in m])
    random.shuffle(labeled_fem_masc)
    featuresets = [(name_features(n), fm) for (n, fm) in labeled_fem_masc]
    train_set, test_set = featuresets[int(len(featuresets)/2):], featuresets[:int(len(featuresets)/2)]
    mfClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(mfClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(mfClassifier, test_set))
    f.close()
    m.close()
    return mfClassifier


def userClassifier(userNames):
    """ Create and return a classifier based on user-provided names. """
    n = open('names.txt', 'r') #name data from: https://github.com/hadley/data-baby-names
    namesList = [line for line in n]
    random.shuffle(namesList)
    shorterNamesList = [] #This list is a list of random names equal in length to the number of names the user inputted. For comparative classification.
    i = 0
    while (len(shorterNamesList) <= len(userNames)) :
        shorterNamesList.append(namesList[i].rstrip('\n'))
        i = i + 1
    labeled_user_names = ([(name, 'good') for name in userNames] + [(badName, 'bad') for badName in shorterNamesList])
    random.shuffle(labeled_user_names)
    featuresets = [(name_features(n), g) for (n, g) in labeled_user_names]
    train_set, test_set = featuresets[int(len(featuresets)/2):], featuresets[:int(len(featuresets)/2)]
    userClassifier = nltk.NaiveBayesClassifier.train(train_set)
    #print(userClassifier.show_most_informative_features(20))
    #print(nltk.classify.accuracy(userClassifier, test_set))
    n.close()
    return userClassifier


def multiClassifier(name, hvTrait=False, mfTrait=False):
    """ Return labels for a name using the appropriate classifiers. """
    classification = set()
    if hvTrait is True:
        hv = classifiers[0].classify(name_features(name))
        classification.add(hv)
    if mfTrait is True:
        mf = classifiers[1].classify(name_features(name))
        classification.add(mf)
    gb = classifiers[2].classify(name_features(name))
    classification.add(gb)
    return classification


def main() :

    # Will prompt user if they want to force a male or female name, if so outputs come from male.txt or female.txt instead of names.txt
    forceMale = False
    forceFemale = False

     # Initialize list for user provided names. Both names from text files and from command line are listed in userNames.
    userNames = []

    # Initialize trait booleans. Will be set to true if user designates they should be on.
    isHeroOn = False
    isVillainOn = False
    isMasculineOn = False
    isFeminineOn = False


    # input: read text file. Find names.
    i = open('exampleTextInput.txt', 'r')
    nam = open('names.txt', 'r')
    text = i.read().lower()
    text = re.sub('[^a-z\ \']+', " ", text)
    longListofNames = [name for name in nam.read().split()]
    for name in text.split() :
        if name.title() in longListofNames :
            userNames.append(name.title())
    i.close()
    nam.close()

    # input: names directly from user
    inputNames = input("**Enter some names you like, separated by commas. Hit enter when finished.\n")
    print()
    inputList = [name.strip() for name in inputNames.split(',')]
    userNames.extend(inputList)

    # input: desired traits
    traitsList = []
    traits1 = input("**Enter which name traits you desire: Hero, Villain, Masculine, Feminine.\n**Type 0 or more seperated by commas: \n")
    print()

    traits2 = [name.strip().lower() for name in traits1.split(',')]
    traitsList.extend(traits2)
    if ("hero" in traitsList) :
        isHeroOn = True
    if ("villain" in traitsList) :
        isVillainOn = True
    if ("masculine" in traitsList) :
        isMasculineOn = True
    if ("feminine" in traitsList) :
        isFeminineOn = True

    if ("yes" in input("**Force a male name? (type 'yes' do to so)\n").lower()) :
        forceMale = True
    elif ('yes' in input("**Force a female name? (type 'yes' do to so)\n").lower()) :
        forceFemale = True
    print()

    # Run classifier on 'names.txt' or male.txt/female.txt if specified by user. Output 20 suggested names
    if (forceMale) :
        a = open('male2.txt', 'r')
        namesList = [line for line in a]
        a.close()
    elif (forceFemale) :
        a = open('female2.txt', 'r')
        namesList = [line for line in a]
        a.close()
    else:
        namesList = longListofNames

    parameter1 = ''
    parameter2 = ''
    if (isHeroOn) :
        parameter1 = 'hero'
    if (isVillainOn) :
        parameter1 = 'villain'
    if (isMasculineOn) :
        parameter2 = 'masculine'
    if (isFeminineOn) :
        parameter2 = 'feminine'

    global classifiers
    classifiers = [hvClassifier(), mfClassifier(), userClassifier(userNames)]

    # Run classifiers on each name from names.txt until n names are found that match classifications from all relevant classifiers
    n = int(input("**How many suggested names would you like? Pick a number greater than 20.\n"))
    while n < 20:
        n = int(input("**Please pick a number greater than 20.\n"))
    print()
    print("Suggested Names ({}): ".format(n))
    random.shuffle(namesList)

    i = 0
    j = 0
    if ((isHeroOn or isVillainOn) and (isMasculineOn or isFeminineOn)) :
        while j < n :
            # only specify the relevant traits as True; all others False by default
            classification = multiClassifier(namesList[i], hvTrait=True, mfTrait=True)
            if {'good', parameter1, parameter2}.issubset(classification):
                print(namesList[i])
                j = j+1
            i = i+1
    elif (isHeroOn or isVillainOn) :
        while j < n :
            classification = multiClassifier(namesList[i], hvTrait=True)
            if {'good', parameter1}.issubset(classification):
                print(namesList[i])
                j = j+1
            i = i+1
    elif (isMasculineOn or isFeminineOn) :
        while j < n :
            classification = multiClassifier(namesList[i], mfTrait=True)
            if {'good', parameter2}.issubset(classification):
                print(namesList[i])
                j = j+1
            i = i+1
    else :
        while j < n :
            classification = multiClassifier(namesList[i])
            if {'good'}.issubset(classification):
                print(namesList[i])
                j = j+1
            i = i+1

main()
