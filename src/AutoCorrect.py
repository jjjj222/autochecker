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

CLASSIFIER_LIST = [
    "majority",
    "naive",
    "decision_tree",
    "maxent"
]

#CLASSIFIER_NAME = "majority"
CLASSIFIER_NAME = "naive"
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


    return classifier


def test_data(classifier, documents, header, show_detail=False):
    result = {}
    candidates = get_candidates(documents)
    feature_set = get_feature_set(candidates, ACTIVE_FEATURES)

    results = [ classifier.classify(f[0]) for f in feature_set ]
    correct_results = [ f[1] for f in feature_set ]
    cm = nltk.ConfusionMatrix(correct_results, results)

    result['cm'] = cm
    result['classifier_accuracy'] = nltk.classify.accuracy(classifier, feature_set)

    new_mistakes = []
    for r, c in itertools.izip(results, candidates):
        m = c.generate_mistake(r)
        if m:
            new_mistakes.append(m)

    golden_mistakes = get_target_mistakes(documents)

    result["correction"] = len(new_mistakes)
    result["golden_correction"] = len(golden_mistakes)

    new_mistakes_set = Set(new_mistakes)
    golden_mistakes_set = Set(golden_mistakes)

    tp_list = []
    fp_list = []
    fn_list = []

    for m in golden_mistakes:
        if m in new_mistakes_set:
            tp_list.append(m)
        else:
            fn_list.append(m)

    for m in new_mistakes:
        if not m in golden_mistakes_set:
            fp_list.append(m)

    tp = len(tp_list)
    fp = len(fp_list)
    fn = len(fn_list)
    precision, recall, f1 = get_precision_recall_f1(tp, fp, fn)

    result['tp'] = tp
    result['fp'] = fp
    result['fn'] = fn
    result['precision'] = precision
    result['recall'] = recall
    result['f1'] = f1

    if show_detail:
        print_header("False Positive")
        dump_mistakes(fp_list)
        print_header("False Negative")
        dump_mistakes(fn_list)
        print_line()

    print_results_format(result, header)

    return result

def print_results_format(result, header):
    if 'cm' in result:
        print result['cm']

    print_result(result, "classifier_accuracy", header)
    print_result(result, "correction", header)
    print_result(result, "golden_correction", header)

    print_result(result, "tp", header)
    print_result(result, "fp", header)
    print_result(result, "fn", header)
    print_result(result, "precision", header)
    print_result(result, "recall", header)
    print_result(result, "f1", header)
    print


def print_result(result, name, header):
    print_info(name, result[name], header)

def print_result_se(result, name, header):
    name_se = "%s_se" % name
    print_info(name_se, result[name_se], header)


def dump_mistakes(mistakes):
    for m in mistakes:
        print m.sentence
        m.dump()
        print
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

    test_data(classifier, train_documents, "train")
    if "show_most_informative_features" in dir(classifier):
        classifier.show_most_informative_features()
    print

    test_data(classifier, test_documents, "test", True)
    #print_info("test_precision", [precision])
    #print_info("test_recall", [recall])
    #print_info("test_f1", [f1])

def run_data_10_fold(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    conlldata.filter_mistakes()


    documents = conlldata.documents
    random.seed(SEED)
    random.shuffle(documents)

    if len(documents) < 10:
        error_msg("len(documents) < 10")
        exit(1)

    documents_list = split_n_fold(documents, 10)
    for i in range(len(documents_list)):
        print_info("documents_list_%d" % i, [d.id for d in documents_list[i]])


    train_results = []
    test_results = []
    for i in range(len(documents_list)):
        msg = "Round %d" % i
        print_header(msg)
        print_progress(msg)

        result = {}
        result['i'] = i

        train_documents, test_documents = generate_train_test_i(documents_list, i)

        classifier = train_classifier(train_documents)

        train_result = test_data(classifier, train_documents, "%d_train" % i)
        train_results.append(train_result)

        if "show_most_informative_features" in dir(classifier):
            classifier.show_most_informative_features()
        print

        test_result = test_data(classifier, test_documents, "%d_test" % i)
        test_results.append(test_result)

    train_result_avg = get_avg_results(train_results)
    test_result_avg = get_avg_results(test_results)

    print_header("Summary")
    print_results_format_se(train_result_avg, "train")
    print_results_format_se(test_result_avg, "test")

    print_results_format(train_result_avg, "train")
    print_results_format(test_result_avg, "test")

    #all_result = {}
    #merge_results(all_result, train_result_avg, "train")
    #merge_results(all_result, test_result_avg, "test")
    #print all_result

def print_results_format_se(result, header):
    print_result_se(result, "classifier_accuracy", header)
    print_result_se(result, "correction", header)
    print_result_se(result, "golden_correction", header)

    print_result_se(result, "tp", header)
    print_result_se(result, "fp", header)
    print_result_se(result, "fn", header)
    print_result_se(result, "precision", header)
    print_result_se(result, "recall", header)
    print_result_se(result, "f1", header)
    print

#def merge_results(all_result, result, header):
    #for key, value in result.iteritems():
    #    all_result["%s_%s" % (header, key)] = value

def get_avg_results(data_list):
    result = {}

    for key, value in data_list[0].iteritems():
        if key == "cm":
            continue

        avg, se = get_info_from_results(data_list, key)
        result[key] = avg
        result["%s_se" % key] = se

    return result


def get_info_from_results(results, name):
    lst = [r[name] for r in results]
    avg = numpy.mean(lst)
    #SE = scipy.stats.sem(lst)
    var = sum([(e - avg)**2 for e in lst]) / (len(lst) - 1)
    SE = math.sqrt(var / len(lst))

    return (avg ,SE)


def process_parameter(parameter):
    global CLASSIFIER_NAME
    global FEATURE_LIST
    global ACTIVE_FEATURES
    global SEED

    parameter_cid = parameter[0]
    parameter_seed = parameter[1]
    parameter_feature = parameter[2:]

    SEED = int(parameter_seed)

    CLASSIFIER_NAME = CLASSIFIER_LIST[int(parameter_cid)]

    active_features_list = []
    for i in range(len(parameter_feature)):
        if parameter_feature[i] == '1':
            active_features_list.append( FEATURE_LIST[i] )

    ACTIVE_FEATURES = set(active_features_list)


def main():
    global CLASSIFIER_NAME
    global FEATURE_LIST
    global ACTIVE_FEATURES
    global SEED

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

    print_header("Setting")
    print_info("start_time", get_date_time())
    print_info("git_hash", git_hash)
    print_info("conll_file", conll_file)
    print_info("ann_file", ann_file)
    print_info("log_file", log_file)
    print_info("parameter", parameter)
    print_info("seed", SEED)
    print_info("classifier", CLASSIFIER_NAME)
    print_info("active_features", sorted(list(ACTIVE_FEATURES)))
    print_info("inactive_features", sorted([f for f in FEATURE_LIST if f not in ACTIVE_FEATURES]))


    if not check_file_to_read(conll_file):
        return

    #run_data(conll_file, ann_file, out_file)
    run_data_10_fold(conll_file, ann_file, out_file)

    print_info("end_time", get_date_time())
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
