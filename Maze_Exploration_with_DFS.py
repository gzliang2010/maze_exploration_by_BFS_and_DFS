import turtle
from stack import Stack
from Graph import *

PART_OF_PATH = ' '
OBSTACLE = '+'
START = 'S'

class Maze:
	def __init__(self, mazeFileName):
		self.mazeList = []
		start_x = 0
		start_y =0
		exit_x = 0
		exit_y = 0
		myfile = open(mazeFileName, 'r')
		for row, line in enumerate(myfile):
			for col, ch in enumerate(line):
				if ch == START:
					start_y = row
					start_x = col
			self.mazeList.append(line)

		self.start_x = start_x
		self.start_y = start_y
		self.rows = row +1
		self.cols = col +1

		for row, line in enumerate(self.mazeList):
			for col, ch in enumerate(line):
				if self.isExit(ch, col, row):
					self.exit_x = col
					self.exit_y = row

		self.t = turtle.Turtle()
		self.t.shape('turtle')
		self.mw = turtle.Screen()
		self.mw.setworldcoordinates(-1, -1, self.cols+1, self.rows+1)

	def drawMaze(self):
		self.t.speed(40)
		for i in range(self.rows):
			for j in range(self.cols):
				if self.mazeList[i][j] == OBSTACLE:
					self.drawRect(j,i, 'grey')
		self.t.up()
		self.t.goto(self.start_x, self.start_y)
		self.t.color('black')
		self.t.fillcolor('blue')

	def drawRect(self, x, y, color = 'grey'):
		self.t.up()
		self.t.goto(x-0.5, y-0.5)
		self.t.fillcolor(color)
		self.t.begin_fill()
		self.t.down()
		self.t.setheading(0)
		for i in range(4):
			self.t.forward(1)
			self.t.left(90)
		self.t.end_fill()

	def moveTurtle(self, x, y):
		self.t.up()
		self.t.goto(x,y)

	def isExit(self, ch, x, y):
		if ch == PART_OF_PATH and (x == 0 or x == self.cols - 1\
			or y == 0 or y == self.rows - 1):
			return True 
		else:
			return False


def main():
	maze = Maze('MazeFile.txt')
	maze.drawMaze()
	#Build a graph for the maze

	mazeGraph = Graph()
	for i in range(maze.rows):
		for j in range(maze.cols):
			if maze.mazeList[i][j] == PART_OF_PATH or maze.mazeList[i][j] == START:
				mazeGraph.addVertex((i+1)*maze.cols+j+1)

	for ver in mazeGraph.vertList:     #ver is the key
		if ver-1 in mazeGraph.vertList:
			mazeGraph.addEdge(ver, ver-1)
		elif ver+1 in mazeGraph.vertList:
			mazeGraph.addEdge(ver, ver+1)
		elif ver+maze.cols in mazeGraph.vertList:
			mazeGraph.addEdge(ver, ver+maze.cols)
		elif ver-maze.cols in mazeGraph.vertList:
			mazeGraph.addEdge(ver, ver-maze.cols)

	#DFS of the graph
	DFS(mazeGraph, mazeGraph.getVertex(maze.start_y*maze.cols+maze.start_x))
	print "Finish!"
	for ver in mazeGraph.vertList:
		print mazeGraph[ver]
	maze.t.down()
	Pred1 = mazeGraph.getVertex((maze.exit_y+1)*maze.cols+maze.exit_x+1)
	print "exit (%s, %s)" %(maze.exit_x+1, maze.exit_y+1)
	print "start: %s" %Pred1
	while Pred1:
		x = Pred1.key%maze.cols-1
		y = Pred1.key//maze.cols-1
		maze.t.goto(x,y)
		print Pred1
		Pred1 = mazeGraph[Pred1.Pred]


