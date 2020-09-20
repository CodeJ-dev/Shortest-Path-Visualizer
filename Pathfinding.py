# Jay Doshi
# Date Finished: 5/20/2020
# Program to simulate the shortest path between two cells on a grid

import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# Pygame 
WIDTH = 400
HEIGHT = 400
BLOCKSIZE = 20
FPS = 50
WAIT = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
FAIL = -100000
MAX = 100000
H = HEIGHT // BLOCKSIZE
W = WIDTH // BLOCKSIZE

# Object that stores information of a specific cell within grid
class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.marked = False
        self.rect = None
        self.dist = MAX
        self.parentX = -1
        self.parentY = -1

    def reset(self):
        self.dist = MAX
        self.parentX = -1
        self.parentY = -1
        self.marked = False
        

# Priorties the next smallest value in the queue to the front for dequeue
# Implemented using a heap
class PriorityQueue(object):
    
    def __init__(self):
        self.array = []
        self.size = 0
        
    def swap(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

    def isEmpty(self):
        return self.size == 0

    def getParent(self, child):
        return (child - 1) // 2

    def percolateUp(self, child):
        parent = self.getParent(child)
        while (self.array[child].dist < self.array[parent].dist):
            swap(child, parent)
            child = parent
            parent = self.getParent(child)

    def put(self, key):
        if (len(self.array) == self.size):
            self.array.append(key)
        else:
            self.array[self.size] = key
        self.size += 1
        self.percolateUp(self.size - 1)

    def smallerChild(self, parent):
        lc = (parent * 2 + 1)
        if (parent * 2 + 1 >= self.size):
            lc = parent
        rc = parent * 2 + 2
        if (parent * 2 + 2 >= self.size):
            rc = parent
        if (self.array[lc].dist >= self.array[rc].dist):
            return rc
        return lc

    def percolateDown(self, parent):
        child = self.smallerChild(parent)
        while (self.array[parent].dist > self.array[child].dist):
            self.swap(parent, child)
            parent = child
            child = self.smallerChild(parent)

    def get(self):
        if (self.isEmpty()):
            return FAIL

        val = self.array[0]

        self.size -= 1
        if (self.size == 0):
            return val

        self.array[0] = self.array[self.size]
        self.percolateDown(0)

        return val

# Stores the edge between two cells 
class Edge(object):
    def __init__(self, x, y, w):
        self.start = x
        self.end = y
        self.weight = w
        
# Graph algorithms    
def createGraph(n, m):
    return [[Cell(y,x) for x in range(m)] for y in range(n)]

def isValid(n, m, x, y):
    return x >= 0 and x < n and y >= 0 and y < m

def printGraph(graph):
    for i in graph:
        for x in i:
            print("(", x.dist, end = ")")
        print()
        
def findParents(graph, s):
    while (graph[s.x][s.y].parentX != -1 and graph[s.x][s.y].parentY != -1):
        color(s.x, s.y, grid, BLUE, WAIT)
        x = s.x
        y = s.y
        s.x = graph[x][y].parentX
        s.y = graph[x][y].parentY
    color(s.x, s.y, graph, BLUE, WAIT)

def setEdges(graph):
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    edges = [[[] for y in range(len(graph[x]))] for x in range(len(graph))]

    for r in range(len(graph)):
        for c in range(len(graph[r])):
            e = []
            for i in range(4):
                x = r + dx[i]
                y = c + dy[i]
                if (isValid(len(graph), len(graph[r]), x, y)):
                    edges[r][c].append(Edge(Cell(r,c), Cell(x,y), 1))
    return edges

def color(x, y, grid, colorType, delay):
    rect = grid[x][y].rect
    pygame.time.delay(delay)
    pygame.draw.rect(screen, colorType, rect, 0)
    pygame.draw.rect(screen, WHITE, rect, 1)
    pygame.display.update()

def bfs(graph, start, end):
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    queue = []
    visited = [[False for x in range(len(graph[y]))] for y in range(len(graph))] 
    visited[start.x][start.y] = True
    queue.append(Cell(start.x,start.y))
    while (queue):
        s = queue.pop(0)

        # Add some draw color to a specfic cell in graph on grid
        color(s.x, s.y, grid, RED, WAIT)
        
        if (s.x == end.x and s.y == end.y):
            return True

        for i in range(4):

            x = dx[i] + s.x
            y = dy[i] + s.y
                  
            if (isValid(len(graph), len(graph[0]), x, y) and not visited[x][y] and not grid[x][y].marked):
                graph[x][y].parentX = s.x
                graph[x][y].parentY = s.y
                visited[x][y] = True
                queue.append(Cell(x,y))
                 
    return False


def dijkstra(graph, start, end):
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    
    queue = PriorityQueue()
    graph[start.x][start.y].dist = 0
    queue.put(graph[start.x][start.y])
    
    while (not queue.isEmpty()):
        s = queue.get()
        s = graph[s.x][s.y]
        for i in range(4):
            x = dx[i] + s.x
            y = dy[i] + s.y
                  
            if (isValid(len(graph), len(graph[0]), x, y) and not grid[x][y].marked):
                t = graph[x][y]
                if (s.dist + 1 < t.dist):
                    graph[t.x][t.y].dist = s.dist + 1
                    graph[t.x][t.y].parentX = s.x
                    graph[t.x][t.y].parentY = s.y
                    queue.put(graph[t.x][t.y])
                    color(t.x, t.y, grid, RED, WAIT)

    if (graph[end.x][end.y].parentX == -1 and graph[end.x][end.y].parentY == -1 and (start.x != end.x or start.y != end.y)):
        return False
    
    return True
        
# start Pygame and make window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shortest Path")
clock = pygame.time.Clock()

 
def onsubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()

def onsubmitreset():
    window1.quit()
    window1.destroy()
  
def drawStartGrid():
    screen.fill(BLACK)
    for x in range(W):
        for y in range(H):
            rect = pygame.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
            grid[x][y].rect = rect
            pygame.draw.rect(screen, WHITE, rect, 1)

def resetGrid():
    screen.fill(BLACK)
    for x in range(W):
        for y in range(H):
            rect = grid[x][y].rect
            pygame.draw.rect(screen, WHITE, rect, 1)
            grid[x][y].reset()


def getCell(pos):
    if (pos[0] > WIDTH or pos[0] < 0 or pos[1] > HEIGHT or pos[1] < 0):
        return [-1]
    if (pos[0] % BLOCKSIZE == 0 or pos[1] % BLOCKSIZE == 1):
        return [-1]
    x = pos[0] // BLOCKSIZE
    y = pos[1] // BLOCKSIZE
    return [x,y]

# Game loop
run = True
hasStarted = True

while run:
    
    for event in pygame.event.get():
        if (event.type == 'pygame.QUIT'):
            run = False

    if not hasStarted:
        continue

    grid = createGraph(H, W)
        
    if hasStarted:
        drawStartGrid()
        pygame.display.update()

    mark = True
    while mark:
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                s = getCell(pos)
                if (s[0] == -1):
                    continue
                grid[s[0]][s[1]].marked = True
                color(s[0], s[1], grid, WHITE, 3)
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                mark = False
                break


    pygame.display.update()

    start = None
    end = None

    # Tkinter
    window = Tk()
    label = Label(window, text='Start(x,y): ')
    startBox = Entry(window)
    label1 = Label(window, text='End(x,y): ')
    endBox = Entry(window)
    var1 = IntVar()
    var2 = IntVar()
    BFS = ttk.Checkbutton(window, text='BFS :', onvalue=1, offvalue=0, variable=var1)
    dij = ttk.Checkbutton(window, text='Dijkstra :', onvalue=1, offvalue=0, variable=var2)
    submit = Button(window, text='Submit', command=onsubmit)
    
    BFS.grid(columnspan=2, row=2)
    dij.grid(columnspan=2, row=3)
    submit.grid(columnspan=2, row=4)
    label1.grid(row=1, pady=3)
    endBox.grid(row=1, column=1, pady=3)
    startBox.grid(row=0, column=1, pady=3)
    label.grid(row=0, pady=3)

    window.update()
    mainloop()
    
    if (var2.get() == 1 and dijkstra(grid, start, end)):
       findParents(grid, end)

    if (var1.get() == 1 and bfs(grid, start, end)):
      findParents(grid, end)

    # Tkinter
    window1 = Tk()
    var3 = IntVar()
    reset = ttk.Checkbutton(window1, text='Reset :', onvalue=1, offvalue=0, variable=var3)
    submit1 = Button(window1, text='Submit', command=onsubmitreset)

    reset.grid(columnspan=1, row=1)
    submit1.grid(columnspan=2, row=2)

    window1.update()
    mainloop()

    pygame.display.update()
    
    hasStarted = False
    
    if var3.get() == 1:
        resetGrid()
        hasStarted = True
        pygame.display.update()
    else:
        hasStarted = False
     
    pygame.display.update()
    
pygame.quit()
