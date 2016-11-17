#! /usr/bin/python

import sys
import nltk
import itertools
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


    test_classifier(classifier, feature_set)

    return classifier

def test_classifier(classifier, feature_set):
    results = [ classifier.classify(f[0]) for f in feature_set ]
    correct_results = [ f[1] for f in feature_set ]
    cm = nltk.ConfusionMatrix(correct_results, results)
    print cm
    print "overfit =", nltk.classify.accuracy(classifier, feature_set)
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
    print "dev =", nltk.classify.accuracy(classifier, feature_set)
    print

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
    for m in new_mistakes:
        m.dump()
    print

    print "# of golden correction =", len(golden_mistakes)
    for m in golden_mistakes:
        m.dump()
    print

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
    for m in fp:
        m.dump()
    print

    print "# of fn =", len(fn)
    for m in fn:
        m.dump()
    print

    print "tp =", len(tp)
    print "fp =", len(fp)
    print "fn =", len(fn)

    print "precision = %s" % (float(len(tp)) / (len(tp) + len(fp)))
    print "recall = %s" % (float(len(tp)) / (len(tp) + len(fn)))

    print "f1 = %s" % (2 * float(len(tp)) / (2 * len(tp) + len(fn) + len(fp)))



def parse_data(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    #write_out_correct(conlldata, out_file)
    conlldata.filter_mistakes()

    half = len(conlldata.documents) / 2
    classifier = train_classifier(conlldata.documents[:half])
    test_data(classifier, conlldata.documents[half:])
    return

    #words = conlldata.get_ArtOrDet_candidates()
    #candidates = [Candidate(w) for w in words if Candidate(w).is_target()]

    #for c in candidates:
    #    c.dump()

    #feature_set = [(artOrDet_features(c.word), c.get_correct_determiner()) for c in candidates]
    #print feature_set[0]
    #return

    #return
    #return
    #feature_set = []
    #for w in words:
    #    s = conlldata.get_sentence(w.nid, w.pid, w.sid)
    #    m = conlldata.get_mistake(w)
    #    f = artOrDet_features(s, w)
    #    c = artOrDet_class(s, w, m)

    #    feature_set.append((f, c))

    #classifier = train_classifier(feature_set)

    #for c in candidates

    #print classifier
    #current_det = [artOrDet_current(w.sentence, w) for w in words]
    #current_det = [c.get_correct_determiner() for c in candidates]
    #results = [ classifier.classify(f[0]) for f in feature_set ]
    #correct_results = [ f[1] for f in feature_set ]
    #cm = nltk.ConfusionMatrix(correct_results, results)
    #print cm
    #print "overfit =", nltk.classify.accuracy(classifier, feature_set)

    #new_mistakes = []
    #for c, r, w in itertools.izip(current_det, results, words):
    #    if c == r:
    #        continue

    #    #print w.nid, w.pid, w.sid, w.id, w, c, r
    #    if r == "<X>":
    #        m = Mistake(w.nid, w.pid, w.sid, w.id, w.id+1, "ArtOrDet", "")
    #    else:
    #        if c == "<X>":
    #            m = Mistake(w.nid, w.pid, w.sid, w.id, w.id, "ArtOrDet", r)
    #        else:
    #            m = Mistake(w.nid, w.pid, w.sid, w.id, w.id+1, "ArtOrDet", r)
    #    new_mistakes.append(m)

    ##print len(new_mistakes)
    #new_mistakes_set = Set(new_mistakes)

    ##print len(new_mistakes_set)

    #tp, fp, fn = 0, 0, 0
    #for m in conlldata.mistakes("ArtOrDet"):
    #    if m in new_mistakes_set:
    #        tp += 1
    #    else:
    #        fn += 1

    #fp = len(new_mistakes_set) - tp

    #print "tp =", tp
    #print "fp =", fp
    #print "fn =", fn

    #print "precision = %s" % (float(tp) / (tp + fp))
    #print "recall = %s" % (float(tp) / (tp + fn))
    #    if m.nid != 829 or m.pid != 4 or m.sid != 1:
    #        continue

    #    print m.show_in_sentence()
    #    m.dump()
    #s = conlldata[0][3][0]
    #print s
    #s.dump()
    #print s.correct_text()



    #current_det = [artOrDet_current(w.sentence, w) for w in candidates]

    #classifier = nltk.NaiveBayesClassifier.train(feature_set)
    #results = [ classifier.classify(f[0]) for f in feature_set ]

    #for c, r, w in itertools.izip(current_det, results, candidates):
    #    if c != r:
    #        print w.nid, w.pid, w.sid, w.id, w, c, r

    #print
    ##print results
    ##print len(feature_set)
    ##print "NaiveBayes:", nltk.classify.accuracy(classifier, feature_set)
    #for m in conlldata.mistakes("ArtOrDet"):
    #    m.dump()
    ##    #s = conlldata.get_sentence(m.nid, m.pid, m.sid)
    ##    print m.sentence
    ##    print m.show_in_sentence()
    ##    #break
    ##    #s = m.sentence
    ##    #print s

    
    #run_classifier(feature_set)
    #run_classifier_overfit(feature_set)
        #if c != 'a' and c != 'an' and c != 'the' and c != '<X>':
        #    #print s.plain_text()
        #    print s.tagged_text()
        #    #print m
        #    print w
        #    print c
        #    print 

        #qq = f
        #print w, m, f, c


    #classifier = nltk.NaiveBayesClassifier.train(train_set)
    #print "NaiveBayes:", nltk.classify.accuracy(classifier, test_set)

    #classifier = nltk.classify.DecisionTreeClassifier.train(feature_set, entropy_cutoff=0)
    #print "DecisionTree:", nltk.classify.accuracy(classifier, feature_set)

    #classifier = nltk.NaiveBayesClassifier.train(feature_set)
    #print(nltk.classify.accuracy(classifier, feature_set))


        #f = artOrDet_features(s, c)
        #print s.get_plain_text()
        #print c
        #print f


        #break
    #    #c.dump()
    #    if m:
    #        c.dump()
    #        m.dump()

    #conlldata.dump()
        #for s in self.sentences:
        #    result.append( s.get_ArtOrDet_candidates() )
    #conlldata.concordance("the")
    #c = []
    #for d in conlldata:
    #    c.append( d.get_ArtOrDet_candidates() )



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
