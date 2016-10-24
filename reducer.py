'''simple script to cut shingles that only occur once'''

import sys, re

digitgetter = re.compile("(?<=,)[0-9]+")

incomingfn = sys.argv[1]

def filter_file():
    current_digit = None
    current_list = []
    counter = 0
    with open(incomingfn, "r") as inf:
        for rw in inf:
            counter += 1
            if counter % 1000 == 0:
                print counter
            digit = digitgetter.search(rw).group(0)
            if digit != current_digit:
                if len(current_list) > 1:
                    with open(incomingfn + ".filter", "a") as outf:
                        for ln in current_list:
                            outf.write(ln)
                current_list[:] = []
                current_digit = digit
            current_list.append(rw)
        

if __name__ == '__main__':
    filter_file()