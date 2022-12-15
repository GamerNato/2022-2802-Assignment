import random
import copy as cp
import matplotlib.pyplot as plt

def load(path):
	infile = open(path, 'r') # open input file
	result = [[float(a[0]),float(a[1]),float(a[2]),float(a[3]),int(a[4] == "setosa")*1 + int(a[4] == "versicolor")*2 + int(a[4] == "virginica")*3] for a in [line[:-1].split(',') for line in infile][1:]]
	 # extract raw data and convert to usable format
	infile.close() # close input file
	return result

def split_data(data,ratio):
	testing = random.sample(data,int(len(data)*ratio)) # select random testing data
	training = cp.copy(data) # setup training as copy of full dataset
	for t in testing: # remove duplicates 1:1
		if t in training:
			training.pop(training.index(t))
	return training,testing

def euclidean_distance(A, B):
	distance = 0
	for x,y in zip(A[:-1],B[:-1]): # euclidean distance between variables except species itself
		distance += (x-y)**2
	return distance**(1/2)

def alternative_distance(A, B):
	distance = 0
	for x,y in zip(A[2:4],B[2:4]): # sum distance between petal variables only
		if x > y:
			distance += x-y
		else:
			distance += y-x
	return distance

def sortKey(element):
	return element[1] # return distance from tuple of (flower,distance)

def kNN(data,sample,k):
	neighbors = [(f,euclidean_distance(f,sample)) for f in data] # for each flower make tuple of flower, distance from sample being tested
	#neighbors = [(f,alternative_distance(f,sample)) for f in data] # using alternative distance function
	neighbors.sort(key = sortKey) # sort by distance
	return neighbors[:k] # return k nearest

def classifier(training,sample,k):
	species = 0
	neighbors = kNN(training,sample,k)
	for n in neighbors: # get kNN of sample
		species += n[0][-1]
	species /= len(neighbors) # get mean species of neighbors
	species = round(species)
	#""" # all for output format
	print('sample class = ',end='')
	if sample[-1] == 1:
		print('Iris-setosa,     ',end='')
	elif sample[-1] == 2:
		print('Iris-versicolor, ',end='')
	elif sample[-1] == 3:
		print('Iris-virginica,  ',end='')
	print('prediction class = ',end='')
	if species == 1:
		print('Iris-setosa,     ',end='')
	elif species == 2:
		print('Iris-versicolor, ',end='')
	elif species == 3:
		print('Iris-virginica,  ',end='')
	print('prediction correct:',sample[-1] == species)
	#"""
	return species

def accuracy(dataset,ratio,k):
	if ratio > 0.995: # if ratio is too big reset to largest acceptable value
		ratio = 0.995
	if ratio < 0.005: # if ratio is too small reset to smallest acceptable value
		ratio = 0.005
	total_accuracy = 0
	accuracy = 0
	training,testing = split_data(dataset,ratio) # split dataset into training and testing
	for s in training: # iterate over training set
		if classifier(training,s,k) == s[4]: # check prediction and actual
			accuracy += 1
	total_accuracy += accuracy
	print(accuracy,'/',(len(training)))
	print('Training set accuracy: '+ str(float(accuracy/(len(training))*100)) + ' %') # calculate percent accuracy
	accuracy = 0
	for s in testing: # iterate over testing set
		if classifier(training,s,k) == s[4]: # check prediction and actual
			accuracy += 1
	total_accuracy += accuracy
	print(accuracy,'/',(len(testing)))
	print('Testing set accuracy: '+ str(float(total_accuracy/(len(testing)+len(training))*100)) + ' %') # calculate percent accuracy
	return float(total_accuracy/(len(testing)+len(training))*100)


#path = input("Please input filepath:")
path = 'iris.csv' # hardcoded path for testing purposes

dataset = load(path)

accuracy(dataset,1/3,3)

""" # iterates through k values and shows accuracy plot
k_values = []
for k in range(1,151):
	k_values.append((int(accuracy(dataset,0.5,k))+int(accuracy(dataset,0.5,k))+int(accuracy(dataset,0.5,k)))/3)

plt.plot(range(1,151),k_values)
plt.xlabel('k')
plt.ylabel('Accuracy')
plt.axis([1, 150, 0, 100])
plt.show()
#"""
