#! /usr/bin/python
import sys
import os
import myutil

def main():
    case_name = sys.argv[1]
    log_dir = "../log/%s" % case_name
    print log_dir
    all_data = []
    for f in os.listdir(log_dir):
        file_name = "%s/%s" % (log_dir, f)
        results =  myutil.parse_space_separated_file(file_name)
        #print results
        data = {}
        for line in results:
            if len(line) == 0:
                continue
            if line[0][-1] == ":":
                data[line[0][:-1]] = " ".join(line[1:]).strip()

        if not 'test_f1' in data:
            continue

        all_data.append(data)

    all_data = sorted(all_data, reverse=True, key=lambda x: float(x['test_f1']))
    #print all_data
    for d in all_data:
        print_data(d)

def print_data(d):
    sys.stdout.write("%.4f" % float(d['test_f1']))
    sys.stdout.write(' ')
    sys.stdout.write("%.4f" % float(d['test_precision']))
    sys.stdout.write(' ')
    sys.stdout.write("%.4f" % float(d['test_recall']))
    sys.stdout.write('\t')
    sys.stdout.write("%-10s" % d['classifier'])
    sys.stdout.write('\t')
    sys.stdout.write("%-10s" % d['parameter'])
    sys.stdout.write('\t')
    sys.stdout.write("%.4f" % float(d['train_classifier_accuracy']))
    sys.stdout.write('\t')
    sys.stdout.write("%.4f" % float(d['test_classifier_accuracy']))
    print


if __name__ == "__main__":
    main()
