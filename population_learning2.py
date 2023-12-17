import matplotlib.pyplot as plt
from math import comb

# alphabet = a,b
# SL-2 grammar

# probability any given word contains a given bigram is:
# 2 / (2+n) where n is the number of bigrams in the grammar

# words heard before convergence (diff n from example above)
w = 20

# initial number of bigrams
n = 4
# value at each index is proportion of population speaking *a specific*
# language with that size of grammar
# initialized so that everyon speaks language with n bigrams
props = [0 for i in range(n+1)]
props[n] = 1

# values in list may not sum to 1
# this should sum to 1 instead:
# for i in range(n+1):
    # sum += probs[i] * (n choose i)
    
plots=[]
for s in range(n+1):
    plots.append([comb(n, s) * props[s]])
    
time = [0]
for i in range(10):
    p_bigram_produced = 0
    for s in range(1, n+1):
        # probability a specific bigram from a size s grammar is produced
        # number of s-size grammars with a given bigram
        # proportion of population speaking each s-size grammar
        p_bigram_produced += (2 / (2+s)) * comb(n-1, s-1) * props[s]

    # 1- probability that this bigram is NOT produced w times
    p_bigram_learned = 1 - (1-p_bigram_produced)**w

    for s in range(n+1):
        # probability of any specific set is the probability each
        # contained element is learned
        # times the probability each other element is not learned
        props[s] = (p_bigram_learned**s) * (1-p_bigram_learned)**(n-s)

    for s in range(n+1):
        plots[s].append(comb(n, s) * props[s])

    # check sum to 1
##    population_sum = 0
##    for j in range(n+1):
##        population_sum += props[j] * comb(n, j)
##    print("sum:", population_sum)
    
    time.append(i+1)
    
print([comb(n, s) * props[s] for s in range(n+1)])
for s in range(n+1):
    plt.plot(time, plots[s], label = str(s))
plt.legend()
plt.show()


