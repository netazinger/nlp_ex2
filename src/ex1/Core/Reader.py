
import re

class Reader:
    def __init__(self, path):
        self.path = path
    
    def read_sentences_from_file(self):
         with open(self.path, "r") as f:
             return [re.split("\s+", line.rstrip('\n')) for line in f]
