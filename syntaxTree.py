import pygame
import time
from math import sqrt
from random import randint

xSize, ySize = 600, 450
screen = pygame.display.set_mode((xSize, ySize), pygame.RESIZABLE)
pygame.display.set_caption("Tree")
pygame.init()

class Node():

    def __init__(self, parent, key, hasLeft, hasRight):
        self.parent = parent
        if parent != None:
            if parent.hasRight and parent.right == None:
                parent.right = self
            elif parent.hasLeft and parent.left == None:
                parent.left = self
            else:
                print("this shouldn't happen")

        self.key = key
        self.hasLeft = hasLeft
        self.hasRight = hasRight

    key = ""
    value = 0
    left = None
    right = None
    x = 0
    y = 0

class Tree():
    nodes = []
    complete = False
    root = None

    # def __init__(self):
    #     pass

    def setRoot(self, key, left, right):
        self.root = Node(None, key, left, right)
        return self.root

    def addNode(self, key, left, right):
        nextNode = getNext(self.root)
        node = Node(nextNode, key, left, right)
        self.complete = getNext(self.root) == None
        self.nodes.append(node)
        return node

    def draw(self):
        setPositions(self.root)
        screen.fill([255,255,255])
        drawTree(self.root)
        pygame.display.flip()


def getNext(node):
    if node.hasRight:
        if node.right == None:
            return node

        nextNode = getNext(node.right)
        if nextNode != None:
            return nextNode
        #else right be full
    
    if node.hasLeft:
        if node.left == None:
            return node

        nextNode = getNext(node.left)
        if nextNode != None:
            return nextNode
        #else both be full
    
    return None

# def getLevel(n):
#     if n == 0: return [root]

#     level = []
#     for parent in getLevel(n - 1):
#         if parent.left != None:
#             level.append(parent.left)
#         if parent.right != None:
#             level.append(parent.right)

#     return level

leaves = []
def getDepth(node):
    leftDepth, rightDepth = 0, 0
    if node.left != None:
        leftDepth = 1 + getDepth(node.left)
    if node.right != None:
        rightDepth = 1 + getDepth(node.right)

    if node.left == None and node.right == None:
        leaves.append(node)

    return max(leftDepth, rightDepth)
depth = 0

def getY(level):
    return 20 if depth == 0 else int((ySize - 40)*level/depth + 20)

def setPos(node, level):
    node.y = getY(level)
    if node.left != None and node.right != None:
        x = int((setPos(node.left, level + 1) + setPos(node.right, level + 1))/2)
    elif node.right != None:
        x = setPos(node.right, level + 1)
    elif node.left != None:
        x = setPos(node.left, level + 1)
    else:
        x = node.x

    node.x = x
    return x

def setPositions(root):
    global leaves, depth
    leaves = []
    depth = getDepth(root)

    for (n, leaf) in enumerate(leaves):
        leaf.x = int((n + 0.5)*xSize/len(leaves))

    setPos(root, 0)

def drawTree(node):
    if node.parent != None:
        pygame.draw.line(screen, [0,0,0], (node.x, node.y), (node.parent.x, node.parent.y), 2)

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render(str(node.key), 1, (0,0,0))
    screen.blit(label, (node.x + 10, node.y - 9))

    if node.left != None:
        drawTree(node.left)
    if node.right != None:
        drawTree(node.right)
    pygame.draw.circle(screen, [20,50,150], (node.x, node.y), 7)

    if node.hasLeft == False:
        label = myfont.render("x", 1, (0,0,0))
        screen.blit(label, (node.x - 15, node.y + 2))

    if node.hasRight == False:
        label = myfont.render("x", 1, (0,0,0))
        screen.blit(label, (node.x + 10, node.y + 2))

clock = pygame.time.Clock()
frameCount = 0
mouseHold = False
done = False

def loop(tree):
    global xSize, ySize
    # frameCount += 1
    done = False
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            xSize, ySize = event.dict['size']
            print(xSize)
            tree.draw()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseHold = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseHold = False

    pygame.display.flip()
    clock.tick(60)

    return done

def quit():
    pygame.quit()


if __name__ == "__main__":
    tree = Tree()
    tree.setRoot("R", True, True)
    tree.addNode("A", False, False)
    tree.addNode("B", False, False)
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

                # for node in nodes:
                #     sqx = (mx - node.x)**2
                #     sqy = (my - node.y)**2

                #     if sqrt(sqx + sqy) < 7:
                #         child = Node(node, "?", (node.left == None))

                # draw()

        # if not complete and frameCount % 1 == 0:
        #     addNode("", randint(0,1), randint(0,1))
        #     draw()

        pygame.display.flip()
        clock.tick(60)

    print("I quit")
    pygame.quit()