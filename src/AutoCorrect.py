#! /usr/bin/python

import sys
import nltk
import itertools
import random
from sets import Set

#import nltk.classify
from document import *
from conlldata import *
from myutil import *
from classifier import *
from features import *

#def is_ArtOrDet(word):
#    if word == "the" or word == 'a' or word == 'an':
#        return True
#
#    return False
target_det = ['a', 'an', 'the']


def artOrDet_current(sentence, word):
    if word.token.lower() in target_det :
        return word.token.lower()
    else:
        return "<X>"

def artOrDet_class(sentence, word, mistake):
    i = word.id

    if mistake == None:
        return artOrDet_current(sentence, word)
    else:
        if mistake.correction == "":
            return "<X>"
        return mistake.correction.lower()


def write_out_correct(conlldata, out_file):
    f = open(out_file, 'w')
    for s in conlldata.sentences():
        f.write(s.correct_text("ArtOrDet"))
        f.write('\n')
        print s.correct_text("ArtOrDet")
    f.close()

def train_classifier(documents):
    #words = []
    #for d in documents:
    #    words += d.get_ArtOrDet_candidates()

    #candidates = [Candidate(w) for w in words if Candidate(w).is_target()]
    candidates = get_candidates(documents)
    feature_set = [(artOrDet_features(c.word), c.get_determiner_class()) for c in candidates]

    #majority
    classifier = MajorityClassifier()
    classifier.train(feature_set)

    #naive
    #classifier = nltk.NaiveBayesClassifier.train(feature_set)

    #decision tree
    #classifier = nltk.DecisionTreeClassifier.train(feature_set)

    #maxent
    classifier = nltk.MaxentClassifier.train(feature_set)


    #test_classifier(classifier, feature_set)
    test_data(classifier, documents)

    return classifier

def test_classifier(classifier, feature_set):
    results = [ classifier.classify(f[0]) for f in feature_set ]
    correct_results = [ f[1] for f in feature_set ]
    cm = nltk.ConfusionMatrix(correct_results, results)
    print cm
    print "accuracy =", nltk.classify.accuracy(classifier, feature_set)
    print


def test_data(classifier, documents):
    candidates = get_candidates(documents)

    #for c in candidates:
    #    c.dump()
    #return

    feature_set = [(artOrDet_features(c.word), c.get_determiner_class()) for c in candidates]
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

    #return
    #results = []
    #for c in candidates:
    #    feature = artOrDet_features(c.word)
    #    result = classifier.classify(feature)
    #    results.append(result)

    #feature_set = [(artOrDet_features(c.word), c.get_correct_determiner()) for c in candidates]
    #return

    #current_det = [c.get_determiner() for c in candidates]


    new_mistakes = []
    for r, c in itertools.izip(results, candidates):
        m = c.generate_mistake(r)
        if m:
            new_mistakes.append(m)


    #return
    golden_mistakes = get_target_mistakes(documents)


    print "# of correction =", len(new_mistakes)
    #for m in new_mistakes:
    #    m.dump()
    #print

    print "# of golden correction =", len(golden_mistakes)
    #for m in golden_mistakes:
    #    m.dump()
    #print

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

    print "# of fp =", len(fp)
    #dump_mistakes(fp)

    print "# of fn =", len(fn)
    #dump_mistakes(fn)

    print "tp =", len(tp)
    print "fp =", len(fp)
    print "fn =", len(fn)

    print "precision = %s" % (float(len(tp)) / (len(tp) + len(fp)))
    print "recall = %s" % (float(len(tp)) / (len(tp) + len(fn)))

    print "f1 = %s" % (2 * float(len(tp)) / (2 * len(tp) + len(fn) + len(fp)))


def dump_mistakes(mistakes):
    for m in mistakes:
        m.dump()
    print


def parse_data(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    #write_out_correct(conlldata, out_file)
    conlldata.filter_mistakes()

    #classifier = train_classifier(conlldata.documents)
    #test_data(classifier, conlldata.documents)

    documents = conlldata.documents
    random.seed(1)
    random.shuffle(documents)
    for d in documents:
        sys.stdout.write(str(d.id))
        sys.stdout.write(" ")
    print


    split = len(documents) / 10

    if split == 0:
        split = 1

    classifier = train_classifier(documents[split:])
    test_data(classifier, documents[:split])



def main():
    #data_path = "../data/simple"
    #conll_file_name = "simple.conll"
    #ann_file_name = "simple.conll.ann"
    #conll_file = "%s/%s" % (data_path, conll_file_name)
    #ann_file = "%s/%s" % (data_path, ann_file_name)

    conll_file = sys.argv[1]
    ann_file = sys.argv[2]
    out_file = sys.argv[3]

    if not check_file_to_read(conll_file):
        return

    parse_data(conll_file, ann_file, out_file)
    #print type(data)

if __name__ == "__main__":
    main()
