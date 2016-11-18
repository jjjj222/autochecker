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
SEED = 0


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

    test_data(classifier, documents, "train")
    return classifier

#def test_classifier(classifier, feature_set):
#    results = [ classifier.classify(f[0]) for f in feature_set ]
#    correct_results = [ f[1] for f in feature_set ]
#    cm = nltk.ConfusionMatrix(correct_results, results)
#    print cm
#    print "accuracy =", nltk.classify.accuracy(classifier, feature_set)
#    print
#

def test_data(classifier, documents, header=None):
    candidates = get_candidates(documents)
    feature_set = get_feature_set(candidates, ACTIVE_FEATURES)

    results = [ classifier.classify(f[0]) for f in feature_set ]
    correct_results = [ f[1] for f in feature_set ]
    cm = nltk.ConfusionMatrix(correct_results, results)
    print cm
    #print "accuracy =", nltk.classify.accuracy(classifier, feature_set)
    print_info("classifier_accuracy", [nltk.classify.accuracy(classifier, feature_set)], header)
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


    print_info("correction", len(new_mistakes), header)
    print_info("golden_correction", len(new_mistakes), header)
    #print " of correction =", len(new_mistakes)
    #print "# of golden correction =", len(golden_mistakes)

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

    print_info("tp", len(tp), header)
    print_info("fp", len(fp), header)
    print_info("fn", len(fn), header)

    precision, recall, f1 = get_precision_recall_f1(len(tp), len(fp), len(fn))
    print_info("precision", precision, header)
    print_info("recall", recall, header)
    print_info("f1", f1, header)
    #print_value("precision", precision)
    #print_value("recall", recall)
    #print_value("f1", f1)
    print
    #print "precision = %s" % (float(len(tp)) / (len(tp) + len(fp)))
    #print "recall = %s" % (float(len(tp)) / (len(tp) + len(fn)))

    #print "f1 = %s" % (2 * float(len(tp)) / (2 * len(tp) + len(fn) + len(fp)))


    return precision, recall, f1


def dump_mistakes(mistakes):
    for m in mistakes:
        m.dump()
    print


def run_data(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    conlldata.filter_mistakes()


    documents = conlldata.documents
    random.seed(SEED)
    random.shuffle(documents)

    split = len(documents) / 10

    if split == 0:
        split = 1

    train_documents = documents[split:]
    test_documents = documents[:split]

    print_info("train_documents", [d.id for d in train_documents])
    print_info("test_documents", [d.id for d in test_documents])

    classifier = train_classifier(train_documents)
    precision, recall ,f1 = test_data(classifier, test_documents, "test")
    #print_info("test_precision", [precision])
    #print_info("test_recall", [recall])
    #print_info("test_f1", [f1])


def process_parameter(parameter):
    global CLASSIFIER_NAME
    global FEATURE_LIST
    global ACTIVE_FEATURES
    global SEED

    parameter_cid = parameter[0]
    parameter_seed = parameter[1]
    parameter_feature = parameter[2:]

    SEED = int(parameter_seed)
    print_info("seed", SEED)

    CLASSIFIER_NAME = CLASSIFIER_LIST[int(parameter_cid)]
    print_info("classifier", CLASSIFIER_NAME)

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
        create_file_dir(log_file)
        sys.stdout = open(log_file, 'w')
        process_parameter(parameter)

    print_info("git_hash", git_hash)
    print_info("date_time", get_date_time())
    print_info("conll_file", conll_file)
    print_info("ann_file", ann_file)
    print_info("log_file", log_file)
    print_info("parameter", parameter)


    if not check_file_to_read(conll_file):
        return

    run_data(conll_file, ann_file, out_file)
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
