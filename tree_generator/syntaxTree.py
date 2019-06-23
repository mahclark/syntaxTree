import pygame
import time
from math import sqrt
from random import randint

class Node():

	parent = None
	tree = None
	text = ""
	sub = None
	value = 0
	left = None
	right = None
	x = 0
	y = 0

	def __init__(self, parent, text, hasLeft, hasRight):
		self.parent = parent
		if parent != None:
			if parent.hasLeft and parent.left == None:
				parent.left = self
			elif parent.hasRight and parent.right == None:
				parent.right = self
			else:
				raise Exception("*** Parent has no available children slots ***")

		self.text = str(text)
		self.hasLeft = hasLeft
		self.hasRight = hasRight

	def subText(self, sub):
		self.sub = str(sub)

def _getNext(node):
	if node.hasLeft:
		if node.left == None:
			return node

		nextNode = _getNext(node.left)
		if nextNode != None:
			return nextNode
		#else left be full

	if node.hasRight:
		if node.right == None:
			return node

		nextNode = _getNext(node.right)
		if nextNode != None:
			return nextNode
		#else both be full

	return None

class Tree():
	complete = False
	root = None
	leaves = []
	depth = 0
	xSize, ySize = 0,0

	def setRoot(self, text, left, right):
		self.root = Node(None, text, left, right)
		self.root.tree = self
		self.complete = _getNext(self.root) == None
		return self.root

	def addSubTree(self, subTree):
		if self.root == None:
			raise Exception("*** Must set root before adding subtree ***")
			return

		if self != self.root.tree:
			raise Exception("*** Cannot add to this subtree - add to the supertree ***")

		self._setTree(subTree.root)

		nextNode = _getNext(self.root)
		if nextNode == None:
			raise Exception("*** Cannot add subtree - tree is already complete ***")
			return
		subTree.root.parent = nextNode

		if nextNode.hasLeft and nextNode.left == None:
			nextNode.left = subTree.root
		elif nextNode.hasRight and nextNode.right == None:
			nextNode.right = subTree.root
		else:
			raise Exception("*** Parent has no available children slots ***")

		self.complete = _getNext(self.root) == None

	def addNode(self, text, left, right):
		if self.root == None:
			raise Exception("*** Must set root before adding nodes ***")
			return

		if self != self.root.tree:
			raise Exception("*** Cannot add to this subtree - add to the supertree ***")

		nextNode = _getNext(self.root)
		if nextNode == None:
			raise Exception("*** Cannot add subtree - tree is already complete ***")
			return

		node = Node(nextNode, text, left, right)
		node.tree = self
		self.complete = _getNext(self.root) == None
		return node

	def getComplete(self):
		return self.complete

	def _setTree(self, node):
		if node == None: return
		node.tree = self
		self._setTree(node.left)
		self._setTree(node.right)

	def _draw(self, surf, dots):
		if self.root == None:
			raise Exception("*** Must set root before drawing ***")
			return

		self.xSize, self.ySize = surf.get_size()

		self._setPositions(self.root)
		surf = self._drawTree(self.root, surf, dots)

		pygame.display.flip()

		return surf

	def _setPos(self, node, level):
		node.y = self._getY(level)
		if node.left != None and node.right != None:
			x = int((self._setPos(node.left, level + 1) + self._setPos(node.right, level + 1))/2)
		elif node.right != None:
			x = self._setPos(node.right, level + 1)
		elif node.left != None:
			x = self._setPos(node.left, level + 1)
		else:
			x = node.x

		node.x = x
		return x

	def _setPositions(self, root):
		self.leaves = []
		self.depth = self._getDepth(root)

		for (n, leaf) in enumerate(self.leaves):
			leaf.x = int((n + 0.5)*self.xSize/len(self.leaves))

		self._setPos(root, 0)

	def _getDepth(self, node):
		leftDepth, rightDepth = 0, 0
		if node.left != None:
			leftDepth = 1 + self._getDepth(node.left)
		if node.right != None:
			rightDepth = 1 + self._getDepth(node.right)

		if node.left == None and node.right == None:
			self.leaves.append(node)

		return max(leftDepth, rightDepth)

	def _getY(self, level):
		return 20 if self.depth == 0 else int((self.ySize - 40)*level/self.depth + 20)

	def _drawTree(self, node, surf, dots):
		if node.parent != None:
			pygame.draw.line(surf, [0,0,0], (node.x, node.y), (node.parent.x, node.parent.y), 2)

		fontSize = 16
		myfont = pygame.font.Font("AvenirLTStd-Book.otf", fontSize)
		title = myfont.render(node.text, 1, (0,0,0))

		if node.sub == None:
			width = 10 + myfont.size(node.text)[0]
			height = myfont.size(node.text)[1]
			textSurface = pygame.Surface((width, height))
			textSurface.fill([255,255,255])
		else:
			width = 10 + max(myfont.size(node.text)[0], myfont.size(node.sub)[0])
			height = fontSize + myfont.size(node.sub)[1]
			textSurface = pygame.Surface((width, height))
			textSurface.fill([255,255,255])
			sub = myfont.render(node.sub, 1, (0,0,0))
			textSurface.blit(sub, ((width - myfont.size(node.sub)[0])/2, fontSize))

		textSurface.blit(title, ((width - myfont.size(node.text)[0])/2, 0))

		if node.left != None:
			self._drawTree(node.left, surf, dots)
		if node.right != None:
			self._drawTree(node.right, surf, dots)

		surf.blit(textSurface, (node.x - width/2, node.y - height/2))

		if dots:
			if node.hasLeft == False:
				pygame.draw.circle(surf, [220,50,30], (node.x - int(width/2), node.y + 10), 3)

			if node.hasRight == False:
				pygame.draw.circle(surf, [220,50,30], (node.x + int(width/2), node.y + 10), 3)

		return surf

def quit():
	pygame.quit()

def tabController(names, selected):
	pad = 3

	btns = []
	poss = []

	totalWidth = pad
	font = pygame.font.Font("AvenirLTStd-Book.otf", 20)
	for name in names:
		totalWidth += font.size(name)[0] + 10 + pad

	back = pygame.Surface((totalWidth, 2*pad + 6 + max([font.size(name)[1] for name in names])))
	back.fill([0,0,0])

	cumWidth = pad
	for n, name in enumerate(names):
		lbl = font.render(name, 1, [255,255,255] if selected == n else [0,0,0])
		width, height = font.size(name)
		btn = pygame.Surface((width + 10, height + 6))
		btn.fill([0,0,0] if selected == n else [255,255,255])
		btn.blit(lbl, (5, 3))
		back.blit(btn, (cumWidth, pad))
		poss.append((cumWidth, pad))
		btns.append(btn)
		cumWidth += width + 10 + pad

	return (back, btns, poss)

def run(trees=[], timeOut=0, dots=True):
	if not isinstance(trees, list):
		trees = [trees]

	xSize, ySize = 600, 450
	screen = pygame.display.set_mode((xSize, ySize), pygame.RESIZABLE)
	pygame.display.set_caption("Tree")
	pygame.init()

	screen.fill([255,255,255])

	selected = None
	if len(trees) > 0:
		selected = 0

		tab, btns, btnsPos = tabController(["Tree {0}".format(i) for i in range(1, len(trees) + 1)], selected)
		if len(trees) == 1:
			tab = pygame.Surface((0,0))

		treeSpace = pygame.Surface((xSize, ySize - tab.get_size()[1]))
		treeSpace.fill([255,255,255])
		treeSpace = trees[selected]._draw(treeSpace, dots)

		screen.blit(treeSpace, (0, tab.get_size()[1]))
		tabPos = ((xSize - tab.get_size()[0])/2, 0)
		screen.blit(tab, tabPos)

	#----------------------Main Loop----------------------#

	clock = pygame.time.Clock()
	frameCount = 0
	mouseHold = False
	done = False
	while not done:
		frameCount += 1
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.VIDEORESIZE:
				screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
				screen.fill([255,255,255])
				xSize, ySize = event.dict['size']

				if selected != None:
					treeSpace = pygame.Surface((xSize, ySize - tab.get_size()[1]))
					treeSpace.fill([255,255,255])
					treeSpace = trees[selected]._draw(treeSpace, dots)

					screen.blit(treeSpace, (0, tab.get_size()[1]))
					tabPos = ((xSize - tab.get_size()[0])/2, 0)
					if len(trees) > 1: screen.blit(tab, tabPos)


			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseHold = True

				for n, btn in enumerate(btns):
					rect = pygame.Rect(tabPos[0] + btnsPos[n][0], tabPos[1] + btnsPos[n][1], btn.get_size()[0], btn.get_size()[1])
					if rect.collidepoint(mx, my):
						selected = n

						screen.fill([255,255,255])
						treeSpace.fill([255,255,255])
						treeSpace = trees[selected]._draw(treeSpace, dots)
						screen.blit(treeSpace, (0, tab.get_size()[1]))

						tab, btns, btnsPos = tabController(["Tree {0}".format(i) for i in range(1, len(trees) + 1)], selected)
						if len(trees) == 1:
							tab = pygame.Surface((0,0))
						screen.blit(tab, tabPos)

						break

			if event.type == pygame.MOUSEBUTTONUP:
				mouseHold = False

		if timeOut > 0 and frameCount > timeOut*60:
			done = True

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	tree1 = Tree()
	tree1.setRoot("Tree 1", True, True)
	tree1.addNode("A", False, True)
	tree1.addNode("B", False, False).subText("Sub Text")
	tree1.addNode("C", False, False)


	tree2 = Tree()
	tree2.setRoot("Tree 2", True, True)
	tree2.addNode("A", False, False)
	tree2.addNode("B", False, True)
	tree2.addNode("C", False, False)


	tree3 = Tree()
	tree3.setRoot("Tree 3", False, False)

	run([tree1, tree2, tree3], 60, False)