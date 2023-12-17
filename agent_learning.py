import numpy as np
import scipy.stats as stats
import random
from collections import Counter
import matplotlib.pyplot as plt

# initial number of bigrams
N = 40

# words heard before convergence
W = 50

# population size
P = 150

# how many times to iterate
T = 150

# other parameters: stop_prob, incrementation of stop_prob



'''
grammar: list of items representing unique basis elements (eg bigrams)
the order of the elements corresponds to their frequency (for this particular
grammar)

returns: list of basis elements (however they are represented)
present in a single `word`
'''
def get_word(grammar):
    output = []
    # grammar is list of bigrams
    stop_prob = .2

    n = len(grammar)
    x = np.arange(1, n+1)
    weights = 1 / x
    weights /= weights.sum()
    bounded_zipf = stats.rv_discrete(name='bounded_zipf', values=(x, weights))
    while True:
        rank = bounded_zipf.rvs(size=1)[0]
        # insert the basis element with this rank
        output.append(grammar[rank-1])
        # with probability stop_prob, return current result
        if True in random.choices([True, False],
                                  weights=[stop_prob, 1-stop_prob],
                                  k=1):
            return output
        
        # stopping is more likely next time
        stop_prob += 0.2

'''
words: list of `words`, represented by lists of basis-element symbols

returns: grammar represented by ordered list of basis-elements. Ordering
corresponds to frequency with which speakers of this grammar will use elements
'''
def get_grammar(words):
    counts = Counter([el for word in words for el in word])
    return([x[0] for x in counts.most_common()])


def learn(grammars, plots=None, mod=1):
    # for each timestep
    for t in range(T):
        new_grammars = []
        # for each individual in the population
        for i in range(P):
            # get W words as input
            words = []
            for w in range(W):
                # get input word from random individual in population
                words.append(get_word(random.choice(grammars)))
            # new grammar is whatever A(inputs) gives
            new_grammars.append(get_grammar(words))

        grammars = new_grammars

        if plots != None:
            for b in range(N):
                if b%mod != 0: continue
                num_using = len(list(filter(lambda g: b in g, grammars)))
                plots[b].append(num_using / P)

    return grammars


# everyone starts from same initial grammar
# integers (0 to N-1) represent basis-elements
# initial ranks are in numerical order
#grammars = [[x for x in range(N)] for i in range(P)]

# plot fraction of population with each basis-element in their grammar
##plots = []
##for b in range(N):
##    plots.append([1])
##time = [i for i in range(T+1)]
##
##mod = 1

##for b in range(N):
##    if b%mod != 0: continue
##    plt.plot(time, plots[b], label = str(b))
##plt.legend()
##
##ax = plt.gca()
##ax.set_ylim([0, 1])
##
##plt.show()

for i in range(10):
    grammars = [[x for x in range(N)] for i in range(P)]
    grammars = learn(grammars)
    
    lost = []
    for b in range(N):
        num_using = len(list(filter(lambda g: b in g, grammars)))
        if num_using == 0:
            lost.append(b)

    print("number elements lost:", len(lost))
    print(lost)

