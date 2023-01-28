from nltk import ngrams
from math import log
import numpy as np

fp = open('/home/zeroday/Desktop/cse654_nlp/hw1/1801042651/syllables.txt','r',encoding = 'utf8')

syllables = fp.read()
uni_grams = ngrams(syllables.split(), 1)
bi_grams = ngrams(syllables.split(), 2)
tri_grams = ngrams(syllables.split(), 3)

# print("################## N-GRAMS #####################")

# print("\n### uni-grams ###")
# for grams in uni_grams:
#     print(grams)

# print("\n### bi-grams ###")
# for grams in bi_grams:
#     print(grams)

# print("\n### tri-grams ###")
# for grams in tri_grams:
#     print(grams)

def generate_n_grams(n_grams):
    dict = {}
    dict.clear()
    for grams in n_grams:
        if grams in dict:
            dict[grams] = dict[grams] + 1
        else:
            dict[grams] = 1
    return dict

def sparse_matrix(arr):
    size = 0
    
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if (arr[i][j] != 0):
                size += 1

    rows, cols = (3, size)
    non_sparse = [[0 for i in range(cols)] for j in range(rows)]
    
    k = 0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if (arr[i][j] != 0):
                non_sparse[0][k] = i
                non_sparse[1][k] = j
                non_sparse[2][k] = arr[i][j]
                k += 1
    
    return non_sparse

def GT_smoothing(freq, arr):
    keys = list(freq.keys())
    keys.sort()

    for i in range(len(keys)):
        if i < len(keys)-1:
            if(keys[i] == 0):
                gt = freq[keys[i + 1]]/len(arr)
            else:
                gt = (keys[i]+1)*freq[keys[i + 1]]/freq[keys[i]]
            for x in range(0, len(arr)):
                if(arr[x] == keys[i]):
                        arr[x] = gt
    return arr

def markov_uni(uni_grams_sentence, clear_dict_uni):
    result = 1
    my_len = 0
    for e in uni_grams_sentence:
        my_len += 1
        if e in clear_dict_uni:
            result *= (clear_dict_uni[e]/ len(clear_dict_uni))
    return result, my_len

def markov_bi(bi_grams_sentence, clear_dict_bi, clear_dict_uni):
    result = 1
    my_len = 0
    for e in bi_grams_sentence:
        my_len += 1
        if e in clear_dict_bi and (e[0],) in clear_dict_uni:
            result *= (clear_dict_bi[e]/clear_dict_uni[(e[0]),])
    return result, my_len

def markov_tri(tri_grams_sentence, clear_dict_tri, clear_dict_bi):
    result = 1
    my_len = 0
    for e in tri_grams_sentence:
        my_len += 1
        if e in clear_dict_tri and (e[0],e[1]) in clear_dict_bi:
            result *= (clear_dict_tri[e]/clear_dict_bi[(e[0],e[1])])
    return result, my_len

def perplexity(markov_n, N):
    result = 1/markov_n
    result = result ** (1/N)
    return result

dict_uni = generate_n_grams(uni_grams)

dict_bi = generate_n_grams(bi_grams)

dict_tri = generate_n_grams(tri_grams)

# print("### frequencies each of the grams ###")
# for e in dict_uni:
#     print(e, dict_uni[e])

# for e in dict_bi:
#     print(e, dict_bi[e])

# for e in dict_tri:
#     print(e, dict_tri[e])

### n-gram tables

uni_arr = np.empty((len(dict_uni)), dtype=float)
bi_arr = np.empty((len(dict_uni), len(dict_uni)), dtype=float)
tri_arr = np.empty((len(dict_bi), len(dict_uni)), dtype=float)

### for uni
i=0
for e in dict_uni:
    uni_arr[i] = dict_uni[e]
    i += 1

### for bi
i=0
j=0
for e in dict_uni:
    j=0
    for e2 in dict_uni:
        if((e[0], e2[0]) in dict_bi):
            bi_arr[i][j] = dict_bi[(e[0], e2[0])]
        else:
            bi_arr[i][j] = 0
        j += 1
    i += 1  

### for tri
i=0
j=0
for e in dict_bi:
    j=0
    for e2 in dict_uni:
        if((e[0], e[1], e2[0]) in dict_tri):
            tri_arr[i][j] = dict_tri[(e[0], e[1], e2[0])]
        else:
            tri_arr[i][j] = 0
        j += 1
    i += 1 

### good turing smoothing

l = list(uni_arr)

frequencies_uni = {x:l.count(x) for x in l}

# for i in range(0, len(uni_arr)):
#     print(uni_arr[i], end='  ')
# print("\n")

uni_arr = GT_smoothing(frequencies_uni, uni_arr)

# for i in range(0, len(uni_arr)):
#     print(uni_arr[i], end='   ')
# print("\n")

non_sparse_bi = sparse_matrix(bi_arr)
# print(non_sparse_bi[2])


l = list(non_sparse_bi[2])

frequencies_bi = {x:l.count(x) for x in l}

non_sparse_bi[2] = GT_smoothing(frequencies_bi, non_sparse_bi[2])
# print("\n\n\n")
# print(non_sparse_bi[2])

# for i in range(0, len(non_sparse_bi[2])):
#     print(non_sparse_bi[i], end='   ')
# print("\n")


non_sparse_tri = sparse_matrix(tri_arr)

l = list(non_sparse_tri[2])

frequencies_tri = {x:l.count(x) for x in l}

non_sparse_tri[2] = GT_smoothing(frequencies_tri, non_sparse_tri[2])

### creating n_grams for a sentence in corpora for perplexity

fd = open('/home/zeroday/Desktop/cse654_nlp/hw1/sentence.txt','r',encoding = 'utf8')

sentence = fd.read()
uni_grams_sentence = ngrams(sentence.split(), 1)
bi_grams_sentence = ngrams(sentence.split(), 2)
tri_grams_sentence = ngrams(sentence.split(), 3)


### markov for uni_grams

m_uni, len_uni = markov_uni(uni_grams_sentence, dict_uni)

### markov for bi_grams

m_bi, len_bi = markov_bi(bi_grams_sentence, dict_bi, dict_uni)

### markov for tri_grams

m_tri, len_tri = markov_tri(tri_grams_sentence, dict_tri, dict_bi)

# m_uni = log(m_uni)
# m_bi = log(m_bi)
# m_tri = log(m_tri)


### perplexity for uni_grams

p_uni = perplexity(m_uni,len_uni)

print("Perplexity for unigrams", end=': ')
print(p_uni)
### perplexity for bi_grams

p_bi = perplexity(m_bi, len_bi)
print("Perplexity for bigrams", end=': ')
print(p_bi)

### perplexity for tri_grams

p_tri = perplexity(m_tri, len_tri)
print("Perplexity for trigrams", end=': ')
print(p_tri)