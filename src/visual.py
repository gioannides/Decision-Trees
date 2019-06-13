import numpy as np
import matplotlib.pyplot as plt

# Plot point on the axes (passed by reference) with a given text
def plot_point(point, ax, text):
	ax.text(point[0] - 1, point[1], text,
			ha='center', va='center',
			fontsize=8,
			bbox=dict(boxstyle='round', ec='k', fc='w'))

# Show an interactive visualisation for a given tree and save the visualisation in a given file_name
def visualise_tree(tree, file_name):
	height = tree[1]
	root = 0, height

	fig = plt.figure(figsize=(5, 7), facecolor='w')
	ax = fig.add_axes([0, 0, 1, 1], xticks=[], yticks=[], frameon=False)

	# plot the root node
	plot_point(root, ax, f'[X{tree[0].attribute} >= {tree[0].value}]')

	# plot children
	plot_node(tree[0].left, root, height - 1, ax, False)
	plot_node(tree[0].right, root, height - 1, ax, True)

	plt.show()
	fig.savefig(file_name, dpi=fig.dpi)

# recursive function that plots a node and all of it's children in the correct location on the axes
def plot_node(node, parent_node, depth, ax, is_right):
	# point is horizontal and vertical distance
	width = 2**depth
	if is_right:
		point = parent_node[0] + width, depth
	else:
		point = parent_node[0] - width, depth

	# draw line connection
	ax.plot([point[0], parent_node[0]], [point[1], parent_node[1]], 'b-')

	if node.is_leaf():
		text = f'leaf:{int(node.value)}'
	else:
		text = f'[X{node.attribute} >= {node.value}]'

	plot_point(point, ax, text)

	# plot children nodes
	if node.left:
		plot_node(node.left, point, depth - 1, ax, False)
	if node.right:
		plot_node(node.right, point, depth - 1, ax, True)
