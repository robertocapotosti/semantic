'''
I read a very interesting article
https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python
From there I took the function jaccard_similarity(x,y)
Although Spacy uses Word2Vec which is more complex and efficient than jaccard_similarity,
comparing the two it helped me to better understand the subject and how Spacy works when
it comes to compare two sentences.
'''

#=== IMPORT SECTION ===
import spacy

#=== FUNCTION SECTION ===
# returns the jaccard similarity between two lists
# taken from the aricle mentioned above and the GitHub repository
# https://gist.github.com/Aditya1001001/0dcb858001998d042e453425ca46eb15#file-jaccard_similarity-py
def jaccard_similarity(x,y):
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

# print a matrix of words and their similarity
def word_similarity(words_str1, words_str2 = ""):
	# variable declarations
	words1 = []
	words2 = []
	tokens1 = object()
	tokens2 = object()
	token1 = object()
	token2 = object()
	pad1 = 0
	pad2 = 0

	if words_str2 == "":
		words_str2 = words_str1
	words1 = words_str1.split()
	words2 = words_str2.split()
	# take the tokens
	tokens1 = nlp(words_str1)
	tokens2 = nlp(words_str2)
	# set the printing pad as the lenght of the longest word + 2
	pad1 = len(max(words1, key = len))+2
	pad2 = len(max(words2, key = len))+2
	if pad2 < 6:
		pad2 = 6
	# print the header
	print("\nSimilarity between words")
	# print the words as column 
	print(" "*pad1,"".join([ i.text.ljust(pad2) for i in tokens2]))
	# for each token in the row
	for token1 in tokens1:
		# print the word used as a row 
		print(token1.text.ljust(pad1), end=" ")
		# for each token, second level
		for token2 in tokens2:
			sim_score = token1.similarity(token2)
			# print the similarity, rounded and padded
			print(str(round(sim_score,2)).ljust(pad2), end="")
		print()
	input("------  Press ENTER ---------")

#==== MAIN SECTION =====
nlp = spacy.load('en_core_web_md')

# example 1 from the HyperionDev T38 PDF
word_similarity('cat apple monkey banana ')
'''NOTES
An interpretation of the results could be:
- cat and monkey are both mammals
- apple and banana are both fuits
- monkey might like banana
'''

# example 1 from the HyperionDev T38 PDF with different words
word_similarity('dog meat dolphin fish ')
'''NOTES
An interpretation of the results could be:
- dog and dolphin are both mammals but not very similar
- meat and fish are both food
- dolphin might prefer fish to meat as a food
- dolphin might be similiar to fish cosidering they live in the same environment
'''

# example 2 from the HyperionDev T38 PDF
sentence_to_compare = "Why is my cat on the car"
sentences = ["where did my dog go",
"Hello, there is my car",
"I\'ve lost my car in my car",
"I\'d like my boat back",
"I will name my dog Diana"]
print("\nSentences similarity")
print("Sentence to be tested: ",sentence_to_compare)
model_sentence = nlp(sentence_to_compare)
for i, sentence in enumerate(sentences):
	similarity = nlp(sentence).similarity(model_sentence)
	print(i, " - " + sentence + " - similarity", round(similarity,2),
		"- jaccard", round(jaccard_similarity(sentence_to_compare, sentence),2))
input("------  Press ENTER ---------")
'''NOTES
All sencences seem having similarities:
sentence 1 - 0.63 - question of "my dog" and "my cat"
sentence 2 - 0.80 - car in common
sentence 3 - 0.68 - less than the sentence 2 because ("my cat" not = "my car") + ("my car" almost = "the car")
sentence 4 - 0.56 - lowest score because boat and car are just both means of transportation
sentence 5 - 0.65 - I was expecting a higher score which has been probably affected by "name" "Diana" 
'''

# Printing the matrix of the similarities of the words that are contained in
# the main sentence: "Why is my cat on the car"
# and the sentence n.5: "I will name my dog Diana"
print("\nTesting the sentences word by word")
word_similarity(sentence_to_compare, sentences[4])

'''
NOTES about the Example.py
When I tried to use the model en_core_web_sm, I had this warning:

"UserWarning: [W007] The model you're using has no word vectors loaded,
so the result of the Doc.similarity method will be based on the tagger,
parser and NER, which may not give useful similarity judgements.
This may happen if you're using one of the small models, e.g. `en_core_web_sm`,
which don't ship with word vectors and only use context-sensitive tensors.
You can always add your own word vectors, or use one of the larger models instead if available.
  print(token.similarity(token_))"

I also tried on this source and indeed the results were much less accurate and
more aligned to the jaccard algorithm
'''