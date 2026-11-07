"""
ECS780P - Week 3 lab: which words appear near which
=====================================================

Run it:                   python lab3.py        (needs your lab2.py in this folder)
Check your own claims:    python test_lab3.py
Submit lab3.py only, by Friday 12:00.

Lab 2 turned a text into words. Lab 3 adds the second stage: for every word,
which words appear near it, and how often. Coursework 1 imports two of these
four functions (context_pairs and most_common), so get them exactly right.

Four functions. Each has a frame; you write what goes between.
The file runs right now. Every function returns an empty answer until you
write it.
"""


def context_pairs(sequence, window):
    """Every (target, context) pair in a sequence, for a given window.

    Input:   sequence, a list of items (usually strings); window, an integer
             >= 0.
    Output:  a list of tuples (target, context). For each position in the
             sequence, the item there is the target, and every OTHER position
             at distance 1 up to window is a context. Positions before the
             start or past the end of the sequence do not exist and produce
             no pair. Order: by target position, then by context position.
             A window of 0, or a sequence of fewer than two items, gives [].

        context_pairs(["a", "b", "c"], 1)  ->  [("a","b"), ("b","a"), ("b","c"), ("c","b")]
        context_pairs(["a", "b", "c"], 2)  ->  [("a","b"), ("a","c"), ("b","a"), ("b","c"),
                                                ("c","a"), ("c","b")]
        context_pairs(["a"], 2)            ->  []
    """
    pairs = [] 
    for i in range(len(sequence)): # takes values 0-len(seq)
            for j in range(i - window, i + window + 1): # for every i, take number range -2 -> end
                if 0 <= j < len(sequence) and i != j: # restrict range of j 0-len and i and j cant be the same- prevents matching a word with itself
                    pairs.append((sequence[i], sequence[j])) # add the word at i and the word at j as a tuple in pairs
                      
    return pairs


def cooccurrence_counts(pairs):
    """How many times each pair appears.

    Input:   pairs, a list of tuples, as context_pairs gives them.
    Output:  a dictionary pair -> count. Keys are the pairs exactly as given,
             in the order they were first seen. Values are integers.

        cooccurrence_counts([("a","b"), ("b","a"), ("a","b")])  ->  {("a","b"): 2, ("b","a"): 1}
        cooccurrence_counts([])                                  ->  {}
    """
    counts = {}
    
    for pair in pairs: # each tuple in pairs
        counts[pair] = counts.get(pair, 0) + 1 # grab count from dictionary and add 1 (starts at 0)
        
    return counts


def most_common(counts, n):
    """The n entries with the largest values.

    Input:   counts, a dictionary whose values are numbers; n, an integer >= 0.
    Output:  a list of (key, value) tuples, largest value first. Entries with
             equal values are ordered by key, smallest key first ("smallest"
             as Python compares them: alphabetical for strings). If n is
             larger than the number of entries, every entry is returned.
             counts itself is not changed.

        most_common({"a": 2, "b": 5, "c": 2}, 2)  ->  [("b", 5), ("a", 2)]
        most_common({"a": 2, "b": 5, "c": 2}, 9)  ->  [("b", 5), ("a", 2), ("c", 2)]
        most_common({}, 3)                        ->  []
    """
    result = []
    items = list(counts.items()) # creates list from the count dictionary
    
    while len(result) < n and len(items) > 0: # results up to size they want (i.e. 2 best counts) and items still in list
        best = items[0] # add first item to best
        for item in items: # grab each item from list... checking the digits of the count???
            if item[1] > best[1] or (item[1] == best[1] and item[0] < best[0]):
                # if first is bigger than ?? check in class
                # or if item and best are the same and previous item less than previous best
                best = item # best now has same value as item
        result.append(best) # after finding the last best (highest), add it to results
        items.remove(best) # remove highest no. and go to next iteration of while loop (until the length of results < n)
        
    return result


def first_index(sequence, item): # looking for item in sequence
    """Where an item first appears.

    Input:   sequence, a list or a string; item, anything.
    Output:  the position (counting from 0) of the first occurrence of item in
             sequence, or -1 if it does not occur.

        first_index(["a", "b", "a"], "a")  ->  0
        first_index(["a", "b", "a"], "z")  ->  -1
        first_index("banana", "n")         ->  2
    """
    position = -1

    for i in range(len(sequence)): # as many times as the no. of entries
        if sequence[i] == item: # the item is same as the element at index i
            return i # return the index
    return -1 # return -1 if the item has not been found in the sequence list



# -----------------------------------------------------------------------------
# Runs only with `python lab3.py`. Uses your lab2.py and alice.txt from this
# folder. Leave it alone.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    from lab2 import tokenize

    with open("alice.txt", encoding="utf-8") as f:
        tokens = tokenize(f.read())

    pairs = context_pairs(tokens, 2)
    counts = cooccurrence_counts(pairs)

    print(f"{len(tokens) = }")
    print(f"{len(pairs) = }")
    print(f"{pairs[:6] = }")
    print(f"{most_common(counts, 5) = }")
    print(f"{first_index(tokens, 'alice') = }")
