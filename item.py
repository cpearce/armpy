import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

itemNameToId = {}
itemIdToName = {}


def item_id(name):
    if not isinstance(name, str):
        raise TypeError("Item name must be string")
    if name not in itemNameToId:
        itemId = len(itemNameToId) + 1
        itemNameToId[name] = itemId
        itemIdToName[itemId] = name
        return itemId
    else:
        return itemNameToId[name]

def item_str(id):
    return itemIdToName[id]

def ItemSet(lst):
    return frozenset(map(item_id, lst))
