class Node():
	def __init__(self, value , attr):
		# label or split value
		self.value     = value
		# column # of attribute (0-6)
		self.attribute = attr
		self.left      = None
		self.right     = None

	def print(self, c):
		print(str(self.value) + " : " + str(self.attribute) + ". At depth " +str(c))
		if not self.left == None:
			print("Left branch")
			self.left.print(c+1)
		if not self.right == None:
			print("Right branch")
			self.right.print(c+1)

	# Methods if Node is a Question
	def set_branches(self, left, right):
		self.left      = left
		self.right     = right

	def match(self, example):
		# Compare the feature value in an example to the
		# feature value in this question.
		val = example[self.attribute]
		# False - val <
		# True  = val >=
		return val >= self.value

	# Methods is Node is a Leaf
	# Returns boolean if Node is a leaf node
	def is_leaf(self):
		# maybe self.attr == None ?
		return (self.left == None) and (self.right == None)

	# After pruning, height updates
	# Call on root - pass in 0
	# Returns new height of tree
	def update_height(self, height=0):
		if self.is_leaf():
			return height
		else:
			lheight = self.left.update_height(height+1)
			rheight = self.right.update_height(height+1)
			return max(lheight, rheight)
