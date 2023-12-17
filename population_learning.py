import matplotlib.pyplot as plt

# alphabet = a,b
# SL-2 grammar

# probability any given word contains a given bigram is:
# 2 / (2+n) where n is the number of bigrams in the grammar

# words heard before convergence (diff n from example above)
n = 5

# initial population conditions
p_all = 1
p_3 = 0 # probability grammar is any specific set of 3
p_2 = 0 # note that this means these probabilities will not sum to 1
p_1 = 0
p_none = 0

# this should sum to 1 instead:
# p_all + 4*p_3 + 6*p_2 + 4*p_1 + p_none

all_over_time = [p_all]
over_time_3 = [p_3]
over_time_2 = [p_2]
over_time_1 = [p_1]
none_over_time = [p_none]
time = [0]
for i in range(10):
    # probability some specific bigram is in a given word the listener hears
    # all bigrams will be the same in this setup
    p_bigram_produced = (p_all / 3) + (p_3 * 6 / 5) + (p_2 * 3 / 2) + (p_1 * 2 / 3)
    
    # 1- probability that this bigram is NOT produced n times
    p_bigram_learned = 1 - (1-p_bigram_produced)**n

    # probability of any specific set is the probability each element is learned
    # times the probability each other element is not learned
    p_all = p_bigram_learned**4
    p_3 = (p_bigram_learned**3) * (1-p_bigram_learned)
    p_2 = (p_bigram_learned**2) * (1-p_bigram_learned)**2
    p_1 = p_bigram_learned * (1-p_bigram_learned)**3
    p_none = (1-p_bigram_learned)**4

    # check sum to 1
    print("none:", p_none)
    print("1:", p_1)
    print("2:", p_2)
    print("3:", p_3)
    print("all:", p_all)
    print("sum:", p_all + 4*p_3 + 6*p_2 + 4*p_1 + p_none)

    all_over_time.append(p_all)
    over_time_3.append(p_3*4)
    over_time_2.append(p_2*6)
    over_time_1.append(p_1*4)
    time.append(i+1)
    none_over_time.append(p_none)

plt.plot(time, all_over_time, label="all")
plt.plot(time, over_time_3, label="3")
plt.plot(time, over_time_2, label="2")
plt.plot(time, over_time_1, label="1")
plt.plot(time, none_over_time, label="none")
plt.legend()
plt.show()


