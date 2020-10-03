from itertools import chain
import numpy as np
from math import sqrt

def cosine_similarity(text_1, text_2):
    """
    ===========================================================================
     Description: Return Cosine Similarity between two Texts.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. text_1 : str (First Text).
        2. text_2 : str (Second Text).
    ===========================================================================
     Return: float (Cosine Similarity between two Texts).
    ===========================================================================
    """
    def corpus2vectors(corpus):
        
        def vectorize(sentence, vocab):
            return [sentence.split().count(i) for i in vocab]
        
        vectorized_corpus = []
        vocab = sorted(set(chain(*[i.lower().split() for i in corpus])))
        for i in corpus:
            vectorized_corpus.append((i, vectorize(i, vocab)))
        
        return vectorized_corpus, vocab
            
    corpus, vocab = corpus2vectors([text_1, text_2]) 
    
    def cosine_sim(u,v):
        return np.dot(u,v) / (sqrt(np.dot(u,u)) * sqrt(np.dot(v,v)))

    u = corpus[0][1]
    v = corpus[1][1]
    
    return cosine_sim(u,v)

