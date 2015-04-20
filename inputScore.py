#python3

#Calculates validity of different methods of extracting names form input file for HarryPotter.txt
#Not functional part of project. Ignore.

actual = ['Harry', 'McGonagall', 'Hagrid', 'Neville', 'Ron', 'Hermione', 'Peeves', 'Fat Friar', 'Petunia', 'Hannah', 'Susan', 'Terry', 'Lavender', 'Millicent', 'Dudley', 'Justin', 'Seamus', 'Hermione', 'Morag', 'Malfoy', 'Crabbe', 'Goyle', 'Moon', 'Nott', 'Parkinson', 'Patil', 'Sally-Anne', 'Percy', 'Dumbledore', 'Albus', 'Dean', 'Lisa', 'Blaise', 'Nick', 'Nicholas', 'Enid' 'Algie', 'Quirrell', 'Snape', 'Filch', 'Scabbers']
# 2
checkNames = ['Emerald', 'Green', 'Will', 'Hall', 'Stone', 'Harry', 'Noble', 'Hope', 'Ron', 'Fred', 'Else', 'Pearly', 'Little', 'Chance', 'Sandy', 'Long', 'Golden', 'Misty', 'Silver', 'Sky', 'Sing', 'May', 'Judge', 'Cap', 'Loyal', 'Roll', 'Abbott', 'Hannah', 'Pink', 'Merrily', 'Susan', 'Terry', 'Mandy', 'Brown', 'Millicent', 'Dudley', 'Justin', 'Seamus', 'Sally', 'Anne', 'Percy', 'Young', 'Thomas', 'Dean', 'Lisa', 'Blaise', 'Reason', 'Nicholas', 'Nick', 'Rice', 'Algie', 'Enid', 'Job', 'Fed', 'Forest', 'Rose', 'Worth', 'Ah', 'Baron', 'Hung', 'Red', 'Velvet', 'Destiny']
# 3
ner = ['Harry', 'Professor', 'Hagrid', 'Ravenclaw', 'Slytherin', 'Neville', 'Ron', 'Fred', 'Hermione', 'Aunt', 'Set', 'Will', 'Abbott', 'Hannah', 'Susan', 'Terry', 'Mandy', 'Brown', 'Lavender', 'Bulstrode', 'Millicent', 'Dudley', 'Justin', 'Granger', 'Morag', 'Crabbe', 'Goyle', 'Parkinson', 'Patil', 'Very', 'Potter', 'Albus', 'Thomas', 'Lisa', 'Percy', 'Blaise', 'Nitwit', 'Sir', 'Nearly', 'Mimsy', 'Seamus', 'Nicholas', 'Someone', 'Mom', 'Algie', 'Uncle', 'Enid', 'Gran', 'Quirrell', 'Snape', 'Mr', 'Anyone', 'Madam', 'Dumbledore', 'Hogwarts', 'Hoggy', 'Teach', 'Ickle', 'Baron', 'Peeves', 'Draconis', 'Malfoy']
# 4
betterNer = ['Hagrid', 'Ravenclaw', 'Slytherin', 'Neville', 'Ron', 'Hermione', 'Hannah', 'Mandy', 'Bulstrode', 'Millicent', 'Dudley', 'Justin', 'Morag', 'Crabbe', 'Goyle', 'Patil', 'Albus', 'Lisa', 'Percy', 'Blaise', 'Mimsy', 'Seamus', 'Algie', 'Enid', 'Gran', 'Quirrell', 'Snape', 'Dumbledore', 'Hogwarts', 'Hoggy', 'Ickle', 'Draconis', 'Malfoy']

two = [x for x in checkNames if x not in actual]
three = [x for x in ner if x not in actual]
four = [x for x in betterNer if x not in actual]

goodTwo = [x for x in checkNames if x in actual]
goodThree = [x for x in ner if x in actual]
goodFour = [x for x in betterNer if x in actual]

# Score = Names Correct - Names overgeneralized

print("Score for Check Names: ")
print(len(goodTwo) - len(two))
print("Score for NER: ")
print(len(goodThree) - len(three))
print("Score for NER with word elimination: ")
print(len(goodFour) - len(four))




