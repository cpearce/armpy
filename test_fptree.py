from collections import Counter
from fptree import FPTree
from fptree import mine_fp_tree
from fptree import construct_initial_tree
from fptree import count_item_frequency_in
from fptree import sort_transaction
from apriori import apriori
from index import InvertedIndex
from item import Item
from item import ItemSet
from datasetreader import DatasetReader
import time
import sys


test_transactions = list(map(lambda t: list(map(Item, t)), [
    ["a", "b"],
    ["b", "c", "d"],
    ["a", "c", "d", "e"],
    ["a", "d", "e"],
    ["a", "b", "c"],
    ["a", "b", "c", "d"],
    ["a"],
    ["a", "b", "c"],
    ["a", "b", "d"],
    ["b", "c", "e"],
]))


def test_basic_sanity():
    # Basic sanity check of know resuts.
    expected_itemsets = {
        ItemSet("e"), ItemSet("de"), ItemSet("ade"), ItemSet("ce"),
        ItemSet("ae"),

        ItemSet("d"), ItemSet("cd"), ItemSet("bcd"), ItemSet("acd"),
        ItemSet("bd"), ItemSet("abd"), ItemSet("ad"),

        ItemSet("c"), ItemSet("bc"), ItemSet("abc"), ItemSet("ac"),

        ItemSet("b"), ItemSet("ab"),

        ItemSet("a"),
    }

    (itemsets, _, _) = mine_fp_tree(
        test_transactions, 2 / len(test_transactions))
    print("expected= {}".format(expected_itemsets))
    print("observed= {}".format(itemsets))
    assert(len(itemsets) == len(expected_itemsets))
    for itemset in [frozenset(list(x)) for x in itemsets]:
        assert(itemset in expected_itemsets)


def test_stress():
    datasets = [
        ("datasets/UCI-zoo.csv", 0.3),
        ("datasets/mushroom.csv", 0.4),
        # ("datasets/BMS-POS.csv", 0.05),
        # ("datasets/kosarak.csv", 0.05),
    ]

    for (csvFilePath, min_support) in datasets:
        # Run Apriori and FP-Growth and assert both have the same results.
        print("Running Apriori for {}".format(csvFilePath))
        start = time.time()
        index = InvertedIndex()
        index.load_csv(csvFilePath)
        apriori_itemsets = apriori(index, min_support)
        apriori_duration = time.time() - start
        print(
            "Apriori complete. Generated {} itemsets in {:.2f} seconds".format(
                len(apriori_itemsets),
                apriori_duration))

        print("Running FPTree for {}".format(csvFilePath))
        start = time.time()
        (fptree_itemsets, _, _) = mine_fp_tree(
            DatasetReader(csvFilePath), min_support)
        fptree_duration = time.time() - start
        print(
            "fp_growth complete. Generated {} itemsets in {:.2f} seconds".format(
                len(fptree_itemsets),
                fptree_duration))

        assert(len(fptree_itemsets) == len(apriori_itemsets))
        for itemset in [list(x) for x in fptree_itemsets]:
            assert(itemset in apriori_itemsets)

        if apriori_duration > fptree_duration:
            print(
                "FPTree was faster by {:.2f} seconds".format(
                    apriori_duration -
                    fptree_duration))
        else:
            print(
                "Apriori was faster by {:.2f} seconds".format(
                    fptree_duration -
                    apriori_duration))
        print("")

