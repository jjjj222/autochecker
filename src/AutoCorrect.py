#! /usr/bin/python

import sys
import nltk
from conlldata import ConllData
from myutil import *
from classifier import *

def is_ArtOrDet(word):
    if word == "the" or word == 'a' or word == 'an':
        return True

    return False

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

def artOrDet_class(sentence, word, mistake):
    i = word.id

    if mistake == None:
        if word.pos == "DT" :
            return word.token
        else:
            return "<X>"
    else:
        if mistake.correction == "":
            return "<X>"
        return mistake.correction


def parse_data(conll_file, ann_file):
    conlldata = ConllData(conll_file, ann_file)
    candidates = conlldata.get_ArtOrDet_candidates()

    #print c
    feature_set = []
    for w in candidates:
        s = conlldata.get_sentence(w.nid, w.pid, w.sid)
        m = conlldata.get_mistake(w)
        f = artOrDet_features(s, w)
        c = artOrDet_class(s, w, m)

        feature_set.append((f, c))
        #print w, m, f, c

    classifier = MajorityClassifier()
    classifier.train(feature_set)
    print "Majority:", classifier.accuracy(feature_set)

    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    print "NaiveBayes:", nltk.classify.accuracy(classifier, feature_set)

    classifier = nltk.classify.DecisionTreeClassifier.train(feature_set, entropy_cutoff=0)
    print "DecisionTree:", nltk.classify.accuracy(classifier, feature_set)

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
