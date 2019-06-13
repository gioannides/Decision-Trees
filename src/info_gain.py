import numpy as np
import math

def calc_h_ds(dataset):
	# count for each label in each of dataset
	counts  = [0,0,0,0]
	for i in range(len(dataset)):
		# index 2nd dim of counts with Label value
		idx = int(dataset[i,-1]-1)
		counts[idx] +=1

	return calc_entropy(counts)


# Returns the remaining total entropy in both subsets
def calc_remainder(dataset, split_row_num):
	# count for each label in each of dataset, leftSubset, rightSubset
	counts = class_counts(dataset, split_row_num)

	# Calculate subset entropies
	H_left  = calc_entropy(counts[1])
	H_right = calc_entropy(counts[2])

	s_all   = sum(counts[0])
	s_left  = sum(counts[1])
	s_right = sum(counts[2])

	remainder = (s_left/s_all)*H_left + (s_right/s_all)*H_right

	return remainder


# count for each label in each of dataset, leftSubset, rightSubset
# split_row is included in the right subset
# Assumption - Labels are an integer value from 1 to NUM_OUTCOMES
NUM_OUTCOMES = 4
def class_counts(dataset, split_row):
	counts = np.zeros(shape=(3,NUM_OUTCOMES))

	# count labels left subset
	for i in range(split_row):
		# index 2nd dim of counts with Label value
		idx = int(dataset[i,-1]-1)
		# count labels globally
		counts[0, idx] +=1
		# count labels left
		counts[1, idx] +=1

	# count labels right subset
	for i in range(split_row,len(dataset)):
		idx = int(dataset[i,-1]-1)
		# count labels globally
		counts[0, idx] +=1
		# count labels right
		counts[2, idx] +=1

	return counts

# Calculates total entropy given counts for each label
def calc_entropy(labelCounts):
	_sum = 0
	total = sum(labelCounts)

	for label in labelCounts:
		# no outcomes of this type in the subset
		if label==0:
			continue
		else:
			_sum += calc_term(label, total)

	return _sum

# Calculates an entropy term
def calc_term(count, total):
	p_k = count/total
	return -1*p_k*math.log2(p_k)
