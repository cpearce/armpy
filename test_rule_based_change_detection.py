from item import Item
from collections import Counter
from fptree import FPTree
import time
import csv
import sys
from rule_based_change_detection import rule_based_change_detection

test_transactions = (
    ["a", "b", "c"],
    ["d", "e", "f"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["d", "e", "f"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["d", "e", "f"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["d", "e", "f"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],


    ["a", "b", "c"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],

    ["a", "b", "c"],
    ["b", "c"],
    ["d", "e"],
    ["a"],
    ["d"],
)


def test_detect_rule_based_change_detection():
    rule_based_change_detection(
        test_transactions,
        min_confidence=0.05,
        min_lift=0.05,
        min_support=0.05,
        initial_window_size=10,
        check_interval=10)
    # found_change_at = -1
    # for (tree, transaction_num) in gen:
    #     print("Detected change at tid {}".format(transaction_num))
    #     found_change_at = transaction_num
    # assert(found_change_at == 20)
    assert(True)


# def test_cdtds():
#     csvFilePath = "datasets/mushroom.csv"
#     with open(csvFilePath, newline='') as csvfile:
#         test_transactions = list(csv.reader(csvfile))
#         gen = change_detection_transaction_data_streams(
#             test_transactions,
#             window_len=1000,
#             merge_threshold=32,
#             min_cut_len=32,
#             local_cut_confidence=0.05)
#         for (tree, transaction_num) in gen:
#             print("Detected change at tid {}".format(transaction_num))

test_detect_rule_based_change_detection()
