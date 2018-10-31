from index import InvertedIndex
from item import item_id


def test_InvertedIndex():
    data = ("a,b,c,d,e,f\n"
            "g,h,i,j,k,l\n"
            "z,x\n"
            "z,x\n"
            "z,x,y\n"
            "z,x,y,i\n")
    index = InvertedIndex()
    index.load(data)
    assert(index.support({item_id("a")}) == 1 / 6)
    assert(index.support({item_id("b")}) == 1 / 6)
    assert(index.support({item_id("c")}) == 1 / 6)
    assert(index.support({item_id("d")}) == 1 / 6)
    assert(index.support({item_id("e")}) == 1 / 6)
    assert(index.support({item_id("f")}) == 1 / 6)
    assert(index.support({item_id("h")}) == 1 / 6)
    assert(index.support({item_id("i")}) == 2 / 6)
    assert(index.support({item_id("j")}) == 1 / 6)
    assert(index.support({item_id("k")}) == 1 / 6)
    assert(index.support({item_id("l")}) == 1 / 6)
    assert(index.support({item_id("z")}) == 4 / 6)
    assert(index.support({item_id("x")}) == 4 / 6)
    assert(index.support({item_id("y")}) == 2 / 6)

    sup_zx = index.support({item_id("z"), item_id("x")})
    assert(sup_zx == 4 / 6)

    sup_zxy = index.support({item_id("z"), item_id("x"), item_id("y")})
    assert(sup_zxy == 2 / 6)

    sup_zxyi = index.support({item_id("z"), item_id("x"), item_id("y"), item_id("i")})
    assert(sup_zxyi == 1 / 6)
