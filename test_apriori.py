from index import InvertedIndex
from apriori import apriori
from item import item_id, ItemSet
from generaterules import generate_rules
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def test_apriori():
    data = ("a,b,c,d,e,f\n"
            "g,h,i,j,k,l\n"
            "z,x\n"
            "z,x\n"
            "z,x,y\n"
            "z,x,y,i\n")

    expectedItemSets = {ItemSet("i"): 2 / 6,
                        ItemSet("z"): 4 / 6,
                        ItemSet("x"): 4 / 6,
                        ItemSet("y"): 2 / 6,
                        ItemSet("xz"): 4 / 6,
                        ItemSet("yz"): 2 / 6,
                        ItemSet("xy"): 2 / 6,
                        ItemSet("xyz"): 2 / 6}

    index = InvertedIndex()
    index.load(data)
    itemsets = apriori(index, 2 / 6)
    assert(len(itemsets) == len(expectedItemSets))
    for itemset in itemsets:
        assert(frozenset(itemset) in expectedItemSets)
    for itemset in itemsets:
        assert(expectedItemSets[frozenset(itemset)] == index.support(itemset))

    print("Itemsets={}".format([i for i in itemsets if len(i) > 1]))

    # (antecedent, consequent, confidence, lift, support)
    expectedRules = {
        (frozenset({item_id("x"), item_id("y")}), frozenset({item_id("z")}), 1, 1.5, 1 / 3),
        (frozenset({item_id("x")}), frozenset({item_id("y")}), 0.5, 1.5, 1 / 3),
        (frozenset({item_id("x")}), frozenset({item_id("z")}), 1, 1.5, 2 / 3),
        (frozenset({item_id("y")}), frozenset({item_id("x")}), 1, 1.5, 1 / 3),
        (frozenset({item_id("y")}), frozenset({item_id("z")}), 1, 1.5, 1 / 3),
        (frozenset({item_id("z"), item_id("x")}), frozenset({item_id("y")}), 0.5, 1.5, 1 / 3),
        (frozenset({item_id("z"), item_id("y")}), frozenset({item_id("x")}), 1, 1.5, 1 / 3),
        (frozenset({item_id("z")}), frozenset({item_id("x")}), 1, 1.5, 2 / 3),
        (frozenset({item_id("z")}), frozenset({item_id("y")}), 0.5, 1.5, 1 / 3),
    }

    itemset_counts = dict(map(lambda i: (tuple(i), index.count(i)), itemsets))
    rules = generate_rules(
        itemsets,
        itemset_counts,
        index.num_transactions,
        0,
        0)

    for (antecedent,
         consequent,
         confidence,
         lift,
         support) in rules:
        print("{}, {} conf={:.4f}, {:.4f}, {:.4f}".
              format(antecedent, consequent, confidence, lift, support))

    assert(len(rules) == len(expectedRules))
    assert(rules == expectedRules)
