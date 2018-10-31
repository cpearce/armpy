from item import item_id

class DatasetReader:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def __iter__(self):

        def tokenize(line):
            return map(lambda x: x.strip(), line.split(","))

        def itemize(tokens):
            return map(item_id, tokens)

        return map(itemize, map(tokenize, open(self.csv_file_path)))