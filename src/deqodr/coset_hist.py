import qecc as q
import itertools as it
import numpy as np
from numpy import array, int16
import random

__all__ = ['free_energy_wt', 'coset_hist', 'freq_hist', 'toric_code',
             'starts', 'squares', 'stars', 'toric_log_xs', 
             'toric_log_zs']

def free_energy_wt(nq, prob, weight):
    """
    For a Pauli on `nq` qubits with weight `weight`, given a 
    depolarizing error model with error probability `prob`, 
    returns the contribution to the free energy from such a Pauli.
    """
    #Extreme ugliness
    f = (prob / (3. * (1. - prob)))**weight * (
        weight + 1. / np.log(3. * (1 - prob) / prob) * weight * \
        np.log(prob / 3.) + (nq - weight) * np.log(1. - prob)
        )
    return f

def coset_hist(stab_code, coset_rep=None):
    """
    This produces a np.histogram-style pair of 1d arrays containing 
    counts and bin markers (which mark the center of a bin)
    """
    bins = array(range(stab_code.nq + 1))
    vals = np.zeros((stab_code.nq + 1,))
    for elem in stab_code.stabilizer_group(coset_rep=coset_rep):
        vals[elem.wt] += 1

    return vals, bins

def freq_hist(stab_code, coset_rep=None, n_trials=10**5):
    """
    Does the exact same thing as coset_hist, but instead of iterating
    over the entire stabilizer group, performs a fixed number of trials
    """
    bins = array(range(stab_code.nq + 1))
    vals = np.zeros((stab_code.nq + 1,))
    
    len_gens = stab_code.nq - stab_code.nq_logical
    if coset_rep is None:
        coset_rep = q.eye_p(stab_code.nq)
    for _ in xrange(n_trials):
        #produce a random bitstring
        long_int = random.getrandbits(len_gens)
        bit_list = map(int, bin(long_int)[2:])
        bit_list = [0]*(len_gens - len(bit_list)) + bit_list
        
        #take product of stabilizers with coset rep depending on bit
        paul = coset_rep
        for idx, stab in enumerate(stab_code.group_generators):
            if bit_list[idx]:
                paul *= stab
        
        #add weight to histogram
        vals[paul.wt] += 1
    return vals, bins

#Should be a static method in qecc.StabilizerCode
def toric_code(n, m=None):
    """
    Given a length n, produces an n-by-n square lattice with closed 
    boundary conditions with a qubit on each edge, a Z stabilizer on 
    every square and an X stabilizer on every star. An optional second
    length allows for toric codes of non-unit aspect ratio.
    """
    if m == None:
        m = n
    
    sz = 2 * m * n
    
    z_stabs = map(lambda r: iter_pauli(r, q.Z, sz),
                                                list(squares(n, m)))
    x_stabs = map(lambda r: iter_pauli(r, q.X, sz), list(stars(n, m)))

    return q.StabilizerCode(z_stabs + x_stabs, toric_log_xs(n, m), 
                                                    toric_log_zs(n, m))

def starts(n, m, star = False):
    """
    Given a set of square dimensions n and m, returns the set of 
    co-ordinates at which square/star stabilizers are to 'start'. 
    """
    x_d, y_d  = xrange(n), xrange(m)
    for offset in y_d:
        for x in x_d:
            if (offset != m - 1) or (x != n - 1):
                yield x + (2 * offset + int(star)) * n 

def squares(n, m):
    """
    expands on starts, using closed boundary conditions and 
    premature optimization
    """
    for start in starts(n, m):
        square = array([start, start + n, 0, 0], dtype=int16)
        
        #wrap at right boundary
        if start % n == n - 1:
            square[2] = start + 1
        else:
            square[2] = start + n + 1
        
        #wrap on top
        if start >= 2 * (m - 1) * n:
            square[3] = start % n
        else:
            square[3] = start + 2 * n
        
        yield square

def stars(n, m):
    """
    expands on starts, using closed boundary conditions and 
    premature optimization
    """
    for start in starts(n, m, star=True):
        star = array([start, start - n, 0, 0], dtype=int16)
        
        #wrap at left boundary
        if start % n == 0:
            star[2] = start - 1
        else:
            star[2] = start - (n + 1)
        
        #wrap on bottom
        if start < 2 * n:
            star[3] = start + 2 * (m - 1) * n
        else:
            star[3] = start - 2 * n
        
        yield star

def toric_log_xs(n, m):
    """
    Returns the logical X operators for the toric_code on an n-by-m
    lattice. 
    """
    sz = 2 * n * m
    return[iter_pauli(range(n, 2 * n), q.X, sz), 
                    iter_pauli([2 * k * n for k in range(m)], q.X, sz)]

def toric_log_zs(n, m):
    """
    Returns the logical Z operators for the toric_code on an n-by-m
    lattice. 
    """
    sz = 2 * n * m
    return[iter_pauli(range(n), q.Z, sz), 
            iter_pauli([(2 * k + 1) * n for k in range(m)], q.Z, sz)]

to_p_dict = lambda arr, pauli: {elem : pauli for elem in arr}

def iter_pauli(ar, pl, sz):
    return q.Pauli.from_sparse(to_p_dict(ar, pl), sz)