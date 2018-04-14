import sys
import os

from Core.Reader import Reader
from Services.Utile import SegmentCalculator
def main():

 path = os.getcwd() + "\\data_files\\heb-pos.gold"
 reader = Reader(path)
 sentence =  reader.read_sentences_from_file()
 segmentCalculator = SegmentCalculator(sentence)
 result = segmentCalculator.calcReliabilityMeasurment()
 print(result)

 
if __name__ == '__main__':
    main()