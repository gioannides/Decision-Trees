from node import Node
from evaluation import evaluate

# Returns pruned trees
def prune_trees(val_sets, trees):
	pruned_trees = []
	traversals = [] # amount of times tree was traversed in pruning procedure
	total_prunes = []
	change_height = []
	for i in range(len(trees)):
		# Prune, then update height
		root, iterations, no_prunes = prune_tree(val_sets[i], trees[i][0])
		height = root.update_height(0)
		tree = root, height
		pruned_trees.append(tree)
		traversals.append(iterations)
		total_prunes.append(no_prunes)
		change_height.append( trees[i][1]-height )
	print("Decrease in max depth (height) per tree")
	print(change_height)
	print("Number of traversals per tree during pruning")
	print(traversals)
	print("Total number of nodes pruned per tree")
	print(total_prunes)
	return pruned_trees

# Returns pruned tree
def prune_tree(val_dataset, root):
	no_nodes_pruned = 0
	iterations = 0
	none_pruned = False
	# Call prune until no nodes are pruned
	while not none_pruned:
		iterations+=1
		count, pruned_root = prune(val_dataset, root, root, root, True, 0)
		if count == 0:
			none_pruned = True
		no_nodes_pruned += count
	return pruned_root, iterations, no_nodes_pruned

# Returns a pruned tree and count = 0, if no nodes have been pruned or count != 0 otherwise.
# left - is curr_node from left branch of parent
def prune(val_dataset, root, parent, curr_node, left, count):
	# iterate recursively till hitting a leaf on both left and right
	if curr_node.left.is_leaf() and curr_node.right.is_leaf():
		# Get reference accuracy
		acc_ref = evaluate(val_dataset, root).c_rate
		# Backup
		_curr_node = curr_node

		# Overwrite
		# Test Left
		curr_node = _curr_node.left
		# Link to parent
		link_parent(parent, curr_node, left)
		acc_left = evaluate(val_dataset, root).c_rate

		# Test Right
		curr_node = _curr_node.right
		# Link to parent
		link_parent(parent, curr_node, left)
		acc_right = evaluate(val_dataset, root).c_rate

		# Compare
		if acc_left >= acc_ref:
			# Question becomes left leaf
			curr_node = _curr_node.left
			count += 1
		elif acc_right >= acc_ref:
			# Question becomes right leaf
			curr_node = _curr_node.right
			count += 1
		else:
			curr_node = _curr_node
		# Commit to parent
		link_parent(parent, curr_node, left)

	else:
		# Check if left is a leaf node
		if not curr_node.left.is_leaf():
			# Search left
			count, root = prune(val_dataset, root, curr_node, curr_node.left, True, count)

		# Check if right is a leaf node
		if not curr_node.right.is_leaf():
			# Search right
			count, root = prune(val_dataset, root, curr_node, curr_node.right, False, count)

	return count, root

# link curr_node to the correct parent (passed by reference)
def link_parent(parent, curr_node, left):
	if left:
		parent.left = curr_node
	else:
		parent.right = curr_node
