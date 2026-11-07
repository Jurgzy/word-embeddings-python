"""
ECS780P - Week 2 lab: a text pipeline you will keep
====================================================

Run it:                   python lab2.py
Check your own claims:    python test_lab2.py
Submit lab2.py only, by Friday 12:00.

Five functions. Together they turn a real text into numbers and back: the
first stage of the language model you will build in coursework 1. Next week's
lab imports them.

The file runs right now. Every function returns an empty answer until you
write it.
"""

PUNCTUATION = ".,;:!?'\"()-"


def tokenize(text):
    """Split a text into lowercase words.

    Input:   text, a string. It may contain punctuation, capitals, newlines
             and runs of spaces.
    Output:  a list of strings, one per word, in the order they appear.
             No punctuation, no capitals, no empty strings.

    Rules:   every character in PUNCTUATION counts as a space; letters are
             case-folded; words are whatever is left between spaces.

        tokenize("Hello, world! Hello.")   ->  ["hello", "world", "hello"]
        tokenize("a daisy-chain")          ->  ["a", "daisy", "chain"]
        tokenize("")                       ->  []
    """
    if text == "":
        return []
    
    for ch in PUNCTUATION:
        text = text.replace(ch, " ")

    tokens = text.casefold().split()

    return tokens


def count_words(tokens):
    """Count how many times each word appears.

    Input:   tokens, a list of strings.
    Output:  a dictionary. Keys are the distinct words, in the order they
             were first seen. Values are integers: how many times each
             word appears.

        count_words(["the", "cat", "the"])  ->  {"the": 2, "cat": 1}
        count_words([])                     ->  {}
    """
    counts = {}

    if len(tokens) ==0:
        return {}
        
    for word in tokens:
        counts[word] = counts.get(word, 0) + 1
        # key=word value is count.get(word) = which is the value, we set it to start at 0 +1 meanss add 1 every time we see the word and get the value=

    return counts


def build_vocabulary(tokens):
    """Give every distinct word a number.

    Input:   tokens, a list of strings.
    Output:  a dictionary. Keys are the distinct words, in the order they
             were first seen. Values are the integers 0, 1, 2, ... in that
             same order. A word that appears many times gets one number.

        build_vocabulary(["the", "cat", "the", "sat"])
            ->  {"the": 0, "cat": 1, "sat": 2}
        build_vocabulary([])  ->  {}
    """
    vocabulary = {}
    position = 0

    if len(tokens) == 0:
        return {}
        
    for word in tokens:
        position # use position variable
        if vocabulary.get(word) == None: # the word is not in vocab
            vocabulary[word] = position
            position += 1 #position increases by 1
        else:
            continue
            
    return vocabulary


def encode(tokens, vocabulary):
    """Replace each word by its number.

    Input:   tokens, a list of strings, and vocabulary, a dictionary of the
             kind build_vocabulary returns. Every word in tokens is a key of
             vocabulary.
    Output:  a list of integers, the same length as tokens, in the same
             order: the number of each word.

        encode(["the", "cat", "the"], {"the": 0, "cat": 1})  ->  [0, 1, 0]
        encode([], {"the": 0})                                ->  []
    """
    
    
    ids = []

    if len(tokens) == 0:
        return []
        
    for word in tokens:
        ids.append(vocabulary.get(word))
        
    return ids


def decode(ids, vocabulary):
    """Replace each number by its word. The exact reverse of encode.

    Input:   ids, a list of integers, and vocabulary, a dictionary of the
             kind build_vocabulary returns. Every integer in ids is a value
             in vocabulary.
    Output:  a list of strings, the same length as ids, in the same order:
             the word for each number.

        decode([0, 1, 0], {"the": 0, "cat": 1})  ->  ["the", "cat", "the"]
        decode([], {"the": 0})                    ->  []
    """
    words = []
    code_word = {}

    if len(ids) == 0:
        return []
        
    for key, value in vocabulary.items(): # select each value
        code_word
        code_word[value] = key # new dicitonary with code as key, word as value

    for code in ids:
        code_word
        words.append(code_word.get(code)) #add code word to list
    
    return words


# -----------------------------------------------------------------------------
# Runs only with `python lab2.py`. Reads alice.txt from the same folder.
# Leave it alone.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    text = """The cat sat on the mat.
The cat sat again!"""

    tokens = tokenize(text)
    counts = count_words(tokens)
    vocabulary = build_vocabulary(tokens)
    ids = encode(tokens, vocabulary)

    print(f"{tokens = }")
    print(f"{counts = }")
    print(f"{vocabulary = }")
    print(f"{ids = }")
    print(f"{decode(ids, vocabulary) = }")