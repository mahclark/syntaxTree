from random import randint
import syntaxTree

tree = syntaxTree.Tree()
tree.setRoot("Root", True, True)
tree.addNode("A", True, False).subText("cat")
tree.addNode("T [+PAST]", False, False).subText("jumped")
# tree.addNode("C", False, False).subText("the")

stree = syntaxTree.Tree()
stree.setRoot("SubRoot", True, True)
stree.addNode("A", True, False).subText("cat")
stree.addNode("T [+PAST]", False, False).subText("jumped")
stree.addNode("C", False, False).subText("the")

tree.addSubTree(stree)

tree.draw()

done = False
while not done:
	done = tree.loop()
	# if not tree.getComplete():
	# 	tree.addNode("?", randint(0,1), randint(0,1))
	# 	tree.draw()

syntaxTree.quit()