#! /usr/bin/python

import sys
import re
from parser import AnnParser
#from myutil import check_file_to_read
from myutil import *
from document import *

class ConllData:
    def __init__(self, conll_file, ann_file):
        self.documents = self._parse_conll(conll_file)
        self.mistakes = self._parse_ann(ann_file)

    def _parse_conll(self, filename):
        results = []

        data = parse_space_separated_file(filename)

        document = None
        for line in data:
            if len(line) == 0:
                continue
            elif len(line) != 9:
                print "Format Error"
                continue

            NID, PID, SID, TOKENID, TOKEN, POS, DPHEAD, DPREL, SYNT = line
            NID = int(NID)
            PID = int(PID)
            SID = int(SID)
            TOKENID = int(TOKENID)

            if document == None or document.get_id() != NID:
                if document != None:
                    results.append(document)
                document = Document(NID)

            word = Word(TOKENID, TOKEN, POS)
            document.add_word(PID, SID, word)

        results.append(document)
        return results

    def _parse_ann(self, filename):
        results = []

        f = open(filename, 'r')
        parser = AnnParser()
        raw = f.read()

        parser.feed(raw)
        results =  parser.get_results()
        return results

    def dump(self):
        for d in self.documents:
            d.dump()


def main():
    data_path = "../data/simple"
    #data_path = "../data/simpleq"
    conll_file_name = "simple.conll"
    ann_file_name = "simple.conll.ann"
    conll_file = "%s/%s" % (data_path, conll_file_name)
    ann_file = "%s/%s" % (data_path, ann_file_name)
    #data_path = "../data/nucle3.2/preprocessed_data"
    #conll_file = "nucle3.2-preprocessed.conll"
    #ann_file = "nucle3.2-preprocessed.conll.ann"
    #print conll_file
    #print sys.argv
    #print "QQ"

    if not check_file_to_read(conll_file):
        return

    data = ConllData(conll_file, ann_file)
    #data.dump()
    #print type(data)

if __name__ == "__main__":
    main()
