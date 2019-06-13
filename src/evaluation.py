import numpy as np

class Eval_Metrics:
	def __init__(self, matrix):
			self.c_matrix = matrix
			self.recall = np.zeros(shape=(4))
			self.precision = np.zeros(shape=(4))
			self.f1 = np.zeros(shape=(4))
			self.c_rate = None

			# storing standard deviation is false by default
			self.sd = False

			self.calc_metrics()

	def __str__(self):
			ret = ""
			# If standard deviation metric, ignore printing
			if not self.sd:
				ret += "Confusion Matrix: \n" + str(self.c_matrix) + "\n"
			ret += "Recall\t\t [C1, C2, C3, C4] = " + str(self.recall) + "\n"
			ret += "Precision\t [C1, C2, C3, C4] = " + str(self.precision) + "\n"
			ret += "F1\t\t [C1, C2, C3, C4] = " + str(self.f1) + "\n"
			ret += "Classification Rate = " + str(self.c_rate) + "\n"
			return ret

	# Extension for standard deviation
	def store_sd(self, sd_recall, sd_precision, sd_f1, sd_cr):
		self.sd = True
		self.recall    = sd_recall
		self.precision = sd_precision
		self.f1        = sd_f1
		self.c_rate    = sd_cr

	def calc_metrics(self):
		self.calc_recall()
		self.calc_precision()
		self.calc_f1(1)
		self.calc_c_rate()

	def calc_recall(self):
		for i in range(4):
			TP = self.c_matrix[i,i]
			FN = 0
			for j in range(4):
				if i != j:
					FN += self.c_matrix[i,j]
			self.recall[i] = TP/(TP+FN)

	def calc_precision(self):
		for i in range(4):
			TP = self.c_matrix[i,i]
			FP = 0
			for j in range(4):
				if i != j:
					FP += self.c_matrix[j,i]
			self.precision[i] = TP/(TP+FP)

	def calc_f1(self, alpha):
		for i in range(4):
			num = (1+alpha**2) * self.precision[i] * self.recall[i]
			den = (alpha**2 * self.precision[i]) + self.recall[i]
			self.f1[i] = num/den

	def calc_c_rate(self):
		trace = 0
		for i in range(4):
			trace += self.c_matrix[i,i]
		m_sum = self.c_matrix.sum()
		self.c_rate = trace / m_sum

# Returns Eval_Metrics for given test data set and tree
def evaluate(test_db,trained_tree):
	c_matrix = np.zeros(shape=(4,4))
	# Fill Confusion Matrix
	for sample in test_db:
		actual = int(sample[-1])
		prediction = int(classify(sample, trained_tree))
		c_matrix[actual-1, prediction-1] +=1

	test_metrics = Eval_Metrics(c_matrix)

	return test_metrics

# Returns predicted value
def classify(sample,root):
	# check if leaf node
	if root.is_leaf():
		# return prediction
		return root.value
	else:
		# is attribute >= value in question
		if root.match(sample):
			# take right branch
			return classify(sample, root.right)
		else:
			# take left branch
			return classify(sample, root.left)

# Returns average Eval_Metrics for all trees and the standard deviation for these metrics
def trees_metrics(test_sets,trees):
	n = len(test_sets)
	if n != len(trees):
		print("trees_metrics() input invalid")
		quit()

	# build up a list of all data points
	all_confusion = np.empty(shape=(4,4,n))
	all_recall = np.empty(shape=(4,n))
	all_precision = np.empty(shape=(4,n))
	all_f1 = np.empty(shape=(4,n))
	all_cr = np.empty(shape=(n))

	for k in range(n):
		eval = evaluate(test_sets[k],trees[k][0])
		for i in range(4):
			# confusion matrix
			for j in range(4):
				all_confusion[i,j,k] = eval.c_matrix[i,j]
			# recall
			all_recall[i,k] = eval.recall[i]
			# sum precision
			all_precision[i,k] = eval.precision[i]
			# f1-measures
			all_f1[i,k] = eval.f1[i]
		# classification rates
		all_cr[k] = eval.c_rate

	# Avg
	avg_c_matrix = np.average(all_confusion, axis=2)
	# for i in range(4):
	# 	for j in range(4):
	# 		avg_c_matrix = all_confusion[i][j].average()
	sd_recall    = np.std(all_recall, axis=1, dtype=np.float64)
	sd_precision = np.std(all_precision, axis=1, dtype=np.float64)
	sd_f1        = np.std(all_f1, axis=1, dtype=np.float64)
	sd_cr        = np.std(all_cr, dtype=np.float64)

	avg_metrics = Eval_Metrics(avg_c_matrix)

	sd_metrics = Eval_Metrics(avg_c_matrix)
	sd_metrics.store_sd(sd_recall, sd_precision, sd_f1, sd_cr)

	return avg_metrics, sd_metrics

# Returns avg, sd, max height
def average_height(trees):
	n = len(trees)
	heights = np.zeros(shape=(n))
	# store heights in a 1D np array
	for i in range(n):
		heights[i] = trees[i][1]

	return np.average(heights), np.std(heights), np.amax(heights)
