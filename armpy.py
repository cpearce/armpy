import csv
import sys
import time
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from fptree import mine_fp_tree
from generaterules import generate_rules
from index import InvertedIndex

def set_to_string(s):
    ss = ""
    for x in sorted(s):
        if ss != "":
            ss += " "
        ss += str(x)
    return ss

def float_between_0_and_1(string):
    value = float(string)
    if value < 0.0 or value > 1.0:
        msg = "%r is not in range [0,1]" % string
        raise ArgumentTypeError(msg)
    return value


def float_gteq_1(string):
    value = float(string)
    if value < 1.0:
        msg = "%r is not in range [1,∞]" % string
        raise ArgumentTypeError(msg)
    return value


def main():
    parser = ArgumentParser(description="Association rule data mining in Python")
    parser.add_argument("--input", dest="input", required=True)
    parser.add_argument("--output", dest="output", required=True)
    parser.add_argument("--min-confidence", dest="min_confidence", type=float_between_0_and_1, required=True)
    parser.add_argument("--min-support", dest="min_support", type=float_between_0_and_1, required=True)
    parser.add_argument("--min-lift", dest="min_lift", type=float_gteq_1, required=True)
    args = parser.parse_args()

    program_start = time.time()
    start = program_start
    print("Mining association rules using FPGrowth...")
    print("Input file: {}".format(args.input))
    print("Output file: {}".format(args.output))
    print("Minimum support: {}".format(args.min_confidence))
    print("Minimum confidence: {}".format(args.min_support))
    print("Minimum lift: {}".format(args.min_lift))

    with open(args.input, newline='') as csvfile:
        transactions = list(csv.reader(csvfile))
        itemsets = list(mine_fp_tree(transactions, args.min_support))
    duration = time.time() - start
    print("fptree mined {} items in {:.2f} seconds".format(len(itemsets), duration))

    start = time.time()
    index = InvertedIndex()
    index.load_csv(args.input)
    duration = time.time() - start
    print("Loaded index for rule generation in {:.2f} seconds".format(duration))

    start = time.time()
    rules = list(generate_rules(itemsets, args.min_confidence, args.min_lift, index))
    duration = time.time() - start
    print("Generated {} rules in {:.2f} seconds".format(len(rules), duration))

    with open(args.output, "w") as f:
        f.write("Antecedent->Consequent,Confidence,Lift,Support")
        for (antecedent,
             consequent,
             confidence,
             lift,
             support) in rules:
            f.write("{} -> {},{:.4f},{:.4f},{:.4f}".
                    format(set_to_string(antecedent), set_to_string(consequent), confidence, lift, support))

    duration = time.time() - program_start
    print("Total runtime {:.2f} seconds".format(duration))

    return 0

if __name__ == "__main__":
    sys.exit(main())