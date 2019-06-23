import syntaxTree

tree = syntaxTree.Tree()
tree.setRoot("CP",True,True)

fixedLabelsR = ["C'", "TP", "T’"]
for label in fixedLabelsR:
    tree.addNode(label, True, True)

fixedLabelsL = ["VP", "T", "DP", "C", ""]
for label in fixedLabelsL:
    tree.addNode(label, False, False)

tree.draw()

done = False
while not done:
	done = tree.loop()