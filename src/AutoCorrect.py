#! /usr/bin/python

import sys
import nltk
import itertools
import random
from sets import Set

from document import *
from conlldata import *
from myutil import *
from classifier import *
from features import *

CLASSIFIER_LIST = [
    "majority",
    "naive",
    "decision_tree",
    "maxent"
]

CLASSIFIER_NAME = "maxent"
ACTIVE_FEATURES = set(FEATURE_LIST)


def write_out_correct(conlldata, out_file):
    f = open(out_file, 'w')
    for s in conlldata.sentences():
        f.write(s.correct_text("ArtOrDet"))
        f.write('\n')
        print s.correct_text("ArtOrDet")
    f.close()

def train_classifier(documents):
    candidates = get_candidates(documents)
    feature_set = get_feature_set(candidates, ACTIVE_FEATURES)

    #majority
    classifier = MajorityClassifier()
    classifier.train(feature_set)

    #naive
    if CLASSIFIER_NAME == "naive":
        classifier = nltk.NaiveBayesClassifier.train(feature_set)

    #decision tree
    if CLASSIFIER_NAME == "decision_tree":
        classifier = nltk.DecisionTreeClassifier.train(feature_set)

    #maxent
    if CLASSIFIER_NAME == "maxent":
        classifier = nltk.MaxentClassifier.train(feature_set)

    test_data(classifier, documents)

    return classifier

#def test_classifier(classifier, feature_set):
#    results = [ classifier.classify(f[0]) for f in feature_set ]
#    correct_results = [ f[1] for f in feature_set ]
#    cm = nltk.ConfusionMatrix(correct_results, results)
#    print cm
#    print "accuracy =", nltk.classify.accuracy(classifier, feature_set)
#    print
#

def test_data(classifier, documents):
    candidates = get_candidates(documents)
    feature_set = get_feature_set(candidates, ACTIVE_FEATURES)

    #feature_set = [(artOrDet_features(c.word), c.get_determiner_class()) for c in candidates]
    results = [ classifier.classify(f[0]) for f in feature_set ]
    correct_results = [ f[1] for f in feature_set ]
    cm = nltk.ConfusionMatrix(correct_results, results)
    print cm
    print "accuracy =", nltk.classify.accuracy(classifier, feature_set)
    print

    #for r, cr, c in itertools.izip(results, correct_results, candidates):
    #    if r != cr:
    #        print "(%s) <-> [%s]" % (r, cr)
    #        c.dump()
    #return



    new_mistakes = []
    for r, c in itertools.izip(results, candidates):
        m = c.generate_mistake(r)
        if m:
            new_mistakes.append(m)


    #return
    golden_mistakes = get_target_mistakes(documents)


    print "# of correction =", len(new_mistakes)
    print "# of golden correction =", len(golden_mistakes)

    new_mistakes_set = Set(new_mistakes)
    golden_mistakes_set = Set(golden_mistakes)

    tp = []
    fp = []
    fn = []

    for m in golden_mistakes:
        if m in new_mistakes_set:
            tp.append(m)
        else:
            fn.append(m)

    for m in new_mistakes:
        if not m in golden_mistakes_set:
            fp.append(m)

    print "tp =", len(tp)
    print "fp =", len(fp)
    #dump_mistakes(fp)

    print "fn =", len(fn)
    #dump_mistakes(fn)

    print "precision = %s" % (float(len(tp)) / (len(tp) + len(fp)))
    print "recall = %s" % (float(len(tp)) / (len(tp) + len(fn)))

    print "f1 = %s" % (2 * float(len(tp)) / (2 * len(tp) + len(fn) + len(fp)))
    print


def dump_mistakes(mistakes):
    for m in mistakes:
        m.dump()
    print


def run_data(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    conlldata.filter_mistakes()


    documents = conlldata.documents
    random.seed(1)
    random.shuffle(documents)

    split = len(documents) / 10

    if split == 0:
        split = 1

    train_documents = documents[split:]
    test_documents = documents[:split]

    print_info("train_documents", [d.id for d in train_documents])
    print_info("test_documents", [d.id for d in test_documents])

    classifier = train_classifier(train_documents)
    test_data(classifier, test_documents)


def process_parameter(parameter):
    global CLASSIFIER_NAME
    global FEATURE_LIST
    global ACTIVE_FEATURES

    parameter_cid = parameter[0]
    parameter_feature = parameter[1:]


    CLASSIFIER_NAME = CLASSIFIER_LIST[int(parameter_cid)]
    print_info("classifier", [CLASSIFIER_NAME])

    active_features_list = []
    for i in range(len(parameter_feature)):
        if parameter_feature[i] == '1':
            active_features_list.append( FEATURE_LIST[i] )

    print_info("active_features", active_features_list)
    ACTIVE_FEATURES = set(active_features_list)


def main():
    git_hash = get_git_hash()
    conll_file = sys.argv[1]
    ann_file = sys.argv[2]
    out_file = sys.argv[3]
    log_file = ""
    parameter = None

    case_name = os.path.basename(conll_file)
    case_name = os.path.splitext(case_name)[0]

    if (len(sys.argv) > 4):
        parameter = sys.argv[4]

    if parameter != None:
        log_file = get_log_file_name(case_name, parameter)
        #create_file_dir(log_file)
        #sys.stdout = open(log_file, 'w')
        process_parameter(parameter)

    print_info("git_hash", [git_hash])
    print_info("conll_file", [conll_file])
    print_info("ann_file", [ann_file])
    print_info("log_file", [log_file])
    print_info("parameter", [parameter])


    if not check_file_to_read(conll_file):
        return

    run_data(conll_file, ann_file, out_file)
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
