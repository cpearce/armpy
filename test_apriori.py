from index import InvertedIndex
from apriori import Apriori
from item import ItemSet


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
    itemsets = Apriori(index, 2 / 6)
    assert(set(expectedItemSets.keys()) == set(itemsets))
    for itemset in itemsets:
        assert(expectedItemSets[itemset] == index.support(itemset))
