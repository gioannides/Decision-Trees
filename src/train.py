from node import Node
from info_gain import calc_remainder
from info_gain import calc_h_ds

import multiprocessing

# Wrapper for find_split() return values
class Split_Info():
	def __init__(self, node, row, sorted_data):
		self.node  = node
		self.row   = row
		self.set   = sorted_data


# Multithread wrapper for learn.decision_tree_learning
def build_tree(procnum, return_dict, dataset):
	print("Started to train tree " + str(procnum+1) + "..")
	root, height = decision_tree_learning(dataset, 0)
	return_dict[procnum] = (root, height)
	print("Tree " + str(procnum+1) + " trained, Height = " + str(height))


# Returns list len 90: elements = (root, height)
def cross_validation_train(training_sets):
	# Build 90 trees
	manager = multiprocessing.Manager()
	# contains (root, height) for trained trees
	trees = manager.dict()
	jobs = []
	count = 0
	for _ in range(6):
		for _ in range(15):
			p = multiprocessing.Process(target=build_tree,
										args=(count,trees,training_sets[count]) )
			count +=1
			jobs.append(p)
			p.start()
		for proc in jobs:
			proc.join()

	return trees


# Returns a Node and it's depth in the tree
# If returning root node, depth return value = tree height
def decision_tree_learning(training_dataset, depth):
	# Check if all samples have same label
	first_label = training_dataset[0,-1]
	all_same = True
	for r in range(len(training_dataset)):
		if training_dataset[r,-1] != first_label:
			all_same = False
			break # need to find a split point

	# If all have same label - found a leaf node
	if all_same:
		leaf = Node(first_label, -1)
		return (leaf, depth)

	# Question node
	else:
		# Find split point + get sorted dataset
		split = find_split(training_dataset)

		# a new decision tree with root as split value
		# and attribute as split col
		node = split.node

		# split the sorted dataset
		ldataset, rdataset = partition(split.row, split.set)

		# create left and right branches
		lbranch, ldepth = decision_tree_learning(ldataset, depth+1)
		rbranch, rdepth = decision_tree_learning(rdataset, depth+1)

		# link Question to left and right branches
		node.set_branches(lbranch, rbranch)

		return(node, max(ldepth, rdepth))


# Find the split point that
# minimises the remaining entropy
def find_split(training_dataset):
	# Entropy in the dataset
	min_remaining_entropy = calc_h_ds(training_dataset)
	# keep track of split point that produced the best_gain
	best_split = None

	num_features = len(training_dataset[0]) - 1

	for j in range(num_features): # for each attribute
		# sort and initialise variables
		sorted_ds = training_dataset[training_dataset[:,j].argsort()]
		for i in range(1, len(sorted_ds)): # check through each example
			# diff outcome
			if sorted_ds[i,-1] != sorted_ds[i-1,-1]:
				remaining_entropy = calc_remainder(sorted_ds, i)

				if remaining_entropy < min_remaining_entropy:
					min_remaining_entropy = remaining_entropy
					# New Question Node - with midpoint value and column
					mid_point = float( (sorted_ds[i,j] + sorted_ds[i-1,j]) / 2 )
					best_split = Split_Info( Node(mid_point , j) , i, sorted_ds )

	return best_split


# Returns two subsets after splitting input dataset
# Dataset should be sorted
# Format: 2D numpy arrays
def partition(split, data):
	split = int(split)
	# rows up to split
	ldata = data[:split, :]
	# rows from split
	rdata = data[split:, :]

	return ldata, rdata
