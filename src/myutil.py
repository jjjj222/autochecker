import os
import sys
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
    log_file = "../log/%s/%s.log" % (case_name, parameter.rstrip('0'))
    return log_file

def create_file_dir(file_name):
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def print_info(name, data):
    sys.stdout.write(str(name))
    sys.stdout.write(":")
    for d in data:
        sys.stdout.write(" ")
        sys.stdout.write(str(d))
    print
    
