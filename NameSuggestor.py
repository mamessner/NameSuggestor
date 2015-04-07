#python3
import nltk
import random

def main() :

    # Will prompt user if they want to force a male or female name, if so outputs come from male.txt or female.txt instead of names.txt
    forceMale = False
    forceFemale = False

     # Initialize list for user provided names. Both names from text files and from command line are listed in userNames.
    userNames = []

    # Initialize trait booleans. Will be set to true if user designates they should be on.
    isHeroOn = False
    isVillianOn = False
    isMasculineOn = False
    isFeminineOn = False


    # input: read text file
    # toDo: implement: Input text file and iterate over for capitalized words and/or words that match a list of names. Store in list.

    # input: names directly from user
    # toDo: implement: Read command line input from users. Store in list.
    inputNames = input("Enter some names you like, separated by commas. Hit enter when finished.\n")
    inputList = [name.strip() for name in inputNames.split(',')]
    userNames.extend(inputList)

        
    # input: desired traits
    # toDo: implement: prompt user for which traits



    # Machine learning using features specified
    # toDo: implement using code from class as base

    # Machine learning using inputted names from user
    # toDo: implement using code from class as base

    # Run classifier on 'names.txt' or male.txt/female.txt if specified by user.
    # toDo: implement ??



    # output: names

    print ('hello')

main()
