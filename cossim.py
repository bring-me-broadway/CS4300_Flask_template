import numpy as np
from numpy import linalg as LA

def build_cossim(input_doc_mat):
    """Returns a similarity matrix of size (num_musicals,num_musicals) where for (i,j):
        [i,j] should be the cosine similarity between the musical with index i and the musical with index j
        
    Note: Set values on the diagonal to 1
    to indicate that all musicals are trivially perfectly similar to themselves.
    
    Params: input_doc_mat: Numpy Array
    Returns: Numpy Array 
    """
    dm_t = np.transpose(input_doc_mat)
    dot = np.matmul(input_doc_mat, dm_t)
    norms = np.apply_along_axis(LA.norm, 1, input_doc_mat)
    intermediate = np.divide(dot,norms)
    sim_mat = np.divide(np.transpose(intermediate),norms)
    np.fill_diagonal(sim_mat,1)
    return sim_mat