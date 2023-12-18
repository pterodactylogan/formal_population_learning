import numpy as np
import scipy.stats as stats
import random
from collections import Counter
import matplotlib.pyplot as plt

# words heard before convergence
W = 30

# population size
P = 300

# how many times to iterate
T = 150

# other parameters: stop_prob, incrementation of stop_prob


def get_bounded_zipf(length):
    x = np.arange(1, length+1)
    weights = 1 / x
    weights /= weights.sum()
    return stats.rv_discrete(name='bounded_zipf', values=(x, weights))


'''
grammar: list of bigrams representing unique basis elements.
the order of the elements corresponds to their frequency (for this particular
grammar)

returns: list of basis elements (however they are represented)
present in a simulated word
'''
def get_word(grammar):
    output = []

    length = stats.poisson.rvs(3) - 1
    last_symb = ""
    for i in range(length):
        if last_symb == "":
            possible_next = grammar
        else:
            possible_next = list(filter(lambda x: x[0] == last_symb, grammar))

        if len(possible_next) == 0:
            return output
        
        distro = get_bounded_zipf(len(possible_next))
        rank = distro.rvs()
        # insert the basis element with this rank
        output.append(possible_next[rank-1])
        last_symb = possible_next[rank-1][1]

    return output

'''
words: list of `words`, represented by lists of basis-element symbols

returns: grammar represented by ordered list of basis-elements. Ordering
corresponds to frequency with which speakers of this grammar will use elements
'''
def get_grammar(words):
    counts = Counter([el for word in words for el in word])
    return([x[0] for x in counts.most_common()])


def learn(grammars, all_elems, plots=None, mod=1):
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
            for b in range(len(all_elems)):
                if b%mod != 0: continue
                num_using = len(list(filter(lambda g: all_elems[b] in g, grammars)))
                plots[b].append(num_using / P)

    return grammars

back_vowels = ["ɯ", "u", "a", "o"]
front_vowels = ["i", "y", "e", "ø"]

grammar = [x+y for x in back_vowels for y in back_vowels]
grammar += [x+y for x in front_vowels for y in front_vowels]
random.shuffle(grammar)

grammars = [grammar.copy() for i in range(P)]

output = learn(grammars, grammar)

##plots = []
##mod=1
##for b in range(len(grammar)):
##    plots.append([1])
##time = [i for i in range(T+1)]
##
##output = learn(grammars, grammar, plots)
##
##for b in range(len(grammar)):
##    if b%mod != 0: continue
##    plt.plot(time, plots[b], label = grammar[b])
##plt.legend()
##
##ax = plt.gca()
##ax.set_ylim([0, 1])
##
##plt.show()



lost = []
for b in range(len(grammar)):
    num_using = len(list(filter(lambda g: grammar[b] in g, output)))
    if num_using == 0:
        lost.append(grammar[b])

print("number elements lost:", len(lost))
print(lost)

