#! /usr/bin/python
import sys
import os
import myutil

def main():
    case_name = sys.argv[1]
    parameter = sys.argv[2] if len(sys.argv) > 2 else ""


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

        if not 'end_time' in data:
            continue

        if not match_parameter(data['parameter'], parameter):
            continue

        all_data.append(data)

    all_data = sorted(all_data, reverse=True, key=lambda x: float(x['test_f1']))
    #print all_data
    count = 0
    for d in all_data:
        print_data(d)
        count += 1
        if count == 40:
            break
    print "Total =", len(all_data)

def match_parameter(parameter, requirement):
    #print "QQ"
    for i in range(len(requirement)):
        if requirement[i] == "?":
            continue

        if len(parameter) <= i:
            return False

        if parameter[i] != requirement[i]:
            return False

    return True

def print_data(d):
    sys.stdout.write("%.2f" % float(d['test_f1']))
    sys.stdout.write('  ')
    sys.stdout.write("%.3f" % float(d['test_precision']))
    sys.stdout.write(' ')
    sys.stdout.write("%.3f" % float(d['test_recall']))
    sys.stdout.write('  ')
    sys.stdout.write("%-14s" % d['classifier'])
    sys.stdout.write(' ')
    sys.stdout.write("%-20s" % d['parameter'])
    sys.stdout.write('\t')
    sys.stdout.write("%.2f" % float(d['train_classifier_accuracy']))
    sys.stdout.write('  ')
    sys.stdout.write("%.2f" % float(d['test_classifier_accuracy']))
    sys.stdout.write('  ')
    sys.stdout.write("%6d" % float(d['test_tp']))
    sys.stdout.write('  ')
    sys.stdout.write("%6d" % float(d['test_fp']))
    sys.stdout.write('  ')
    sys.stdout.write("%6d" % float(d['test_fn']))
    print


if __name__ == "__main__":
    main()
