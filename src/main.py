#!/usr/bin/python

import numpy as np

from node import Node
import train
import evaluation
import pruning
import visual

# Returns lists for training, validation and test datasets
# each lists has k*k-1 2D numpy arrays
# k*k-1 - k-1 permutations per fold
# k = number of folds
def split_dataset(dataset, k):
	# 10-fold split - k-1,1,1
	training_sets = []
	validation_sets = []
	test_sets = []

	# 10 times - test-fold changes
	for i in range(k):
		# split into 10 folds
		_dataset = dataset
		folds = []
		split_size = len(dataset) / k
		for _ in range(k):
			fst, snd = train.partition(split_size , _dataset)
			folds.append(fst)
			_dataset = snd

		# create 9 total sets of train,val, test
		for j in range(k-1):
			inner_folds = folds.copy()

			# test set is ith fold
			test_sets.append( inner_folds.pop(i) )

			# validation set fold
			validation_sets.append( inner_folds.pop(j) )

			t_fold = inner_folds.pop(0)
			for _ in range(len(inner_folds)):
				t_fold = np.vstack( (t_fold, inner_folds.pop(0)) )

			training_sets.append(t_fold)

	return training_sets, validation_sets, test_sets

def main():
	# Load data
	clean_file = 'src/WIFI_db/clean_dataset.txt'
	noisy_file = 'src/WIFI_db/noisy_dataset.txt'
	cleanDS = np.loadtxt(clean_file)
	noisyDS = np.loadtxt(noisy_file)

	# Shuffle datasets
	np.random.shuffle(cleanDS)
	np.random.shuffle(noisyDS)

	# Create data sets
	print("Splitting datasets (10-fold).")
	clean_train_sets, clean_val_sets, clean_test_sets = split_dataset(cleanDS, 10)
	noisy_train_sets, noisy_val_sets, noisy_test_sets = split_dataset(noisyDS, 10)

	#===============================================================================
	#===============================================================================
	# Train
	print("Training Clean trees...\n")
	# contains (root, height) for trained trees
	clean_trees = train.cross_validation_train(clean_train_sets)
	print("All Clean trees trained.")
	# Height Stats
	clean_height_stats = evaluation.average_height(clean_trees)
	print("Average height of Clean trees = \t" + str(clean_height_stats[0]))
	print("Standard deviation of Clean trees height = \t" + str(clean_height_stats[1]))
	print("Max height of Clean trees = \t" + str(clean_height_stats[2]))
	print("\n")

	print("Training Noisy trees...\n")
	# contains (root, height) for trained trees
	noisy_trees = train.cross_validation_train(noisy_train_sets)
	print("All Noisy trees trained.")
	# Height Stats
	noisy_height_stats = evaluation.average_height(noisy_trees)
	print("Average height of Noisy trees = \t" + str(noisy_height_stats[0]))
	print("Standard deviation of Noisy trees height = \t" + str(noisy_height_stats[1]))
	print("Max height of Noisy trees = \t" + str(noisy_height_stats[2]))
	print("\n\n")

	#===============================================================================
	# Evaluate with test sets before pruning
	print("Pre-pruning test metrics.")
	print("Now testing Clean trees with test sets\n")
	clean_metrics = evaluation.trees_metrics(clean_test_sets, clean_trees)
	print("Average metrics:")
	print(str(clean_metrics[0]))
	print("Standard deviation")
	print(str(clean_metrics[1]))
	print("\n")

	print("Now testing Noisy trees with test sets\n")
	noisy_metrics = evaluation.trees_metrics(noisy_test_sets, noisy_trees)
	print("Average metrics:")
	print(str(noisy_metrics[0]))
	print("Standard deviation")
	print(str(noisy_metrics[1]))
	print("\n\n")

	#===============================================================================
	# Prune
	print("Pruning Clean trees")
	clean_trees_pruned = pruning.prune_trees(clean_val_sets, clean_trees)
	# Height Stats
	clean_height_stats = evaluation.average_height(clean_trees_pruned)
	print("Average height of Clean trees = \t" + str(clean_height_stats[0]))
	print("Standard deviation of Clean trees height = \t" + str(clean_height_stats[1]))
	print("Max height of Clean trees = \t" + str(clean_height_stats[2]))
	print("\n")

	print("Pruning Noisy trees")
	noisy_trees_pruned = pruning.prune_trees(noisy_val_sets, noisy_trees)
	# Height Stats
	noisy_height_stats = evaluation.average_height(noisy_trees_pruned)
	print("Average height of Noisy trees = \t" + str(noisy_height_stats[0]))
	print("Standard deviation of Noisy trees height = \t" + str(noisy_height_stats[1]))
	print("Max height of Noisy trees = \t" + str(noisy_height_stats[2]))
	print("\n\n")

	#===============================================================================
	# Evaluate with test sets after pruning
	print("Post-pruning validation metrics.")
	print("Now testing Clean trees with test sets\n")
	clean_metrics = evaluation.trees_metrics(clean_test_sets, clean_trees_pruned)
	print("Average metrics:")
	print(str(clean_metrics[0]))
	print("Standard deviation")
	print(str(clean_metrics[1]))
	print("\n")

	print("Now testing Noisy trees with test sets\n")
	noisy_metrics = evaluation.trees_metrics(noisy_test_sets, noisy_trees_pruned)
	print("Average metrics:")
	print(str(noisy_metrics[0]))
	print("Standard deviation")
	print(str(noisy_metrics[1]))
	print("\n\n")

	#===============================================================================
	# # Visualize Tree
	# # Uncomment to train, and then visulaize clean and dirty trees before and after pruning
	# # now comment everything from lines 68 to 147
	# noisy_tree = train.decision_tree_learning(noisy_train_sets[0], 0)
	# visual.visualise_tree(noisy_tree, "noisy_tree.png")

	# noisy_tree_pruned, _, _ = pruning.prune_tree(noisy_val_sets[0], noisy_tree[0])
	# visual.visualise_tree((noisy_tree_pruned, noisy_tree_pruned.update_height(0)), "noisy_tree_pruned.png")

	# clean_tree = train.decision_tree_learning(clean_train_sets[0], 0)
	# visual.visualise_tree(clean_tree, "clean_tree.png")

	# clean_tree_pruned, _, _ = pruning.prune_tree(clean_val_sets[0], clean_tree[0])
	# visual.visualise_tree((clean_tree_pruned, clean_tree_pruned.update_height(0)), "clean_tree_pruned.png")

if __name__ == '__main__':
	main()