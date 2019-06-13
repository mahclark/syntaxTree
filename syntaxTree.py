import pygame
import time
from math import sqrt
from random import randint

class Node():

    def __init__(self, parent, text, hasLeft, hasRight):
        self.parent = parent
        if parent != None:
            if parent.hasRight and parent.right == None:
                parent.right = self
            elif parent.hasLeft and parent.left == None:
                parent.left = self
            else:
                print("this shouldn't happen")

        self.text = text
        self.hasLeft = hasLeft
        self.hasRight = hasRight

    def addSubText(self, subText):
        self.subText = subText

    text = ""
    subText = None
    value = 0
    left = None
    right = None
    x = 0
    y = 0

def _getNext(node):
    if node.hasRight:
        if node.right == None:
            return node

        nextNode = _getNext(node.right)
        if nextNode != None:
            return nextNode
        #else right be full
    
    if node.hasLeft:
        if node.left == None:
            return node

        nextNode = _getNext(node.left)
        if nextNode != None:
            return nextNode
        #else both be full

    return None

class Tree():
    nodes = []
    complete = False
    root = None
    leaves = []
    depth = 0

    xSize, ySize = 600, 450
    screen = None
    clock = pygame.time.Clock()
    frameCount = 0

    def __init__(self):
        self.screen = pygame.display.set_mode((self.xSize, self.ySize), pygame.RESIZABLE)
        pygame.display.set_caption("Tree")
        pygame.init()

    def setRoot(self, text, left, right):
        self.root = Node(None, text, left, right)
        return self.root

    def addNode(self, text, left, right):
        nextNode = _getNext(self.root)
        node = Node(nextNode, text, left, right)
        self.complete = _getNext(self.root) == None
        self.nodes.append(node)
        return node

    def draw(self):
        self._setPositions(self.root)
        self.screen.fill([255,255,255])
        self._drawTree(self.root)
        pygame.display.flip()

    def getComplete(self):
        return self.complete

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

    def _drawTree(self, node):
        if node.parent != None:
            pygame.draw.line(self.screen, [0,0,0], (node.x, node.y), (node.parent.x, node.parent.y), 2)

        myfont = pygame.font.SysFont("monospace", 15)
        title = myfont.render(node.text, 1, (0,0,0))

        if node.subText == None:
            width = 10 + myfont.size(node.text)[0]
            height = myfont.size(node.text)[1]
            textSurface = pygame.Surface((width, height))
            textSurface.fill([255,255,255])
        else:
            width = 10 + max(myfont.size(node.text)[0], myfont.size(node.subText)[0])
            height = 15 + myfont.size(node.subText)[1]
            textSurface = pygame.Surface((width, height))
            textSurface.fill([255,255,255])
            sub = myfont.render(node.subText, 1, (0,0,0))
            textSurface.blit(sub, ((width - myfont.size(node.subText)[0])/2, 15))

        textSurface.blit(title, ((width - myfont.size(node.text)[0])/2, 0))

        if node.left != None:
            self._drawTree(node.left)
        if node.right != None:
            self._drawTree(node.right)
        # pygame.draw.circle(self.screen, [20,50,150], (node.x, node.y), 7)

        if node.hasLeft == False:
            label = myfont.render("x", 1, (0,0,0))
            self.screen.blit(label, (node.x - 15, node.y + 2))

        if node.hasRight == False:
            label = myfont.render("x", 1, (0,0,0))
            self.screen.blit(label, (node.x + 10, node.y + 2))

        self.screen.blit(textSurface, (node.x - width/2, node.y - height/2 - 5))

    def loop(self):
        self.frameCount += 1
        done = False
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.xSize, self.ySize = event.dict['size']
                self.draw()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHold = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False

        pygame.display.flip()
        self.clock.tick(60)

        return done

def quit(self):
    pygame.quit()


if __name__ == "__main__":
    tree = Tree()
    tree.setRoot("The Root", True, True)
    tree.addNode("A node", False, False).addSubText("The Cat")
    tree.addNode("B node", False, False)
    tree.draw()

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
                xSize, ySize = event.dict['size']

                tree.draw()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHold = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseHold = False

        pygame.display.flip()
        clock.tick(60)

    print("I quit")
    pygame.quit()