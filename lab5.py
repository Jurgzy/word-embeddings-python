"""
ECS780P - Week 5 lab: functions and modules
============================================

Run it:                   python lab5.py
Check your own claims:    python test_lab5.py
Submit lab5.py only, by Friday 12:00.

Four functions on lists of numbers. Three of them are how coursework 1
compares words: norm is in function 12, cosine in 13 and 14, accuracy in 16.
This file is a module: cw1.py says `import lab5` and uses them by name.

Each function has a frame; you write what goes between. The docstring is the
whole specification. Every sentence of it is a case the tests will try.
"""

import math


def dot(u, v):
    """The dot product of two vectors.

    Input:   u and v, two lists of numbers of the same length.
    Output:  a float: the sum of u[i] * v[i] over every position i.
             Two empty lists give 0.0.

        dot([1, 2, 3], [4, 5, 6])  ->  32.0
        dot([1, 0], [0, 1])        ->  0.0
        dot([], [])                ->  0.0
    """
    total = 0.0

    if len(u) == 0 or len(v) == 0:
        return 0.0
    if len(u) != len(v):
        return None

    for i in range(len(u)):
        total = total + (u[i]*v[i])

    float(total)
    
    return total
    


def norm(v):
    """The length of a vector.

    Input:   v, a list of numbers.
    Output:  a float: the square root of dot(v, v). A vector of zeros, or an
             empty list, has length 0.0.

        norm([3, 4])   ->  5.0
        norm([0, 0])   ->  0.0
        norm([1])      ->  1.0

    Uses: dot, math.sqrt
    """
    length = 0.0
    x = 0.0
    for i in range(len(v)):
        x = x + (v[i] ** 2)
    length = float(math.sqrt(x))
    return length
 
    ##  length = math.sqrt(dot(v,v)) # dot(v, v) would be the same as x = x + (v[i] ** 2)

def cosine(u, v):
    """Cosine similarity: how alike two vectors are in direction.

    Input:   u and v, two lists of numbers of the same length.
    Output:  a float between -1.0 and 1.0: dot(u, v) divided by the product
             of the two lengths. If either vector has length 0.0, the answer
             is 0.0: there is no direction to compare, and nothing is divided
             by zero.

        cosine([1, 0], [1, 0])   ->  1.0
        cosine([1, 0], [0, 1])   ->  0.0
        cosine([1, 0], [1, 1])   ->  0.7071067811865475
        cosine([0, 0], [1, 1])   ->  0.0

    Uses: dot, norm
    """
    similarity = 0.0
    if norm(u) == 0 or norm(v) == 0:
        return 0.0
    similarity = dot(u, v) / (norm(u) * norm(v))
    return similarity
    #

def accuracy(predicted, actual):
    """The fraction of predictions that are right.

    Input:   predicted and actual, two lists of the same length. The items
             can be anything that can be compared with ==.
    Output:  a float between 0.0 and 1.0: the number of positions i where
             predicted[i] == actual[i], divided by the length. Two empty
             lists give 0.0. A prediction of None never counts as right.

        accuracy(["a", "b"], ["a", "c"])     ->  0.5
        accuracy(["a", "b"], ["a", "b"])     ->  1.0
        accuracy([None, "b"], ["a", "b"])    ->  0.5
        accuracy([], [])                     ->  0.0
    """
    score = 0.0

    
    if len(actual) == 0 or len(predicted) == 0:
        return 0.0
    
    for i in range(len(actual)):
        if actual[i] == None or predicted[i] == None:
            continue
        
        if actual[i] == predicted[i]:
            score = score + 1
    return score / len(actual)


# -----------------------------------------------------------------------------
# Runs only with `python lab5.py`. Leave it alone.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    a = [2, 0, 1]
    b = [1, 1, 1]
    c = [0, 0, 0]

    print(f"{dot(a, b) = }")
    print(f"{norm(a) = }")
    print(f"{cosine(a, b) = }")
    print(f"{cosine(a, a) = }")
    print(f"{cosine(a, c) = }")
    print(f"{accuracy(['cat', 'dog', None], ['cat', 'cow', 'dog']) = }")
