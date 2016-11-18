#! /usr/bin/python
import sys

def main():
    case_name = sys.argv[1]
    log_dir = "../log/%s" % case_name
    print log_dir

if __name__ == "__main__":
    main()
