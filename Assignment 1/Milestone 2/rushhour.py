import copy as cp
import random
import time
import os

def visual(data): # simple loop for creating a visual of a board state given as a string or list of chars
	for x,c in enumerate(data):
		if x%6 == 0:
			print()
		print(c,end = '')
	print()
	print()

class block: # essential data-type used to represent all pieces on the board and their movements
	def __init__ (self, puzzle, index, identifier): # constructor for the different blocks.
		self.id = identifier # They contain only 3 things, their start (topleftmost cell), their end (bottomrightmost cell), and their id (the letter with which they are represented)
		if self.id not in 'OPQR':
			self.start = index
			if puzzle[index+1] == self.id:
				self.end = index+1
				self.horizontal = True
				#print(self.id,self.start,self.end,self.horizontal)
			else:
				self.end = index+6
				self.horizontal = False
				#print(self.id,self.start,self.end,self.horizontal)
		else:
			self.start = index
			if puzzle[index+2] == self.id:
				self.end = index+2
				self.horizontal = True
				#print(self.id,self.start,self.end,self.horizontal)
			else:
				self.end = index+12
				self.horizontal = False
				#print(self.id,self.start,self.end,self.horizontal)

	def move(self,puzzle,D): # function for moving a block on a given state. (the block does not have to exist as specified in the given board so misuse IS possible)
		if self.horizontal == True:
			if D == 'L' and self.start%6 != 0 and puzzle[self.start-1] == '.':
				self.start -= 1
				puzzle[self.start] = self.id
				puzzle[self.end] = '.'
				self.end -= 1
				puzzle[self.end] = self.id
				return puzzle
			elif D == 'R' and self.end%6 != 5 and puzzle[self.end+1] == '.':
				self.end += 1
				puzzle[self.end] = self.id
				puzzle[self.start] = '.'
				self.start += 1
				puzzle[self.start] = self.id
				return puzzle
			else:
				return False
		else:
			if D == 'U' and self.start > 5 and puzzle[self.start-6] == '.':
				self.start -= 6
				puzzle[self.start] = self.id
				puzzle[self.end] = '.'
				self.end -= 6
				puzzle[self.end] = self.id
				return puzzle
			elif D == 'D' and self.end < 30 and puzzle[self.end+6] == '.':
				self.end += 6
				puzzle[self.end] = self.id
				puzzle[self.start] = '.'
				self.start += 6
				puzzle[self.start] = self.id
				return puzzle
			else:
				return False

def extract(puzzle): # simple loop for extracting the positions of vehicles from a given board state
	options = ['A','B','C','D','E','F','G','H','I','J','K','X','O','P','Q','R']
	vehicles = []
	for x,c in enumerate(puzzle):
		if c in options:
			options.remove(c)
			vehicles.append(block(puzzle,x,c))
	return vehicles

def expand(current_state, vehicles): # a few nested loops for iterating over moving each number of spaces in each direction for each vehicle in a given board state.
	states = [] # the vehicles themselves may later be attained using extract() rather than as an argument.
	moves = []
	for v in vehicles:
		for d in 'UDLR':
			v_copy = cp.deepcopy(v)
			state_copy = cp.deepcopy(current_state)
			for i in range(1,5):
				if v_copy.move(state_copy,d):
					states.append(cp.deepcopy(state_copy))
					moves.append(v_copy.id + d + str(i))
	return states, moves

def load(): # loop for loading in the problems and proposed solutions from 'rh.txt'
	file = open('rh.txt')
	rp = False
	rs = False
	problems = []
	solutions = []
	for line in file.readlines():
		line = line.split()
		if line == ['---', 'end', 'RH-input', '---']:
			rp = False
		if rp:
			problems.append(line[0])
		if line == ['---', 'RH-input', '---']:
			rp = True
		if rs == True:
			extend = solutions[-1]
			if line[-1] == '.':
				for x in line[:-1]:
					extend.append(x)
				rs = False
			else:
				for x in line:
					extend.append(x)
			solutions[-1] = extend
		if len(line) != 0 and line[0] == 'Sol:':
			if line[-1] == '.':
				solutions.append(line[1:-1])
			else:
				solutions.append(line[1:])
				rs = True
	file.close()
	return problems, solutions

def compress(solution): # function for converting a move such as "AL1,AL1,AL1" into "AL3" as the solution format allows multi-space moves (nolonger needed in final implementation)
	compressed = []
	i = 0
	for x in solution:
		compressed.append(x)
	for x in range(len(solution)-1):
		if compressed[i][0:2] == compressed[i+1][0:2]:
			combine = compressed[i][0:2] + str(int(compressed[i][2]) + int(compressed[i+1][2]))
			compressed.pop(i)
			compressed.pop(i)
			compressed.insert(i,combine)
		else:
			i+= 1

	return compressed

def decompress(solution): # function for converting a move such as "AL3" into "AL1,AL1,AL1" as the move function operates one space at a time (nolonger needed in final implementation)
	decompressed = []
	for x in solution:
		for y in range(int(x[2])):
			decompressed.append(x[0:2]+str(1))
	return decompressed
###################################################################
	# new functions
def check(state): # absurdly simple function for checking if a given state is solved or not
	if state[17] == 'X':
		return True
	else:
		return False

def evaluate(state): # basic heuristic function for deciding the value of a state based on the number of obstacles infront of the first 'X'
	if check(state):
		return 0
	obstacles = 1 # obstacles starts at 1 in order to represent the fact that even with nothing in the way the state is not currently solved.
	for i in range(6):
		if state[17-i] == 'X':
			return obstacles
		if state[17-i] != '.':
			obstacles += 1

def output(solution): # function for printing it's input to the output file
	file = open('output.txt','a')
	if solution != None:
		for e in solution:
			file.write(str(e)+'\n')
	file.close()

def Asortkey(element): # function for sorting possible moves in A*
	return len(element[1]) + evaluate(element[0])

def Hillcost(element): # function for sorting possible moves in HillClimb
	return evaluate(element[0])*(50-len(element[1]))

def resultKey(element):
	if type(element[1]) == list:
		return len(element[1])
	else:
		return 1000

###################################################################
	# search algorithms

def BFS(start): # BreadthFirstSearch
	# startup
	global limit
	ts = time.process_time()
	queue = [(start,[])]
	checked = {str(start)}
	print()
	while not check(queue[0][0]):
		x,y = expand(queue[0][0],extract(queue[0][0]))
		for i,j in zip(x,y):
			if time.process_time() > ts+(limit/10):
				print('FAILED\n')
				return ['FAILED','FAILED']
			if str(i) not in checked:
				checked.add(str(i))
				k = cp.copy(queue[0][1])
				k.append(j)
				queue.append((i,k))
		queue.pop(0)
	visual(queue[0][0])
	print(queue[0][1])
	print(len(checked),'states checked')
	print('Solution found at depth', len(queue[0][1]))
	print('Solution found within:',time.process_time()-ts)
	return queue[0]

def DLS(start,depth,ts):
	states = [start]
	checked = set()
	while len(states):
		current = states[-1]
		states.pop()
		x,y = expand(current[0],extract(current[0]))
		for i,j in zip(x,y):
			if time.process_time() > ts+(limit/10):
				print('FAILED\n')
				return 'Fail'
			if str(i) not in checked:
				checked.add(str(i))
				k = cp.copy(current[1])
				k.append(j)
				if check(i):
					return (i,k,checked)
				if len(k) < depth+1:
					states.append((i,k))
	return 'no solutions within depth'

def Iter(start): # Iterative Deepening
	global limit
	ts = time.process_time()
	Initial = (start,[])
	i = 0
	result = DLS(Initial,i,ts)
	if result == 'Fail':
		return
	while type(result) == str:
		if result == 'Fail':
			return ['FAILED','FAILED']
		i += 1
		result = DLS(Initial,i,ts)
	visual(result[0])
	print(result[1])
	print(len(result[2]),'states checked')
	print('Solution found at depth', len(result[1]))
	print('Solution found within:',time.process_time()-ts)
	return result[:2]

def AStar(start): # A*
	global limit
	ts = time.process_time()
	queue = [(start,[])]
	checked = {str(start)}
	while not check(queue[0][0]):
		x,y = expand(queue[0][0],extract(queue[0][0]))
		for i,j in zip(x,y):
			if time.process_time() > ts+(limit/10):
				print('FAILED\n')
				return ['FAILED','FAILED']
			if str(i) not in checked:
				checked.add(str(i))
				k = cp.copy(queue[0][1])
				k.append(j)
				queue.append((i,k))
		queue.pop(0)
		queue.sort(key = Asortkey)
	visual(queue[0][0])
	print(queue[0][1])
	print(len(checked),'states checked')
	print('Solution found at depth', len(queue[0][1]))
	print('Solution found within:',time.process_time()-ts)
	return queue[0]

def HillClimb(Start): # Random Restart Hill Climbing
	global limit
	ts = time.process_time()
	state = [Start,[]]
	best = [Start,[]]
	checked_board = []
	checked_steps = []
	while not check(state[0]):
		new = []
		x,y = expand(state[0],extract(state[0]))
		for i,j in zip(x,y):
			if time.process_time() > ts+(limit/10):
				print('FAILED')
				print('The best state found is:')
				print(best[1])
				visual(best[0])
				return ['FAILED','FAILED']
			if i not in checked_board:
				checked_board.append(i)
				k = cp.copy(state[1])
				k.append(j)
				checked_steps.append(k)
				new.append((i,k))
		new.sort(key = Hillcost)
		if len(new):
			if Hillcost(new[0]) < Hillcost(best):
				best = new[0]
			if Hillcost(new[0]) < Hillcost(state):
				state = new[0]
		else:
			index = random.choice(range(len(checked_board)))
			state = [checked_board[index],checked_steps[index]]
	print(best[1])
	visual(best[0])
	print(len(checked_board),'states checked')
	print('Solution found at depth', len(best[1]))
	print('Solution found within:',time.process_time()-ts)
	return best

###################################################################

problems,solutions = load() # load problems and solutions from 'rh.txt'
i = 1
for x,y in zip(problems,solutions): # print each problem and its solution
	print('Problem '+str(i)+':')
	i +=1
	visual(x)
	print('Given solution:',y,end = '\n\n')
i = 0
#data = list('AA...OP..Q.OPXXQ.OP..Q..B...CCB.RRR.') # hardcoded example problem

limit = 100 # other than Iterative Deepening expect solutions within ~6 seconds
#limit = input('Input time limit in 1/10s: ')

if os.path.exists('output.txt'): # clearing the output file if there is one
	os.remove('output.txt')

for i in range(38,39):
	data = list(problems[i]) # the same problem as above but taken from the loaded problems list

	print('Problem ' +str(i+1)) #
	print('Initial State:')     #
	visual(data)                # visualising the selected problem

	ts = time.process_time() # start time

	result = []

	print('\nBFS:',end = '')         #
	result.append(BFS(data))         #
	print('\nIterative Deepening:')  #
	result.append(Iter(data))        #
	print('\nA*:')                   #
	result.append(AStar(data))       # ugly code for clean printing and output
	print('\nHillClimb:')            #
	result.append(HillClimb(data))   #
	result.sort(key = resultKey)     #

	output([str(result[0][1]).replace("'",'').replace(',','').replace('[','').replace(']','')]) # cleans up the list into a string of the original solution format

	te = time.process_time() # end time

	print('\nAll algorithms run within', te-ts)
	print('Example solution:', solutions[i])


#possible_states,possible_moves = expand(data,vehicles) # example of the expand opperation with a loop displaying all reachable states and the associated moves
#for x,y in zip(possible_states,possible_moves):
	#print(y + ':')
	#visual(x)


#print(decompress(['CL3','OD3','AR1','PU1','BU1','RL2','QD2','XR5'])) # example/test case for decompress/compress functions
#print(compress(decompress(['CL3','OD3','AR1','PU1','BU1','RL2','QD2','XR5'])))
