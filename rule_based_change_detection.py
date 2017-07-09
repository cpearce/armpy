from item import Item
from index import InvertedIndex
import sys
from fptree import mine_fp_tree
from generaterules import generate_rules
from generaterules import is_closed_itemset
from generaterules import powerset
from collections import Counter
import scipy.stats

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def rule_based_change_detection(
        transactions,
        min_confidence,
        min_lift,
        min_support,
        initial_window_size,
        check_interval):
    assert(min_confidence > 0 and min_confidence <= 1)
    assert(min_lift > 0 and min_lift <= 1)
    assert(min_support > 0 and min_support <= 1)
    window = []
    num_transaction = 0
    next_check = initial_window_size + check_interval
    closed_itemsets = dict()
    for transaction in transactions: #[list(map(Item, t)) for t in transactions]:
        num_transaction += 1
        window.append(transaction)
        if num_transaction < initial_window_size:
            continue
        elif num_transaction == initial_window_size:
            # Do inital mine.
            print("window:")
            print(window)
            itemsets = mine_fp_tree(window, min_support)
            index = InvertedIndex()
            for txn in [list(map(Item, t)) for t in window]:
                index.add(txn)
            rules = generate_rules(itemsets, min_confidence, min_lift, index)
            for (antecedent, consequent, confidence, lift, support) in rules:
                print("rule {} -> {}".format(antecedent, consequent))
                itemset = antecedent | consequent
                if not is_closed_itemset(itemset, index):
                    continue
                closed_itemsets[tuple(sorted(list(itemset)))] = support
            window = []
            continue

        if num_transaction < next_check:
            continue

        print("closed_itemsets=")
        print(closed_itemsets)

        # Check if supports of closed itemsets has changed.

        # First figure out the frequencies of the closed itemsets in the
        # window of unmined transactions.
        new_closed_itemsets_count = Counter()
        for t in window:
            for subset in powerset(t):
                itemset = tuple(sorted(list(subset)))
                if itemset in closed_itemsets:
                    new_closed_itemsets_count[itemset] += 1

        old = []
        new = []

        for item in closed_itemsets.keys():
            old.append(closed_itemsets[item])
            new.append(new_closed_itemsets_count[item] / len(window))

        (statistic, pvalue) = scipy.stats.ks_2samp(old, new)
        print("ks_2samp=({},{})".format(statistic, pvalue))
        if pvalue < 0.05:
            # Change detected!
            print("Change detected at transaction_num={}".format(transaction_num))

        next_check = num_transaction + check_interval
        window = []




