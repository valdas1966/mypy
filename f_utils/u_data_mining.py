import u_list

def bigram(li_1, li_2):
    """
    ===========================================================================
     Description: Calc Similarity between 2 lists with order significance
                     by BiGram method.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. li_1 : First List.
        2. li_2 : Second List.
    ===========================================================================
     Return: float (BiGram Similarity between the two lists).
    ===========================================================================
    """
    tuples_1 = u_list.to_tuples_bigram(li_1)
    tuples_2 = u_list.to_tuples_bigram(li_2)
    
    count_intersection = len(set.intersection(tuples_1,tuples_2))
    count_union = len(set.union(tuples_1,tuples_2))
    ratio_count = count_intersection / count_union
    
    size_min = min(len(li_1),len(li_2))
    size_max = max(len(li_1),len(li_2))
    ratio_size = size_min / size_max   
    
    return round(ratio_count*ratio_size, 2)


"""
===============================================================================
===============================================================================
==========     Tester     =====================================================
===============================================================================
===============================================================================
"""
def tester():
    
    import u_tester
    
    def tester_bigram():
        
        li_1 = list('denis')
        li_2 = list('dennis')
        
        bigram_test = bigram(li_1, li_2)
        
        tuples_1 = [ tuple('de'), tuple('en'), tuple('ni'), tuple('is') ]
        tuples_2 = [ tuple('de'), tuple('en'), tuple('nn'), tuple('ni'), tuple('is')]
        
        count_intersection = 8
        count_union = 9
        ratio_count = 0.89
        
        ratio_size = 0.83
        
        bigram_true = 0.74
        
        p0 = bigram_test == bigram_true
        
        u_tester.run([p0])
        
    
    u_tester.print_start(__file__)
    #tester_bigram()
    u_tester.print_finish(__file__)
   
tester()
        

from itertools import chain
import numpy as np
from math import sqrt, log

def corpus2vectors(corpus):
    
    def vectorize(sentence, vocab):
        return [sentence.split().count(i) for i in vocab]
    
    vectorized_corpus = []
    vocab = sorted(set(chain(*[i.lower().split() for i in corpus])))
    for i in corpus:
        vectorized_corpus.append((i, vectorize(i, vocab)))
    
    return vectorized_corpus, vocab
        
corpus, vocab = corpus2vectors(['aaa bbb ccc','ccc bbb aaa']) 


def cosine_sim(u,v):
    return np.dot(u,v) / (sqrt(np.dot(u,u)) * sqrt(np.dot(v,v)))

u = corpus[0][1]
v = corpus[1][1]

print(cosine_sim(u,v))   