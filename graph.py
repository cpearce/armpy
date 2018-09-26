from item import Item
from item import ItemSet
from fptree import FPTree
from fptree import FPNode

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

class Grapher:
    def __init__(self, filename):
        self.filename = filename
        self.child_graphs = dict()

    def add(self, parent, path, fptree):
        graph_nodes = []
        self.add_nodes(path, fptree.root, graph_nodes)
        if parent not in self.child_graphs:
            self.child_graphs[parent] = []
        self.child_graphs[parent].append((path, graph_nodes))

    def add_nodes(self, path, tree_node, graph_nodes):
        id = "root" if tree_node.is_root()
            else path + "_" + str(tree_node.item)
        label = "root" if tree_node.is_root()
            else (str(tree_node.item) + ":" + str(item.count))
        children = map(lambda n: id + "_" + n.id, tree_node.children)
        graph_nodes.append((id, label, children))
        for child in tree_node.children:
            add_nodes(self, id, child, graph_nodes)

    def write(self):
        with open(args.output, "w") as f:
            f.write("graph {")
            cluster_num = 0
            for parent_id in self.child_graphs:
                (path, nodes) = self.child_graphs[parent_id]:
                f.write("\tsubgraph cluster_" + str(cluster_num) + " {")
                f.write("\t\tlabel=\"" + path + "\";")
                for (id, label, child_ids) in nodes {
                    f.write("\t\tid -- {" + " " .join(child_ids) + " }");
                }
                f.write("\t"}")
                cluster_num += 1
            f.write("}")