from item import ItemSet
from apriori import apriori
from itertools import chain, combinations
import sys


if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def split_out(item, itemset):
    return [x for x in itemset if x != item],[item]

def calc_stats(support, antecedent, consequent, calculate_support):
    a_sup = calculate_support(antecedent)
    confidence = support / a_sup
    c_sup = calculate_support(consequent)
    lift = support / (a_sup * c_sup)
    return (confidence, lift)

def is_sorted(candidates):
    for i in range(1, len(candidates)):
        if candidates[i-1] > candidates[i]:
            return False
    return True

def prefix_match_len(a, b):
    assert(len(a) == len(b))
    for i in range(len(a)):
        if a[i] != b[i]:
            return i
    return len(a)

def generate_rules_for_itemset(
        itemset,
        calculate_support,
        min_confidence,
        min_lift):

    # Generate rules via appgenrules; combine consquents until all
    # combinations have been tested.
    rules = []
    candidates = []

    # First level candidates are consequents with single items in consequent.
    support = calculate_support(itemset)
    for item in itemset:
        (antecedent, consequent) = split_out(item, itemset)
        (confidence, lift) = calc_stats(support, antecedent, consequent, calculate_support)
        if confidence < min_confidence:
            continue
        if lift >= min_lift:
            rules.append((antecedent, consequent, confidence, lift, support))
        candidates.append(consequent)

    # Create subsequent rules by merging consequents which have size-1 items
    # in common in the consequent.

    k = len(itemset)
    itemset_as_set = set(itemset)
    while len(candidates) > 0 and len(candidates[0]) + 1 < k:
        assert(is_sorted(candidates))
        next_gen = []
        m = len(candidates[0])
        for i1 in range(len(candidates)):
            for i2 in range(i1+1, len(candidates)):
                c1 = candidates[i1]
                c2 = candidates[i2]
                if prefix_match_len(c1, c2) != m-1:
                    # Consequents in the candidates list are sorted, and the
                    # candidates list itself is sorted. So we can stop
                    # testing combinations once our iteration reaches another
                    # candidate that no longer shares an m-1 prefix. Stopping
                    # the iteration here is a significant optimization. This
                    # ensures that we don't generate or test duplicate
                    # rules.
                    break
                consequent = list(sorted(set(c1) | set(c2)))
                antecedent = list(sorted(itemset_as_set - set(consequent)))
                assert(is_sorted(consequent))
                (confidence, lift) = calc_stats(support, antecedent, consequent, calculate_support)
                if confidence < min_confidence:
                    continue
                if lift >= min_lift:
                    rules.append((antecedent, consequent, confidence, lift, support))
                next_gen.append(consequent)
        candidates = next_gen
    return rules


def generate_rules(
        itemsets,
        itemset_counts,
        num_transactions,
        min_confidence,
        min_lift):

    def calculate_support(i):
        key = list(i)
        return itemset_counts[tuple(key)] / num_transactions

    rules = []
    for itemset in filter(lambda i: len(i) > 1, itemsets):
        rules.extend(generate_rules_for_itemset(
            itemset, calculate_support, min_confidence, min_lift))
    return rules