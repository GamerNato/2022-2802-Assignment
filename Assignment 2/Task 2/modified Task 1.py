import random
import copy as cp
import matplotlib.pyplot as plt

def k_load(path): # modified load function
	infile = open(path, 'r') # open input file
	result = [a for a in [line[:-1].split(',') for line in infile][1:]]
	for x in result:
		if x.pop(0) == 'democrat':
			x.append(1)
		else:
			x.append(2)
		for e,y in enumerate(x[:-1]):
			if y == '0':
				x[e] = 0
			else:
				x[e] = 1
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

def sortKey(element):
	return element[1] # return distance from tuple of (flower,distance)

def kNN(data,sample,k):
	neighbors = [(f,euclidean_distance(f,sample)) for f in data] # for each flower make tuple of flower, distance from sample being tested
	neighbors.sort(key = sortKey) # sort by distance
	return neighbors[:k] # return k nearest

def classifier(training,sample,k):
	species = 0
	for n in kNN(training,sample,k): # get kNN of sample
		species += n[0][-1]
	species /= k # get mean species of neighbors
	species = round(species)
	#""" # modified output formap
	print('sample class = ',end='')
	if sample[-1] == 1:
		print('dem, ',end='')
	elif sample[-1] == 2:
		print('rep, ',end='')
	print('prediction class = ',end='')
	if species == 1:
		print('dem, ',end='')
	elif species == 2:
		print('rep, ',end='')
	print('prediction correct:',sample[-1] == species)
	#"""
	return species

def k_accuracy(dataset,ratio,k):
	if ratio > 0.995: # if ratio is too big reset to largest acceptable value
		ratio = 0.995
	if ratio < 0.005: # if ratio is too small reset to smallest acceptable value
		ratio = 0.005
	total_accuracy = 0
	accuracy = 0
	training,testing = split_data(dataset,ratio) # split dataset into training and testing
	for s in training: # iterate over training set
		if classifier(training,s,k) == s[-1]: # check prediction and actual
			accuracy += 1
	total_accuracy += accuracy
	print(accuracy,'/',(len(training)))
	print('Training set accuracy: '+ str(float(accuracy/(len(training))*100)) + ' %') # calculate percent accuracy
	accuracy = 0
	for s in testing: # iterate over testing set
		if classifier(training,s,k) == s[-1]: # check prediction and actual
			accuracy += 1
	total_accuracy += accuracy
	print(accuracy,'/',(len(testing)))
	print('Testing set accuracy: '+ str(float(total_accuracy/(len(testing)+len(training))*100)) + ' %') # calculate percent accuracy
	return float(total_accuracy/(len(testing)+len(training))*100)


#path = input("Please input filepath:")
path = 'votes.csv' # hardcoded path for testing purposes

dataset = k_load(path)

k_accuracy(dataset,1/2,200)

#""" # iterates through k values and shows accuracy plot
k_values = []
for k in range(1,201):
	k_values.append((k_accuracy(dataset,0.5,k)))

plt.plot(range(1,201),k_values)
plt.xlabel('k')
plt.ylabel('Accuracy')
plt.axis([1, 200, 0, 100])
plt.show()
#"""
