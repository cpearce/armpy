from fptree import FPTree
from fptree import mine_fp_tree
from fptree import construct_initial_tree
from apriori import apriori
from index import InvertedIndex
from item import Item
from item import ItemSet
import time
import csv
import sys


def test_basic_sanity():
    # Basic sanity check of know resuts.
    transactions = [
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
    ]
    expected_itemsets = {
        ItemSet("e"), ItemSet("de"), ItemSet("ade"), ItemSet("ce"),
        ItemSet("ae"),

        ItemSet("d"), ItemSet("cd"), ItemSet("bcd"), ItemSet("acd"),
        ItemSet("bd"), ItemSet("abd"), ItemSet("ad"),

        ItemSet("c"), ItemSet("bc"), ItemSet("abc"), ItemSet("ac"),

        ItemSet("b"), ItemSet("ab"),

        ItemSet("a"),
    }

    itemsets = mine_fp_tree(transactions, 2 / len(transactions))
    assert(set(itemsets) == expected_itemsets)


def test_tree_sorting():
    transactions = [
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
    ]

    expected_tree = construct_initial_tree(transactions)
    assert(expected_tree.is_sorted())

    tree = FPTree()
    for transaction in transactions:
        # Insert reversed, since lexicographical order is already decreasing
        # frequency order in this example.
        tree.insert(map(Item, reversed(transaction)))
    assert(str(expected_tree) != str(tree))
    tree.sort()
    assert(tree.is_sorted())
    assert(str(expected_tree) == str(tree))

    datasets = [
        "datasets/UCI-zoo.csv",
        "datasets/mushroom.csv",
        # "datasets/BMS-POS.csv",
        # "datasets/kosarak.csv",
    ]

    for csvFilePath in datasets:
        print("Loading FPTree for {}".format(csvFilePath))
        start = time.time()
        tree = FPTree()
        with open(csvFilePath, newline='') as csvfile:
            for line in list(csv.reader(csvfile)):
                # Insert sorted lexicographically
                transaction = sorted(map(Item, line))
                tree.insert(transaction)
        duration = time.time() - start
        print("Loaded in {:.2f} seconds".format(duration))
        print("Sorting...")
        start = time.time()
        tree.sort()
        duration = time.time() - start
        print("Sorting took {:.2f} seconds".format(duration))
        assert(tree.is_sorted())


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
        with open(csvFilePath, newline='') as csvfile:
            transactions = list(csv.reader(csvfile))
            fptree_itemsets = mine_fp_tree(transactions, min_support)
        fptree_duration = time.time() - start
        print(
            "fp_growth complete. Generated {} itemsets in {:.2f} seconds".format(
                len(fptree_itemsets),
                fptree_duration))

        if set(fptree_itemsets) == set(apriori_itemsets):
            print("SUCCESS({}): Apriori and fptree results match".format(csvFilePath))
        else:
            print("FAIL({}): Apriori and fptree results differ!".format(csvFilePath))
        assert(set(fptree_itemsets) == set(apriori_itemsets))

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
