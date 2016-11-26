import numpy as np
import cPickle as pickle

def make_pi(hash_len):
    pi = np.random.permutation(hash_len)
    with open("pi.p", "w") as outf:
        pickle.dump(pi, outf)
    return None

if __name__ == '__main__':
    make_pi(32)