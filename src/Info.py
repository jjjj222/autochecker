#! /usr/bin/python

import sys
import nltk
import itertools
import random
import numpy
import math
#import scipy
#import scipy.stats
from sets import Set

from document import *
from conlldata import *
from myutil import *
from classifier import *
from features import *

def run_data(conll_file, ann_file):
    conlldata = ConllData(conll_file, ann_file)
    conlldata.filter_mistakes()

    mistakes = get_target_mistakes(conlldata.documents)

    #for m in mistakes:
    #    print m.sentence
    #    m.dump()
    #    print

    print_info("mistake_count", len(mistakes))

    candidates = get_candidates(conlldata.documents)
    print_info("candidates_count", len(candidates))


    #documents = conlldata.documents
    #random.seed(SEED)
    #random.shuffle(documents)

    #split = len(documents) / 10

    #if split == 0:
    #    split = 1

    #train_documents = documents[split:]
    #test_documents = documents[:split]

    #print_info("train_documents", [d.id for d in train_documents])
    #print_info("test_documents", [d.id for d in test_documents])

    #classifier = train_classifier(train_documents)

    #test_data(classifier, train_documents, "train")
    #if "show_most_informative_features" in dir(classifier):
    #    classifier.show_most_informative_features()
    #print

    #test_data(classifier, test_documents, "test", True)
    #print_info("test_precision", [precision])
    #print_info("test_recall", [recall])
    #print_info("test_f1", [f1])

def main():
    conll_file = sys.argv[1]
    ann_file = sys.argv[2]

    if not check_file_to_read(conll_file):
        return

    run_data(conll_file, ann_file)

if __name__ == "__main__":
    main()
