#! /usr/bin/python
import os
import sys
import random
import subprocess

import AutoCorrect
import features
import myutil

#print "QQ"
#print AutoCorrect.CLASSIFIER_LIST
#print features.FEATURE_LIST

#prin t random.random()
#RUN_CASE = python $(EXEC) ../data/$@/$@.conll ../data/$@/$@.conll.ann ../result/$@.out 11

def rand_parameters():
    parameters = []

    parameters.append( str(random.randint(0, len(AutoCorrect.CLASSIFIER_LIST)-1)) )
    for i in range(len(features.FEATURE_LIST)):
        parameters.append( str(random.randint(0, 1)) )

    return "".join(parameters)

def main():
    case_name = sys.argv[1]
    conll_file = "../data/%s/%s.conll" % (case_name, case_name)
    ann_file = "../data/%s/%s.conll.ann" % (case_name, case_name)
    while True:
        parameters = rand_parameters()
        log_file = myutil.get_log_file_name(case_name, parameters)
        out_file = "../result/%s_%s.out" % (case_name, parameters)
        #print log_file
        if os.path.exists(log_file):
            print "X", case_name, parameters
            continue
        else:
            print "V", case_name, parameters
        #else:
        #    print "V", log_file

        cmd = "python AutoCorrect.py %s %s %s %s" %\
            (conll_file, ann_file, out_file, parameters)

        print cmd
        subprocess.call(cmd.split(' '))


if __name__ == "__main__":
    main()
