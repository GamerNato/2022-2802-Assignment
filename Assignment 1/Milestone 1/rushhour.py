import copy as cp

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
	record = False
	problems = []
	solutions = []
	for line in file.readlines():
		line = line.split()
		if line == ['---', 'end', 'RH-input', '---']:
			record = False
		if record:
			problems.append(line[0])
		if line == ['---', 'RH-input', '---']:
			record = True
		if len(line) != 0 and line[0] == 'Sol:':
			pass
			solutions.append(line[1:-1])
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

problems,solutions = load() # load problems and solutions from 'rh.txt'
for x,y in zip(problems,solutions):
	visual(x)
	print(y)


#data = list('AA...OP..Q.OPXXQ.OP..Q..B...CCB.RRR.') # hardcoded example problem
data = list(problems[0]) # the same problem as above but taken from the loaded problems list
print('Initial State:')
visual(data)
vehicles = extract(data)

possible_states,possible_moves = expand(data,vehicles) # loop displaying all reachable states and the associated moves
for x,y in zip(possible_states,possible_moves):
	print(y + ':')
	visual(x)


#print(decompress(['CL3','OD3','AR1','PU1','BU1','RL2','QD2','XR5'])) # example/test case for decompress/compress functions
#print(compress(decompress(['CL3','OD3','AR1','PU1','BU1','RL2','QD2','XR5'])))
