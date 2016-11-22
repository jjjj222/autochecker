import os
import sys
import datetime
import subprocess

def error_msg(msg):
    print "Error: %s !" % msg

def check_file_to_read(filename):
    if not os.path.exists(filename):
        error_msg("file '%s' doesn't exist" % filename)
        return False

    return True

def parse_space_separated_file(filename):
    result = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            words = line.split()
            result.append(words)
    return result

def get_git_hash():
    git_hash_cmd = ("git log -1 --pretty=%H")
    out = exec_shell_command(git_hash_cmd).strip()
    return out


def exec_shell_command(cmd):
    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

def get_log_file_name(case_name, parameter):
    par_str = parameter.rstrip('0')
    if par_str == "":
        par_str = "0"
    log_file = "../log/%s/%s.log" % (case_name, par_str)
    return log_file

def create_file_dir(file_name):
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def print_info(name, data, header=None):
    if header != None:
        sys.stdout.write(str(header))
        sys.stdout.write('_')
    sys.stdout.write(str(name))
    sys.stdout.write(":")

    if type(data) == list:
        for d in data:
            sys.stdout.write(" ")
            sys.stdout.write(str(d))
        print
    else:
        sys.stdout.write(" ")
        print data

def print_value(name, value):
    print "%s = %s" % (name, value)


def get_precision_recall_f1(tp, fp, fn):
    precision = float(tp) / (tp + fp) if tp + fp != 0 else 1
    recall = float(tp) / (tp + fn) if tp + fn != 0 else 1
    f1 = 2 * float(tp) / (2 * tp + fn + fp) if (2 * tp + fn + fp) != 0 else 1
    return (precision, recall, f1)

def get_time():
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_date_time():
    return datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')


def split_n_fold(lst, n = 10):
    return [ lst[i::n] for i in xrange(n) ]

def generate_train_test_i(lst, i):
    train = []

    for j in range(len(lst)):
        if j != i:
            train += lst[j]

    return (train, lst[i])

def print_line(n=50):
    print "-" * n

def print_header(title, n=50):
    n_space = ((n - len(title) - 2)/ 2) - 1

    print_line(n)
    print " " * n_space, title
    print_line(n)

def print_progress(msg):
    tmp = sys.stdout
    sys.stdout = sys.__stdout__
    print get_time(), msg
    sys.stdout = tmp
