from graphics import *
import random
from time import *
gvn = [27]
win = GraphWin("Sudoku", 460, 600)
sol = []
puz = []
	
	
def drawgrid():
	xy = [5,55,105,155,205,255,305,355,405,455]
	for i in range(10):
		l = Line( Point(xy[0], xy[i]), Point(xy[9], xy[i]))
		if i % 3 == 0:
			l.setWidth(3)
		l.draw(win)
	for i in range(10):
		l = Line( Point(xy[i], xy[0]), Point(xy[i], xy[9]))
		if i % 3 == 0:
			l.setWidth(3)
		l.draw(win)
		
def blank(ix):    # blank a particular square
	x = (ix % 9) * 50 
	y = int(ix / 9) * 50
	r = Rectangle(Point(x + 7, y + 7), Point(x + 53, y + 53))
	r.setFill("white")
	r.setOutline("white")
	r.draw(win)

def eliminate(i,num):
	col = i % 9   # top of column
	row = int(i / 9)   # start of row
	cnr = int(col / 3) * 3 + int(row / 3) * 27
	for x in range(9): # remove numbers found in row
		f = wkg[row * 9 + x]
		if f > 0:
			num[f] = 0
	for y in range(9): # remove numbers found in column
		f = wkg[col + y * 9]
		if f > 9:
			print("f = ",f,wkg)
		if f > 0:
			num[f] = 0
	for b in range(9): # remove numbers found in nine-block
		f = wkg[cnr + int(b / 3) * 9 + b % 3]
		if f > 0:
			num[f] = 0
	
def getsol():     # fill with random valid entries
	ri = 0
	a = 0
	t = 0
	global wkg 
	wkg = list(range(81))
	while t == 0:
		a = a + 1
		for i in range(81):
			wkg[i] = 0
		for i in range(81):
			num = list(range(10))
			eliminate(i,num)
			if sum(num) > 0:    # ensure there are numbers left in num[]
				v = [0]
				while v[0] == 0:     # choose a non-zero value at random
					v = random.sample(num,1)
				wkg[i] = v[0]
				if i == 80:
					t = 1
					print(a," Reached 80!")
			else:
				if i > ri:
					print(a," Failed at ",i)
					ri = i
				break
	global sol
	sol = list(wkg)
	for i in range(81):
#		sol[i] = wkg[i]
		m = Text(Point((i % 9) * 50 + 30, int(i / 9) * 50 + 35),sol[i])
		m.draw(win)
	t = "Solution generated in "  + str(a) + " attempts"
	print(t)
	m = Text(Point(125,470),t)
	m.draw(win)
	sleep(3)
		
def placegvn():
	v = 0
	c = 0
	global puz, a
	puz = list(range(81))
	while v != gvn[0]:
		for i in range(81):
			puz[i] = 0
		gap = range(int(162 / gvn[0]))
		i = 0
		t = 0
		v = 0
		while t == 0:
			g = random.sample(gap,1)
			i = i + g[0]
			if i < 81:
				puz[i] = sol[i]
				v = v + 1
				i = i + 1
			else:
				t = 1
		c = c + 1
#		print c, " givens: ",v
	for i in range(81):
		blank(i)
		if puz[i] > 0:
			m = Text(Point((i % 9) * 50 + 30, int(i / 9) * 50 + 35),puz[i])
			m.setStyle("bold")
			m.setSize(22)
			m.draw(win)
	r = Rectangle(Point(2,485), Point(448,515))
	r.setFill("white")
	r.setOutline("white")
	r.draw(win)
	t = str(gvn[0]) + " givens placed in " + str(c) + " attempts. (" + str(a) + ")"
	print(t)
	m = Text(Point(140,500),t)
	m.draw(win)
	
def finduniques():
	global wkg
	for i in range(81):   # Check if any cells have only one possibility
		if wkg[i] == 0:
			num = list(range(10))
			eliminate(i,num)
			c = 0
			for x in range(10):
				if num[x] > 0:
					v = num[x]
					c = c + 1
			if c == 1:
				wkg[i] = v
				m = Text(Point((i % 9) * 50 + 30, int(i / 9) * 50 + 35),v)
				m.setTextColor("red")
				m.draw(win)
				
def lineuniques():
	global wkg
	for y in range(9):  # check each row to find single possibilities 
		num = list(range(10))
		for n in num:   # for each number
			u = 0       # possibilities
			for x in range(9):   # each cell
				v = 0
				if wkg[y * 9 + x] == n: # there is an n already
					u = 100
				if wkg[y * 9 + x] == 0:
					v = 1                # this cell might be n
					for yy in range(9):  # check column for n
						if wkg[yy * 9 + x] == n:
							v = 0        # there is an n in the column
					if v == 1:
						xx = x
				u = u + v
			if u == 1:              # unique found
				wkg[y * 9 + xx] = n
				m = Text(Point(xx * 50 + 30, y * 50 + 35),n)
				m.setTextColor("blue")
				m.draw(win)
			
def coluniques():
	global wkg
	for x in range(9):  # check each column to find single possibilities 
		num = list(range(10))
		for n in num:   # for each number
			u = 0       # possibilities
			for y in range(9):   # each cell
				v = 0
				if wkg[y * 9 + x] == n: # there is an n already
					u = 100
				if wkg[y * 9 + x] == 0:
					v = 1                # this cell might be n
					for xx in range(9):  # check column for n
						if wkg[y * 9 + xx] == n:
							v = 0        # there is an n in the column
					if v == 1:
						yy = y
				u = u + v
			if u == 1:              # unique found
				wkg[yy * 9 + x] = n
				m = Text(Point(x * 50 + 30, yy * 50 + 35),n)
				m.setTextColor("green")
				m.draw(win)
					
def boxuniques():
	global wkg
	for b in range(9):  # check each box to find single possibilities 
		num = list(range(10))
		for n in num:   # for each number
			u = 0       # possibilities
			for c in range(9):   # each cell
				v = 0
				y = int(b / 3) * 3 + int(c / 3)  
				x = (b % 3) * 3 + (c % 3)
				if wkg[y * 9 + x] == n: # there is an n here already
					u = 100
				if wkg[y * 9 + x] == 0:
					v = 1                # this cell might be n
					for xx in range(9):  # check line for n
						if wkg[y * 9 + xx] == n:
							v = 0        # there is an n in the line
					for yy in range(9):  # check colunm for n
						if wkg[yy * 9 + x] == n:
							v = 0        # there is an n in the line
					if v == 1:
						yb = y
						xb = x           # record position
				u = u + v
			if u == 1:              # unique found
				wkg[yb * 9 + xb] = n
				m = Text(Point(xb * 50 + 30, yb * 50 + 35),n)
				m.setTextColor("orange")
				m.draw(win)
		   
	
def trysolve():
	global wkg
	global d,f
	d = 0
	wkg = list(puz)
	p = 0
	while d < 10:
		d = d + 1
		finduniques()
		lineuniques()
		coluniques()
		boxuniques()
		f = 0
		for i in range(81):
			if wkg[i] == 0:
				f = f + 1
		if f != p:
			d = 0
		p = f
		if f == 0:
			d = 100

		
def makepuz():
	global d,f,a
	a = 0
	d = 0
	while d != 100:
		a = a + 1
		placegvn()
		trysolve()
		print("Attempt ",a," spaces = ",f)
#		sleep(2)
		if a == 500:
			break
#		win.getMouse() # Pause to view result
	if a == 500:
		t = "No puzzle solvable by simple rules found in " + str(a) + " attempts."
	else:
		t = "Puzzle solvable by simple rules found in " + str(a) + " attempts."
	print(t)
	m = Text(Point(200,530),t)
	m.draw(win)
	for i in range(81):
		if puz[i] == 0:
			blank(i)
#		else:
#			m = Text(Point((i % 9) * 50 + 30, int(i / 9) * 50 + 35),puz[i])
#			m.setStyle("bold")
#			m.draw(win)
		
def close():			
	win.getMouse() # Pause to view result
	win.close()    # Close window when done
	exit()

drawgrid()
getsol()
makepuz()
close()
