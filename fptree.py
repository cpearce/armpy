from collections import Counter
from collections import deque
from collections import defaultdict
from apriori import apriori
from index import InvertedIndex
from item import Item
from item import ItemSet
import time
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


class FPNode:
    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        # Number of paths which include this node.
        self.count = count
        self.children = {}
        self.parent = parent

    def is_root(self):
        return self.parent is None

    def __str__(self, level=0):
        ret = ("[root]" if self.is_root()
               else " " * level + str(self.item) + ":" + str(self.count))
        ret += "\n"
        # Print out the child nodes in decreasing order of count, tie break on
        # lexicographical order. As with sort_transaction() below, we achieve
        # this by relying on the fact that python's sort is stable, so we
        # sort first lexicographically, and again by count.
        children = sorted(self.children.values(), key=lambda node: node.item)
        children = sorted(children, key=lambda node: node.count, reverse=True)
        for node in children:
            ret += node.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.__str__()


class FPTree:
    def __init__(self):
        self.root = FPNode()
        self.header = defaultdict(list)
        self.item_count = Counter()

    def insert(self, transaction, count=1):
        assert(count > 0)
        parent = self.root
        parent.count += count
        for item in transaction:
            self.item_count[item] += count
            if item not in parent.children:
                node = FPNode(item, count, parent)
                parent.children[item] = node
                parent = node
                self.header[item].append(parent)
            else:
                parent = parent.children[item]
                parent.count += count


    def __str__(self):
        return "(" + str(self.root) + ")"

def path_to_root(node):
    path = []
    while not node.is_root():
        path += [node.item]
        node = node.parent
    return path


def construct_conditional_tree(tree, item):
    conditional_tree = FPTree()
    for node in tree.header[item]:
        path = path_to_root(node.parent)
        conditional_tree.insert(reversed(path), node.count)
    return conditional_tree


def first_child(node):
    return list(node.children.values())[0]


def fp_growth(
        tree,
        min_count,
        path,
        path_count,
        itemsets,
        itemset_counts,
        maximal_only=False):
    # For each item in the tree that is frequent, in increasing order
    # of frequency...
    for item in sorted(
            tree.item_count.keys(),
            key=lambda i: tree.item_count[i]):
        if tree.item_count[item] < min_count:
            # Item is no longer frequent on this path, skip.
            continue

        # Build conditional tree of all patterns in this tree which start
        # with this item.
        conditional_tree = construct_conditional_tree(tree, item)
        itemset = path + [item]
        itemset.sort()
        new_path_count = conditional_tree.root.count
        fp_growth(
            conditional_tree,
            min_count,
            itemset,
            new_path_count,
            itemsets,
            itemset_counts,
            maximal_only)

        # Need to store the support of this itemset, so we
        # can look it up during rule generation later on.
        itemset_key = tuple(itemset)
        assert(itemset_key not in itemset_counts)
        itemset_counts[itemset_key] = new_path_count

        itemsets.append(itemset)

def mine_fp_tree(transactions, min_support):
    (tree, num_transactions) = construct_initial_tree(transactions, min_support)
    min_count = min_support * num_transactions
    itemsets = []
    itemset_counts = dict()
    fp_growth(
        tree,
        min_count,
        [],
        num_transactions,
        itemsets,
        itemset_counts)
    return (itemsets, itemset_counts, num_transactions)


def sort_transaction(transaction, frequency):
    # Sorts by non-increasing item frequency. We need the sort to tie
    # break consistently; so that when two items have the same frequency,
    # we always sort them into the same order. This is so that when we're
    # sorting the trees and we re-insert sorted paths, that the path
    # overlap in a consistent way. We achieve this ordering by sorting
    # twice; once lexicographically, and then a second time in order of
    # frequency. This works because Python's sort is stable; items that
    # compare equal aren't permuted.
    transaction = sorted(transaction)
    if frequency is None:
        return transaction
    if not isinstance(frequency, Counter):
        raise TypeError("frequency must be Counter")
    return sorted(transaction, key=lambda item: frequency[item], reverse=True)


def count_item_frequency_in(transactions):
    frequency = Counter()
    num_transactions = 0
    for transaction in transactions:
        num_transactions += 1
        for item in transaction:
            frequency[item] += 1
    return (frequency, num_transactions)


def construct_initial_tree(transactions, min_support):
    (frequency, num_transactions) = count_item_frequency_in(transactions)
    min_count = num_transactions * min_support
    tree = FPTree()
    for transaction in transactions:
        # Remove infrequent items from transaction. They cannot contribute to
        # producing frequent itemsets, and just slow down the tree algorithms.
        transaction = filter(
            lambda item: frequency[item] >= min_count,
            transaction)
        tree.insert(sort_transaction(transaction, frequency))
    return (tree, num_transactions)
