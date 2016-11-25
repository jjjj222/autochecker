#! /usr/bin/python
import os
import sys
import random
import subprocess
import signal

import AutoCorrect
import features
import myutil

def rand_parameters(parameter_filter):
    parameters = []

    # classifier
    parameters.append( str(random.randint(0, len(AutoCorrect.CLASSIFIER_LIST)-1)) )

    # seed
    parameters.append( str(random.randint(0, 9)) )

    for i in range(len(features.FEATURE_LIST)):
        parameters.append( str(random.randint(0, 1)) )

    # filter
    for i in range(len(parameter_filter)):
        if parameter_filter[i] == "?":
            continue

        parameters[i] = parameter_filter[i]

    return "".join(parameters)


def main():
    case_name = sys.argv[1]
    parameter_filter = sys.argv[2] if len(sys.argv) > 2 else ""
    conll_file = "../data/%s/%s.conll" % (case_name, case_name)
    ann_file = "../data/%s/%s.conll.ann" % (case_name, case_name)

    #signal.signal(signal.SIGINT, signal_handler)
    #print('Press Ctrl+C')
    #signal.pause()

    exist_count = 0
    try:
        while True:
            parameters = rand_parameters(parameter_filter)
            log_file = myutil.get_log_file_name(case_name, parameters)
            #out_file = "../result/%s_%s.out" % (case_name, parameters)
            #print log_file
            if os.path.exists(log_file):
                print "X", case_name, parameters, exist_count
                exist_count += 1
                if exist_count > 100:
                    break
                continue
            else:
                print "V", case_name, parameters, myutil.get_time()
            #else:
            #    print "V", log_file
            exist_count = 0

            cmd = "python AutoCorrect.py %s %s %s %s" %\
                (conll_file, ann_file, log_file, parameters)

            #print cmd
            p = subprocess.call(cmd.split(' '))
    except:
        print "DELETE %s" % log_file
        cmd = "rm %s" % log_file
        subprocess.call(cmd.split(' '))


if __name__ == "__main__":
    main()
