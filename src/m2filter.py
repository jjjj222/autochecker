import sys

def main():
    filename = sys.argv[1]
    match = sys.argv[2]
    out_filename = "%s.%s" % (filename, match)

    fout = open(out_filename, 'w')

    with open(filename, 'r') as fin:
        for line in fin.readlines():
            words = line.split()
            if len(words) != 0 and words[0] == "A":
                if not match in line:
                    continue
            fout.write(line)

    fout.close()

if __name__ == "__main__":
    main()
