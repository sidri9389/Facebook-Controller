import nltk
from nltk.corpus import wordnet 


import textdistance
import sys

command_file = 'command.txt'

command = open(command_file, 'r').read()

command = command.lower().split()
print(command)


#word = sys.argv[1:]

#nltk.download()

'''

distance = textdistance.Levenshtein(external = False)

print(distance(word[0],word[1]))

if len(word) > 1:
	result = ''
	for w in word:
		result += w
		result += '_'
	print(result)
	word = result

synonyms = []


word = 'start'
print("Synonims for " + word)
for syn in wordnet.synsets(word):
    for lm in syn.lemmas():
             synonyms.append(lm.name())
print (set(synonyms))

'''