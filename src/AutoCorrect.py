#! /usr/bin/python

import sys
#import re
from conlldata import ConllData
from myutil import *


def parse_data(conll_file, ann_file):
    conlldata = ConllData(conll_file, ann_file)
    c = conlldata.get_ArtOrDet_candidates()

    print c

    #conlldata.dump()
        #for s in self.sentences:
        #    result.append( s.get_ArtOrDet_candidates() )
    #conlldata.concordance("the")
    #c = []
    #for d in conlldata:
    #    c.append( d.get_ArtOrDet_candidates() )



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

    parse_data(conll_file, ann_file)
    #print type(data)

if __name__ == "__main__":
    main()
