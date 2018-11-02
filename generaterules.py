from item import ItemSet
from apriori import apriori
from itertools import chain, combinations
from typing import Callable, Dict, List, Tuple
import sys


if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def split_out(item: int, itemset: List[int]) -> Tuple[List[int], List[int]]:
    return [x for x in itemset if x != item], [item]


def calc_stats(
        support: float,
        antecedent: List[int],
        consequent: List[int],
        calculate_support: Callable[[List[int]], float]
    ) -> Tuple[float, float]:
    a_sup: float = calculate_support(antecedent)
    confidence: float = support / a_sup
    c_sup: float = calculate_support(consequent)
    lift: float = support / (a_sup * c_sup)
    return (confidence, lift)


def is_sorted(candidates) -> bool:
    for i in range(1, len(candidates)):
        if candidates[i-1] > candidates[i]:
            return False
    return True


def prefix_match_len(a: List[int], b: List[int]) -> int:
    assert(len(a) == len(b))
    for i in range(len(a)):
        if a[i] != b[i]:
            return i
    return len(a)


def generate_rules_for_itemset(
        itemset: List[int],
        calculate_support: Callable[[List[int]], float],
        min_confidence: float,
        min_lift: float
    ) -> List[Tuple[List[int], List[int], float, float, float]]:

    # Generate rules via appgenrules; combine consquents until all
    # combinations have been tested.
    rules: List[Tuple[List[int], List[int], float, float, float]] = []
    candidates: List[List[int]] = []

    # First level candidates are consequents with single items in consequent.
    support = calculate_support(itemset)
    for item in itemset:
        (antecedent, consequent) = split_out(item, itemset)
        (confidence, lift) = calc_stats(
            support, antecedent, consequent, calculate_support)
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
                (confidence, lift) = calc_stats(
                    support, antecedent, consequent, calculate_support)
                if confidence < min_confidence:
                    continue
                if lift >= min_lift:
                    rules.append(
                        (antecedent, consequent, confidence, lift, support))
                next_gen.append(consequent)
        candidates = next_gen
    return rules


def generate_rules(
        itemsets: List[List[int]],
        itemset_counts: Dict[Tuple[int, ...], int],
        num_transactions: int,
        min_confidence: float,
        min_lift: float
    ) -> List[Tuple[List[int], List[int], float, float, float]]:

    def calculate_support(i: List[int]) -> float:
        key = list(i)
        return itemset_counts[tuple(key)] / num_transactions

    rules = []
    for itemset in filter(lambda i: len(i) > 1, itemsets):
        rules.extend(generate_rules_for_itemset(
            itemset, calculate_support, min_confidence, min_lift))
    return rules
