import syntaxTree

tree = syntaxTree.Tree()
tree.setRoot("Root", True, True)
tree.addNode("A", True, False)
tree.addNode("B", False, False)
tree.addNode("C", False, False)

tree.draw()

done = False
while not done:
	done = syntaxTree.loop(tree)