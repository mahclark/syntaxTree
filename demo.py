from random import randint
import syntaxTree

stree = syntaxTree.Tree()
stree.setRoot("SubRoot", True, True)
stree.addNode("A", True, False).subText("cat")
stree.addNode("T [+PAST]", False, False).subText("jumped")
stree.addNode("C", False, False).subText("the")

tree = syntaxTree.Tree()
tree.setRoot(200, True, True)
tree.addNode("A", True, False).subText("cat")
tree.addNode("T [+PAST]", False, False).subText("jumped")
# tree.addNode("C", False, False).subText("the")

tree.addSubTree(stree)

syntaxTree.run(tree, 60)