import syntaxTree
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_lg")
print("corpus loaded")
matcher = Matcher(nlp.vocab)
print("matcher loaded")

text = (u"I saw a cat")
doc = nlp(text)
for token in doc:
	print (token.text, token.pos_, token.tag_, token.dep_)
print("parsed")
#text = (u"[CP[TP [DP I] [VP SAW [DP A CAT]]]]")

# patternDP = [{"TEXT": "DP"}]
# matcher.add("DP", None, patternDP)
# doc = nlp(text)
# matches = matcher(doc)
dpLeftBranching = False

streesubj = syntaxTree.Tree()
streeDP = syntaxTree.Tree()
streeQP = syntaxTree.Tree()

for token in doc:
	if token.dep_ == "predet":
		streeQP.setRoot("QP", dpLeftBranching, True)
		streeQP.addNode("Q'",True,True)
		streeQP.addNode("Q",False,False).subText(token.text)

	elif token.dep_ == "det":
		streeDP.setRoot("DP", dpLeftBranching, True)
		streeDP.addNode("D", False, False).subText(token.text)

	elif token.dep_ == "nsubj":
		streeDP.setRoot("DP", dpLeftBranching, True)
		streeDP.addNode("D'",True,True)
		if token.pos_ == "PRON":
			streeDP.addNode("D", False, False).subText(token.text)
		elif token.pos_ == "NOUN":
			streeDP.addNode("NP",False,True)
			streeDP.addNode("N'",False,True)
			streeDP.addNode("N",False,False).subText(token.text)

		if dpLeftBranching == True:
			streeDP.addNode("AP", False, False)
		else:
			streeDP.addNode("", False, False)

tree = syntaxTree.Tree()
tree.setRoot("CP",True,True)

fixedLabelsR = ["C'", "TP", "T’"]
for label in fixedLabelsR:
    tree.addNode(label, True, True)

verbs = []
for token in doc:
	#make headings
	if token.pos_ == "VERB":
		tree.addNode("VP", True, True)
		tree.addNode("V'", True, True)
		verbs.append(token.text)


	elif token.pos_ == "NOUN" and token.dep_ == "dobj":
		tree.addNode("DP",dpLeftBranching,True)
		tree.addNode("D'",True,True)
		tree.addNode("NP",False,True)
		tree.addNode("N'",False,True)
		tree.addNode("N",False,False).subText(token.text)

	else:
		# tree.addNode("",False,False)
		print("intransitive VERB")
	

for token in reversed(doc):
	#fill in left branches

	if token.dep_ == "ROOT":
		tree.addNode("V", False, False).subText(token.text)
		tree.addNode("ti", False, False)


	elif token.dep_ == "det":
		tree.addNode("D", False, False).subText(token.text)

	# elif token.pos_ == "NOUN" and token.dep_ == "nsubj":
	# 	tree.addNode("DP",False,True)
	# 	tree.addNode("D'",True,True)
	# 	tree.addNode("NP",False,True)
	# 	tree.addNode("N'",False,True)
	# 	tree.addNode("N",False,False).subText(token.text)

tree.addNode("T [" + ("+" if token.tag_ == "VBD" else "-") + "PAST]", False, False)

if streeQP.root == None:
	tree.addSubTree(streeDP)
elif streeDP.root == None:
	srteeQP.addNode("ti", False, False)
	tree.addSubTree(streeQP)
else:
	streeQP.addSubTree(streeDP)
	tree.addSubTree(streeQP)

tree.addNode("C", False, False)
tree.addNode("", False, False)
# if token.pos_== "DET":
# 		tree.addNode("D",False,False)

	# patternDP = [{token.pos_: "NOUN"}, {token.dep_: "obj"}]
	# matcher.add("DP", None, patternDP)
	# matches = matcher(doc)
	# print("noun and obj:", patternDP)
	# for match in matches:
	# 	print(match)
	# if patternDP[0]:


# fixedLabelsL = ["T [" + ("+" if token.tag_ == "VBD" else "-") + "PAST]", "DP", "C", ""]
# for label in fixedLabelsL:
#     tree.addNode(label, False, False)


tree.draw()

fc = 0
done = False
while not done:
	fc += 1
	done = tree.loop() or fc > 60*600
syntaxTree.quit()
	