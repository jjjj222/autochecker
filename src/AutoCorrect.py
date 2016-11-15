#! /usr/bin/python

import sys
#import nltk
import itertools
#import nltk.classify
from conlldata import ConllData
from myutil import *
from classifier import *

#def is_ArtOrDet(word):
#    if word == "the" or word == 'a' or word == 'an':
#        return True
#
#    return False
target_det = ['a', 'an', 'the']

def artOrDet_features(sentence, word):
    result = {}

    i = word.id

    if word.pos == "DT":
        result['word'] = sentence[i+1].token.lower()
        result['tag'] = sentence[i+1].pos
    else:
        result['word'] = sentence[i].token.lower()
        result['tag'] = sentence[i].pos

    return result

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


#def run_classifier(feature_set):
#    train_set = feature_set[:len(feature_set)/2]
#    test_set = feature_set[len(feature_set)/2:]
#
#    classifier = MajorityClassifier()
#    classifier.train(train_set)
#    print "Majority:", nltk.classify.accuracy(classifier, test_set)
#
#    classifier = nltk.NaiveBayesClassifier.train(train_set)
#    print "NaiveBayes:", nltk.classify.accuracy(classifier, test_set)
#
#def run_classifier_overfit(feature_set):
#    classifier = MajorityClassifier()
#    classifier.train(feature_set)
#    print classifier.labels()
#    print "Majority:", nltk.classify.accuracy(classifier, feature_set)
#
#    classifier = nltk.NaiveBayesClassifier.train(feature_set)
#    print "NaiveBayes:", nltk.classify.accuracy(classifier, feature_set)


def parse_data(conll_file, ann_file, out_file):
    conlldata = ConllData(conll_file, ann_file)
    candidates = conlldata.get_ArtOrDet_candidates()

    feature_set = []
    for w in candidates:
        s = conlldata.get_sentence(w.nid, w.pid, w.sid)
        m = conlldata.get_mistake(w)
        f = artOrDet_features(s, w)
        c = artOrDet_class(s, w, m)

        feature_set.append((f, c))


    #s = conlldata[0][3][0]
    #print s
    #s.dump()
    #print s.correct_text()

    f = open(out_file, 'w')
    for s in conlldata.sentences():
        #f.write(s.__str__())
        f.write(s.correct_text("ArtOrDet"))
        f.write('\n')
        print s.correct_text("ArtOrDet")
        #break
    f.close()


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
