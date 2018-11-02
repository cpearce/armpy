from mypy import api


def test_types():
    files_to_type_check = [
        "apriori.py",
        "armpy.py",
        "datasetreader.py",
        "fptree.py",
        "generaterules.py",
        "index.py",
        "item.py",
        "test_apriori.py",
        "test_fptree.py",
        "test_index.py",
    ]

    result = api.run(files_to_type_check)

    if result[0]:
        print('\nType checking report:\n')
        print(result[0])  # stdout

    if result[1]:
        print('\nError report:\n')
        print(result[1])  # stderr

    print('\nExit status:', result[2])
    assert(result[2] == 0)
