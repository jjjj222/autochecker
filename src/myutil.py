import os

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
