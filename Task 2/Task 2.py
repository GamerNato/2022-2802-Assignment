import random
import math
import copy as cp
import matplotlib.pyplot as plt

################################################
 # DT functions

def load(path):
	infile = open(path, 'r') # open input file
	result = [a for a in [line[:-1].split(',') for line in infile][1:]] # read out all lines
	infile.close() # close input file
	for x in result:
		x.append(x.pop(0)) # move class to the end (to resemble task 1 dataset (did not end up being used for knn))
		for i in range(len(x[:-1])):
			x[i] = int(x[i])
	 # extract raw data and convert to usable format
	return result

def split_data(data,ratio):
	testing = random.sample(data,int(len(data)*ratio)) # select random testing data
	training = cp.copy(data) # setup training as copy of full dataset
	for t in testing: # remove duplicates 1:1
		if t in training:
			training.pop(training.index(t))
	return training,testing

def check_entropy(data): # return entropy of node
	if len(data):
		dem = len([p for p in data if p[-1] == 'democrat'])/len(data)
		rep = len([p for p in data if p[-1] == 'republican'])/len(data)
		if dem == 0 or rep == 0: # if data is all the same class entropy is 0
			return 0
		return -(dem*math.log2(dem))-(rep*math.log2(rep)) # if no edge cases return entropy as usual
	else: # if data is empty return 1 to rank it as a useless split
		return 1

def split_entropy(data,Attribute_Index): # calculate the entropy of splitting data by some attribute
	true = [p for p in data if p[Attribute_Index]] # data with attribute true
	false = [p for p in data if not p[Attribute_Index]] # data with attribute false
	return (len(true)/len(data))*check_entropy(true)+(len(false)/len(data))*check_entropy(false) # return entropy of split

def information_gain(data,Attribute_Index):
	return check_entropy(data)-split_entropy(data,Attribute_Index) # return info gain for some split

def next_attribute(data, options): # return the best attribute to split data by
	#print(options)
	best = (None,0)
	for i in options: # check each remaining option
		gain = information_gain(data,i)
		if gain > best[1]: # record best attribute by max info gain
			best = (i,gain)
	if best[0] in options:
		options.remove(best[0]) # remove best option from list
		return best[0],options # return best attribute and remaining optionsd
	else:
		return 'class' # if no splits gain any information or if there are no more options left

def next_node(data, options): # split data by best attribute and return the nodes
	node = next_attribute(data,options)
	if type(node) == str:
		return 'class' # if no best attribute return class
	else:
		true = [p for p in data if p[node[0]]]
		false = [p for p in data if not p[node[0]]]
		return true,false,node[1],node[0] # return true data,false data, the remaining options for further splits, and attribute the data has been split by

def build_tree(tree,index,data,options = [-1]): # recursive generation of a decision tree
	if options == [-1]: # if no options given
		for i in range(len(data[0])-1):
			options.append(i)
	# tree format = (attribute,true index,false index) or 'class'
	returned = next_node(data,cp.copy(options)) # get next split
	if type(returned) == str: # if node should be leaf
		if tree == []: # if tree is empty
			tree.append(None) # make sure there is at least 1 node to be a leaf
		if len([p for p in data if p[-1] == 'democrat']) > len([p for p in data if p[-1] == 'republican']): # pick which class it belongs to
			tree[index] = 'democrat'
		else:
			tree[index] = 'republican'
		return tree
	else:
		if tree == []: # if tree is empty
			tree.append((returned[-1],len(tree)+1,len(tree)+2)) # add starting node
		else:
			tree[index] = (returned[-1],len(tree),len(tree)+1) # add next node
		tree.append(None) #
		tree.append(None) # make space for child nodes to be defined as split or leaf later
	for e,i in enumerate(tree[index][1:]): # for each child node
		if check_entropy(returned[e]) < 0.01: # if sufficiently low entropy make leaf node
			if len([p for p in data if p[-1] == 'democrat'])/len(data) > len([p for p in data if p[-1] == 'republican'])/len(data): # pick most prevalent class
				tree[tree[index][e+1]] = 'democrat'
			else:
				tree[tree[index][e+1]] = 'republican'
		else: # else recurse to split again
			build_tree(tree,tree[index][e+1],returned[e],returned[-2])
	# once all branches terminate return complete tree
	return tree

def classifier(tree,sample,index = 0): # given some sample recurse through the tree
	if type(tree[index]) != str: # if not a leaf node recurse
		if sample[tree[index][0]]: # pick which branch to move to based on sample
			return classifier(tree,sample,tree[index][1])
		else:
			return classifier(tree,sample,tree[index][2])
	else: # if leaf node reached
		return tree[index] # return prediction back up the recursion tree to original call

def accuracy(tree,testing): # calculate accuracy over testing data
	correct = 0
	for x in testing:
		if classifier(tree,x) == x[-1]: # if prediction is correct incriment
			correct += 1
	return correct/len(testing)*100 # return accuracy as %

def precision(tree,testing):
	correct_dems = 0
	incorrect_dems = 0
	correct_reps = 0
	incorrect_reps = 0
	for x in testing: # for each test sample
		if classifier(tree,x) == x[-1]: # if prediction is correct
			if x[-1] == 'democrat': # if actually dem
				correct_dems += 1
			else: # if actually rep
				correct_reps += 1
		else: # if prediction is incorrect
			if x[-1] == 'democrat': # if actually dem
				incorrect_dems += 1
			else: # if actually rep
				incorrect_reps += 1
	return correct_dems/(correct_dems+incorrect_dems),correct_reps/(correct_reps+incorrect_reps) # return precision values for dems and reps

def recall(tree,testing): # return recall values for DT
	correct_dems = 0
	incorrect_reps = 0
	correct_reps = 0
	incorrect_dems = 0
	for x in testing: # for each test sample
		if classifier(tree,x) == x[-1]: # if prediction is correct
			if x[-1] == 'democrat': # if actually dem
				correct_dems += 1
			else: # if actually rep
				correct_reps += 1
		else: # if prediction is incorrect
			if x[-1] == 'democrat': # if actually dem
				incorrect_dems += 1
			else: # if actually rep
				incorrect_reps += 1
	return correct_dems/(correct_dems+incorrect_reps),correct_reps/(correct_reps+incorrect_dems) # return recall values for dems and reps

def F1(tree,testing): # return DT F1 values
	p = precision(tree,testing)
	r = recall(tree,testing)
	return 2*((r[0]*p[0])/(r[0]+p[0])),2*((r[1]*p[1])/(r[1]+p[1])) # return F1 values for dems and reps separately

def results(tree,testing): # print all DT results
	print('precision =',precision(tree,testing))
	print('recall =',recall(tree,testing))
	print('F1 =',F1(tree,testing))

################################################
 # KNN functions

def k_load(path): # modified load function
	infile = open(path, 'r') # open input file
	result = [a for a in [line[:-1].split(',') for line in infile][1:]] # read out all lines
	infile.close() # close input file
	for x in result:
		if x.pop(0) == 'democrat': # put class variable at the end as int
			x.append(1) # democrat class = 1
		else:
			x.append(2) # republican class = 2
		for i in range(len(x[:-1])): # convert strings to int
			x[i] = int(x[i])
	 # extract raw data and convert to usable format
	return result

def euclidean_distance(A, B): # calculates euclidean distance between sample A and sample B
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

def k_classifier(training,sample,k): # classify sample using k nearest in training set
	species = 0
	neighbors = kNN(training,sample,k)
	for n in neighbors: # get kNN of sample
		species += n[0][-1]
	species /= len(neighbors) # get mean species of neighbors
	species = round(species)
	return species # return prediction

def k_accuracy(training,testing,k): # retrun knn accuracy
	total_accuracy = 0
	accuracy = 0
	for s in testing: # iterate over testing set
		if k_classifier(training,s,k) == s[-1]: # check prediction and actual
			accuracy += 1
	total_accuracy += accuracy
	#print(accuracy,'/',(len(testing)))
	#print('KNN accuracy: '+ str(float(total_accuracy/(len(testing))*100)) + ' %') # calculate percent accuracy
	return float(total_accuracy/(len(testing))*100)

def k_precision(training,testing,k): # return knn precision
	correct_dems = 0
	incorrect_dems = 0
	correct_reps = 0
	incorrect_reps = 0
	for x in testing: # for each test sample
		if k_classifier(training,x,k) == x[-1]: # if prediction is correct
			if x[-1] == 1: # if actually dem
				correct_dems += 1
			else: # if actually rep
				correct_reps += 1
		else: # if prediction is incorrect
			if x[-1] == 1: # if actually dem
				incorrect_dems += 1
			else: # if actually rep
				incorrect_reps += 1
	return correct_dems/(correct_dems+incorrect_dems),correct_reps/(correct_reps+incorrect_reps) # return precision values

def k_recall(training,testing,k): # return knn recall values
	correct_dems = 0
	incorrect_reps = 0
	correct_reps = 0
	incorrect_dems = 0
	for x in testing: # for each test sample
		if k_classifier(training,x,k) == x[-1]: # if prediction is correct
			if x[-1] == 1: # if actually dem
				correct_dems += 1
			else: # if actually rep
				correct_reps += 1
		else: # if prediction is incorrect
			if x[-1] == 1: # if actually dem
				incorrect_dems += 1
			else: # if actually rep
				incorrect_reps += 1
	result = []
	if correct_dems+incorrect_reps: # check that denomenator is not 0
		result.append(correct_dems/(correct_dems+incorrect_reps))
	else:
		result.append(0)
	if correct_reps+incorrect_dems: # check that denomenator is not 0
		result.append(correct_reps/(correct_reps+incorrect_dems))
	else:
		result.append(0)
	return tuple(result) # return recall values

def k_F1(training,testing,k): # return knn F1 values
	p = k_precision(training,testing,k)
	r = k_recall(training,testing,k)
	result = []
	if r[0]+p[0]: # check that denomenator is not 0
		result.append(2*((r[0]*p[0])/(r[0]+p[0])))
	else:
		result.append(0)
	if r[1]+p[1]: # check that denomenator is not 0
		result.append(2*((r[1]*p[1])/(r[1]+p[1])))
	else:
		result.append(0)
	return tuple(result) # return f1 values

def k_results(training,testing,k): # print all knn results
	print('k precision =',k_precision(training,testing,k))
	print('k recall =',k_recall(training,testing,k))
	print('k F1 =',k_F1(training,testing,k))

################################################
 # main

#path = input("Please input filepath:")
path = 'votes.csv' # hardcoded path for testing purposes

k_dataset = k_load(path)
k_training,k_testing = split_data(k_dataset,1/2) # split dataset into training and testing

k_results(k_training,k_testing,200)

dataset = load('votes.csv')
training, testing = split_data(dataset,1/2)

results(build_tree([],0,training),testing)
print(build_tree([],0,training))
#learning curve loop

x_key = []
k_accuracies = []
accuracies = []
for r in range(1,10):
	r = float(r/10)
	k_training,k_testing = split_data(k_dataset,r)
	training, testing = split_data(dataset,r)
	k_accuracies.append(k_accuracy(k_training,k_testing,200))
	accuracies.append(accuracy(build_tree([],0,training),testing))
	x_key.append(r)
	#print(x_key[-1],k_accuracies[-1],accuracies[-1])
	#print(len([p for p in k_training if p[-1] == 1]),len([p for p in k_training if p[-1] == 2]),k_classifier(k_training,k_testing[0],200),k_testing[0][-1])

# learning curve plot

plt.plot(x_key,k_accuracies,label = 'KNN Accuracy')
plt.plot(x_key,accuracies, label = 'DT Accuracy')
plt.legend()
plt.xlabel('ratio')
plt.ylabel('Accuracy')
plt.axis([0, 1, 0, 100])
plt.show()

