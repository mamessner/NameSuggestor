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
	return features

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
    print(text.split())
    longListofNames = [name for name in nam.read().split()]
    for name in text.split() :
    	if name.title() in longListofNames :
    		userNames.append(name.title())

    # input: names directly from user
    inputNames = input("**Enter some names you like, separated by commas. Hit enter when finished.\n")
    inputList = [name.strip() for name in inputNames.split(',')]
    userNames.extend(inputList)

    # input: desired traits
    traitsList = []
    traits1 = input("**Enter which name traits you desire: Hero, Villain, Masculine, Feminine.\n**Type 0 or more seperated by commas: \n")
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


    # Machine learning using features specified
    if (isHeroOn or isVillainOn) :
    	h = open('heroes.txt', 'r')
    	v = open('villains.txt', 'r')
    	labeled_hero_villain = ([(line.rstrip('\n'), 'hero') for line in h] + [(line.rstrip('\n'), 'villain') for line in v])
    	random.shuffle(labeled_hero_villain)
    	featuresets = [(name_features(n), hv) for (n, hv) in labeled_hero_villain]
    	train_set, test_set = featuresets[int(len(featuresets)/2):], featuresets[:int(len(featuresets)/2)]
    	classifier = nltk.NaiveBayesClassifier.train(train_set)
    	print(classifier.show_most_informative_features(20))
    	print(nltk.classify.accuracy(classifier, test_set))

    if (isFeminineOn or isMasculineOn) :
    	f = open('female.txt', 'r')
    	m = open('male.txt', 'r')
    	labeled_fem_masc = ([(line.rstrip('\n'), 'feminine') for line in f] + [(line.rstrip('\n'), 'masculine') for line in m])
    	random.shuffle(labeled_fem_masc)
    	featuresets = [(name_features(n), fm) for (n, fm) in labeled_fem_masc]
    	train_set, test_set = featuresets[int(len(featuresets)/2):], featuresets[:int(len(featuresets)/2)]
    	classifier = nltk.NaiveBayesClassifier.train(train_set)
    	print(classifier.show_most_informative_features(20))
    	print(nltk.classify.accuracy(classifier, test_set))


    # Machine learning using inputted names from user. Labels names entered by user as good, and random other names as bad.
    n = open('names.txt', 'r')
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
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(classifier.show_most_informative_features(20))
    print(nltk.classify.accuracy(classifier, test_set))


    # Run classifier on 'names.txt' or male.txt/female.txt if specified by user.
    # toDo: implement ??



    # output: names


    print (userNames)

main()
