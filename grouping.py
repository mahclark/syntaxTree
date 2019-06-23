from tree_generator import syntaxTree
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_lg")
print("corpus loaded")
matcher = Matcher(nlp.vocab)
print("matcher loaded")

def anyIn(xs, ys):
	for x in xs:
		if x in ys:
			return True
	return False

text = u"If I were to go"

doc = nlp(text)
for token in doc:
	print (token.text, token.pos_, token.tag_, token.dep_)
print("parsed")

splitText = text.split(' ')

groups = []

for token in doc:
	if len(groups) > 0 and (token.dep_ == "cc" or groups[-1][-1].dep_ in ["det", "acl", "advcl", "advmod", "amod", "appos","meta", "neg", "nn", "nounmod", "npmod", "nummod", "poss", "prep", "quantmod", "cc", "cop", "aux", "auxpass"]):
		groups [-1].append(token)
	else:
		groups.append([token])

print(groups)

def makeClause(whGroup, subjGroup):
	subtree = syntaxTree.Tree()
	subtree.setRoot("CP",True, True)
	subtree.addNode("TO DO", False, False)
	subtree.addNode("C'", True, True)
	subtree.addNode("C [" + ("+" if whGroup != None and anyIn(["WDT", "WP", "WP$", "WRB"], [token.tag_ for token in whGroup])  else "-") + "WH Q]", False, False)
	subtree.addNode("TP", True, True)
	subtree.addNode("subj TO DO", False, False).subText(" ".join([token.text for token in subjGroup]))
	return subtree

	if anyIn(["DET", "NOUN", "PRON"], [token.pos_ for token in group]):
		dpLeftBranching = False
		subtree.setRoot("DP", dpLeftBranching, True)
		subtree.addNode("D'", True, True)

		for token in group:

			subText = None
			for token in group:
				if token.tag_ in ["DT", "PRP", "PRP$"]:
					subText = token.text

			if token.tag_ in ["DT", "PRP", "PRP$"]:
				subtree.addNode("D", False, False).subText(token.text)

				for n, token in enumerate(group):
					if token.tag_ in ["DT", "PRP", "PRP$"]:
						detIndex = n
						break

				if len(group) > 1 and group[detIndex + 1] in ["NN", "NNP", "NNPS", "NNS"]:

					subText = None
					for token in group:
						if token.pos_ in ["NN", "NNP", "NNPS", "NNS"]:
							subText = token.text

					subtree.addNode("NP",False,True)
					subtree.addNode("N'",False,True)
					subtree.addNode("N",False,False).subText(token.text)

				else:
					subtree.addNode("", False, False)

			elif token.pos_ in ["NN", "NNP", "NNPS", "NNS"]:

					subText = None
					for token in group:
						if token.pos_ in ["NN", "NNP", "NNPS", "NNS"]:
							subText = token.text

					subtree.addNode("D", False, False).subText("")
					subtree.addNode("NP",False,True)
					subtree.addNode("N'",False,True)
					subtree.addNode("N",False,False).subText(token.text)

	return subtree

whGroup = None
for group in groups:
	if anyIn(["WDT", "WP", "WP$", "WRB"], [token.tag_ for token in group]):
		whGroup = group
		break

subjGroup = None
for group in groups:
	if "nsubj" in [token.dep_ for token in group]:
		subjGroup = group
		break

tree = syntaxTree.Tree()
tree = makeClause(whGroup, subjGroup)
# tree.setRoot("CP",True,True)

# if tree.root.left == None:
# 	tree.addNode("", False, False)

# tree.addNode("C'", True, True)
# tree.addNode("C [" + ("+" if token.tag_ in ["WDT", "WP", "WP$", "WRB"] else "-") + "WH Q]", False, False)
# tree.addNode("TP", True, True)
# if len(qdpList) > 0:
# 	tree.addSubTree(qdpList[-1])

def getNoSpaces(node):
	a, b = 0, 0
	if node.hasRight:
		if node.right == None:
			a = 1
		else:
			a = getNoSpaces(node.right)
	if node.hasLeft:
		if node.left == None:
			b = 1
		else:
			b = getNoSpaces(node.left)

	return a + b

def makeSpecTP():
	dp = syntaxTree.Tree()
	dp.setRoot("TODO: DP", False, False)
	return dp 

def makeBlock(group):
	subtree = syntaxTree.Tree()
	

	if "VERB" in [token.pos_ for token in group]:
		try:
			subtree.setRoot("x", True, True)

			subText = None
			for token in group:
				if token.dep_ in ["aux", "auxpass"]:
					subText = token.text

			print(group)
			for token in group:
				print(token, token.dep_, token.tag_)
				if token.dep_ in ["aux", "auxpass"]:
					subtree.addNode("T'", True, True)
					subtree.addNode("T [" + ("+" if "VBD" in [token.tag_ for token in group] else "-") + "PAST]", False, False).subText(subText)

				elif token.dep_ == "ROOT" and token.text == "were":
					print("subjunctive")
					subtree.addNode("T [" + ("+" if token.tag_ == "VBD" else "-") + "PAST]", False, False).subText(token)

				elif token.tag_ in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] and token == group[0]:
							subtree.addNode("T [" + ("+" if token.tag_ == "VBD" else "-") + "PAST]", False, False)
							subtree.addNode("VP", True, True)
							subtree.addNode("ti", False, False)
							subtree.addNode("V'", True, True)
							subtree.addNode("V", False, False).subText(token.text)
							subtree.addNode("ti", False, False)


				elif token.tag_ in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]and token != group[0]:
							subtree.addNode("VP", True, True)
							subtree.addNode("ti", False, False)
							subtree.addNode("V'", True, True)
							subtree.addNode("V", False, False).subText(token.text)
							subtree.addNode("ti", False, False)

			

		except:
			print("complete:", subtree.getComplete())
			subtree.setRoot("Verb Failed", False, True)
			print("complete:", subtree.getComplete())

	elif "predet" in [token.dep_ for token in group]:
		subtree.setRoot("QP", False, True)
		subtree.addNode("Q'", True, False)

		for token in group:
			if token.dep_ == "predet":
				subtree.addNode("Q", False, False).subText(token.text)

		for n, token in enumerate(group):
			if token.dep_ == "predet":
				predetIndex = n
				break

		if len(group) >= predetIndex and group[predetIndex + 1].pos_ in ["DET", "NOUN", "PRON"]:
			subtree.addSubTree(makeDP)
		elif len(group) >= predetIndex and group[predetIndex + 1].pos_ == "ADJ":
			subtree.addSubTree(makeAP)
		else:
			subtree.addNode("", False, False)

	elif anyIn(["acl", "amod", "advcl", "advmod", "acomp"], [token.dep_ for token in group]):
		subtree.setRoot("AP", True, True)
		subtree.addNode("A'", True, True)

		subText = None
		for token in group:
			if token.dep_ in ["acl", "amod", "advcl", "advmod", "acomp"]:
				subText = token.text

		subtree.addNode("A", False, False).subText(token.text)

		subText = None
		for token in group:
			if token.dep_ in ["acl", "amod", "advcl", "advmod", "acomp"]:
				subText = token.text

		if anyIn(["acl", "amod", "advcl", "advmod", "acomp"], [token.dep_ for token in group]):
			subtree.setRoot("AP", False, True)
			subtree.addNode("A'", True, True)
			subtree.addNode("A", False, False).subText(token.text)

		elif anyIn(["DET", "NOUN", "PRON"], [token.pos_ for token in group]):
			subtree.addSubTree(makeDP)

		else:
			subtree.addNode("", False, False)

	# syntaxTree.run(subtree, 60*30)

	# assert subtree.complete == False

	if subtree.root != None:
		assert getNoSpaces(subtree.root) == 1

		current = subtree.root
		while current.right != None:
			current = current.right

		assert current.hasRight

	print("made a block")
	return subtree

for group in groups:
	block = makeBlock(group)
	if block.root != None:
		tree.addSubTree(block)
syntaxTree.run(tree, 60)
# tree.draw()

# fc = 0
# done = False
# while not done:
# 	fc += 1
# 	done = tree.loop() or fc > 60*600
# syntaxTree.quit()
