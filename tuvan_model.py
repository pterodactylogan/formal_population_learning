import numpy as np
import scipy.stats as stats
import random
from collections import Counter
import matplotlib.pyplot as plt

# words heard before convergence
W = 50

# population size
P = 300

# how many times to iterate
T = 150


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
        if t%20 == 0: print(t)
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

back_vowels = {"a": 0.324, "u": 0.127,
               "o": 0.084, "ɯ": 0.025} # vowel: frequency

front_vowels = {"e": 0.166, "i":0.162,
                "ø": 0.096, "y": 0.042}

# order bigrams according to vowel frequencies
bigram_freqs = []
for x in back_vowels:
    for y in back_vowels:
        bigram_freqs.append((x+y,
                             back_vowels[x] * back_vowels[y]))

for x in front_vowels:
    for y in front_vowels:
        bigram_freqs.append((x+y,
                             front_vowels[x] * front_vowels[y]))

bigram_freqs.sort(key=lambda x: x[1], reverse=True)
grammar = [b[0] for b in bigram_freqs]

grammars = [grammar.copy() for i in range(P)]

#output = learn(grammars, grammar)

plots = []
mod=1
for b in range(len(grammar)):
    plots.append([1])
time = [i for i in range(T+1)]

output = learn(grammars, grammar, plots)

lost = []
for b in range(len(grammar)):
    num_using = len(list(filter(lambda g: grammar[b] in g, output)))
    if num_using == 0:
        lost.append(grammar[b])

print("number elements lost:", len(lost))
print(lost)

for b in range(len(grammar)):
    if b%mod != 0: continue
    plt.plot(time, plots[b], label = grammar[b])
plt.legend()

ax = plt.gca()
ax.set_ylim([0, 1])

plt.show()

