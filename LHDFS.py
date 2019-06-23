import syntaxTree
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_lg")
print("corpus loaded")
matcher = Matcher(nlp.vocab)
print("matcher loaded")

text = u"The cat saw me"
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

qdpList = []
for token in doc:
	if token.dep_ == "predet":
		if len(qdpList) > 0 and not qdpList[-1].getComplete():
			qdpList[-1].addNode("ti", False, False)

		streeQP = syntaxTree.Tree()
		streeQP.setRoot("QP", dpLeftBranching, True)
		streeQP.addNode("Q'",True,True)
		streeQP.addNode("Q",False,False).subText(token.text)
		print(streeQP)
		qdpList.append(streeQP)

	elif token.dep_ == "nsubj":

		streeDP = syntaxTree.Tree()
		streeDP.setRoot("DP", dpLeftBranching, True)
		streeDP.addNode("D'",True,True)
		if token.tag_ in ["DT", "PRP", "PRP$"]:
			streeDP.addNode("D", False, False).subText(token.text)
		elif token.pos_ in ["NN", "NNP", "NNPS", "NNS"]:
			streeDP.addNode("NP",False,True)
			streeDP.addNode("N'",False,True)
			streeDP.addNode("N",False,False).subText(token.text)

		if dpLeftBranching == True:
			streeDP.addNode("AP", False, False)
		else:
			streeDP.draw()
			streeDP.addNode("", False, False)

		if len(qdpList) > 0 and not qdpList[-1].getComplete():
			if True:#we dont wanna join them:
				qdpList[-1].addNode("ti", False, False)
				print(streeDP)
				qdpList.append(streeDP)
			else:
				qdpList[-1].addSubTree(streeDP)

		print(streeDP)
		qdpList.append(streeDP)
				


tree = syntaxTree.Tree()
tree.setRoot("CP",True,True)

addedDP = False
for token in doc:
	if token.tag_ in ["WDT", "WP", "WP$", "WRB"]:
		tree.addSubTree(streeDP)
		addedDP = True
		break

if not addedDP:
	tree.addNode("", False, False)

tree.addNode("C'", True, True)
tree.addNode("C [" + ("+" if token.tag_ in ["WDT", "WP", "WP$", "WRB"] else "-") + "WH Q]", False, False)
tree.addNode("TP", True, True)
if len(qdpList) > 0:
	tree.addSubTree(qdpList[-1])
tree.addNode("T’", True, True)

verbs = []
for token in doc:
	if token.dep_ == "nsubj":
		pass
	elif token.pos_ == "VERB":
		tree.addNode("T [" + ("+" if token.tag_ == "VBD" else "-") + "PAST]", False, False)
		tree.addNode("VP", True, True)
		tree.addNode("ti", False, False)
		tree.addNode("V'", True, True)
		verbs.append(token.text)
		if token.dep_ == "ROOT":
			tree.addNode("V", False, False).subText(token.text)

	elif token.tag_ in ["DT", "PRP", "PRP$"] :
		tree.addNode("DP",dpLeftBranching,True)
		tree.addNode("D'",True,True)
		tree.addNode("D", False, False).subText(token.text)

	elif token.pos_ == "NOUN" and token.dep_ == "dobj":
		tree.addNode("NP",False,True)
		tree.addNode("N'",False,True)
		tree.addNode("N",False,False).subText(token.text)

	else:
		print("intransitive VERB")
	

tree.draw()

fc = 0
done = False
while not done:
	fc += 1
	done = tree.loop() or fc > 60*600
syntaxTree.quit()
	