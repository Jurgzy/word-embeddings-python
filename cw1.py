"""
ECS780P - Coursework 1: Words by the company they keep
=======================================================

Run the finished program:        python cw1.py train      (build and save a model)
                                 python cw1.py            (explore it)
Try things as you go:            cw1.ipynb  (unassessed)

Submit:  cw1.py, cw1.pdf, stopwords.txt, and lab2.py, lab3.py, lab4.py,
         lab5.py (this file imports them). Nothing else. Names are checked
         exactly.

You write the body of the 16 functions in Parts A to D. Each one has a frame
(the first and last lines); you fill in the middle. Each docstring states what
the function must do - its input, its output, and examples that must hold.
Several say "Uses:" and name a function from one of your lab files: that is
what you are expected to call.

Allowed imports: the ones already at the top of this file. Nothing else.

Everything after the line "PROVIDED CODE" is complete. You may change train()
and only train(): that is the performance component. Do not change
save_embeddings, load_embeddings, explore, corpus_files or the main block.

data/puzzles_dev.txt holds forty puzzles for development, built from the book
you were given. Marking uses a corpus that may be different and test puzzles
built from its words. Train on several books and write puzzles for them.
"""

import math
import os
import sys

import lab2
import lab3
import lab4
import lab5


# =============================================================================
# PART A - Text in
# =============================================================================

def load_corpus(paths):
    """Read several text files and join them into one string.

    Input:   paths, a list of file paths (strings). May be empty.
    Output:  one string: the contents of the files, in the order given,
             separated by a single newline character. No file -> "".

    Uses: lab4.read_text
    """
    contents = []
    for path in paths:
        if path == "":
            continue
        else:
            content = lab4.read_text(path)
            contents.append(content)
    text = "\n".join(contents) # single string with \n separater
    return text

def split_sentences(text):
    """Cut a text into sentences.

    Input:   text, a string.
    Output:  a list of strings. A sentence ends at '.', '!' or '?'. The
             ending mark is not part of the sentence. Each sentence has
             whitespace removed from its ends, and nothing else changed.
             Empty sentences are dropped.

        split_sentences("Hi. How are you? Fine!")  ->  ["Hi", "How are you", "Fine"]
        split_sentences("Really?! Yes.")           ->  ["Really", "Yes"]
        split_sentences("no ending")               ->  ["no ending"]
        split_sentences("")                        ->  []
    """
    sentences = []
    # remove punc (shown in list of punc) from the string and replace with a new line
    punctuation = ".!?"
    for i in punctuation:
        text = text.replace(i, ".") # or text = text.replace(".", "").replace("?", "").replace("!", "")
    # remove 
    pre_sentences = text.strip(".").split(".") # strips arg 
    # get rid of space in front of new sentences left after new lines
    for word in pre_sentences:
        if word.strip(): # checking if the string is empty
            sentences.append(word.strip()) # add non blank to list
    return sentences

def tokenize_sentences(sentences):
    """Tokenize every sentence.

    Input:   sentences, a list of strings.
    Output:  a list of lists of strings: each sentence replaced by its tokens.
             A sentence that produces no tokens is dropped entirely.

        tokenize_sentences(["How are you", "..."])  ->  [["how", "are", "you"]]

    Uses: lab2.tokenize
    """
    result = []
    for sentence in sentences:
        tokens = lab2.tokenize(sentence)
        if tokens: # ignore string with no tokens
                result.append(tokens)
    return result

def flatten(nested):
    """One list from a list of lists.

    Input:   nested, a list whose items are lists.
    Output:  a single list with every item of every inner list, in order.
             Only one level is flattened: an item that is itself a list
             inside an inner list stays as it is.

        flatten([[1, 2], [], [3]])     ->  [1, 2, 3]
        flatten([["a", ["b"]], ["c"]]) ->  ["a", ["b"], "c"]
        flatten([])                    ->  []
    """
    flat = []
    if len(nested) == 0: # blank list returns blank
        return []
    for nest in nested: # check every small list in the big list
        flat += nest # add small list to new list
    return flat

# =============================================================================
# PART B - Choosing words
# =============================================================================

def load_word_list(path):
    """Read a list of words from a file, one word per line.

    Input:   path to a text file.
    Output:     a list of strings.
                Each line gives one word:
                    whitespace removed from its ends,
                    case-folded.
                Blank lines and lines whose first non-blank character is '#' are ignored.
                A word that appears more than once is kept only the first time.
                Order is the file's order.

    Uses: lab4.read_lines
    """
    words = []
    seen = set() # set quicker to search
    pre_words = lab4.read_lines(path) # # txt file -> single string with new lines -> list with each word as element (new lines split the elements) --> list
    for pre_word in pre_words:
        word = pre_word.casefold().strip() # lower case preserving length & remove whitspace at ends... add to next list
        if word == "" or word.startswith("#"): # boolean checks
            continue
        if word not in seen:
            words.append(word)
            seen.add(word)
    return words

def remove_words(tokens, banned):
    """Drop every token that is in the banned collection.

    Input:   tokens, a list of strings; banned, a collection of strings to
             drop: a list, or a dictionary (then its keys are the banned
             words). A dictionary is allowed because a vocabulary IS a
             dictionary, and "which of these words are not in the
             vocabulary?" is a question this program asks.
    Output:  a new list with the tokens not in banned, in their original
             order. Comparison is exact: "The" and "the" are different.

        remove_words(["the", "cat", "sat"], ["the"])          ->  ["cat", "sat"]
        remove_words(["cat", "zebra"], {"cat": 0, "dog": 1})  ->  ["zebra"]
    """
    kept = []
    banned_set = set(banned) # set has quicker checks, if banned is dict, puts keys in set
    for token in tokens: # each word
        if token not in banned_set:
            kept.append(token)
    return kept

def select_context_words(counts, n):
    """The n most frequent words.

    Input:   counts, a dictionary word -> count; n, a non-negative integer.
    Output:  a list of the n words with the highest counts, highest first.
             Words with equal counts are in alphabetical order. If n is
             larger than the number of words, every word is returned.

        select_context_words({"a": 2, "b": 5, "c": 2}, 2)  ->  ["b", "a"]

    Uses: lab3.most_common
    """
    pre_context_words = lab3.most_common(counts, n)
    context_words = []
    for pre_context_word in pre_context_words:
        context_words.append(pre_context_word[0])
    return context_words

# =============================================================================
# PART C - Vectors
# =============================================================================

def count_cooccurrences(sentences, window):
    """Count how often each pair of words appears near each other.

    Input:   sentences, a list of lists of tokens; window, a positive int.
    Output:  a dictionary (target, context) -> count, where context is a
             token within `window` positions of target in the SAME sentence.
             Pairs never cross from one sentence into the next.

        count_cooccurrences([["a", "b"], ["b", "c"]], 1)
            ->  {("a","b"): 1, ("b","a"): 1, ("b","c"): 1, ("c","b"): 1}

    Uses: lab3.context_pairs
    """
    cooc = {}
    for sentence in sentences:
        pairs = lab3.context_pairs(sentence, window) # list of tuples
        for pair in pairs:
            cooc[pair] = cooc.get(pair, 0) + 1
    return cooc

def make_vector(word, cooc, context_words):
    """The vector for one word: how often it appears near each context word.

    Input:   word, a string; cooc, a dictionary (target, context) -> count;
             context_words, a list of strings.
    Output:  a list of numbers, one per context word, in the same order as
             context_words: the count for (word, context), or 0 if that pair
             was never seen.

        make_vector("a", {("a", "b"): 3}, ["b", "c"])  ->  [3, 0]
    """
    # if a not in -> return 0
    # how many times is word next to each of words in context list
    # make sure word is in cooc also
    vector = [] 
    for context_word in context_words:
        pair = (word, context_word) # (a, b)
        vector.append(cooc.get(pair, 0)) # return the value if in the dict otherwise return 0 
    return vector

def build_embeddings(words, cooc, context_words):
    """A vector for every word.

    Input:   words, a list of strings; cooc and context_words as above.
    Output:  a dictionary word -> vector (as make_vector gives it), with the
             words as keys in the order given. A word listed twice has one
             entry.

        build_embeddings(["a", "b"], {("a", "b"): 2}, ["a", "b"])
            ->  {"a": [0, 2], "b": [0, 0]}

               for i in range(len(words)):
        j = make_vector(words[i], cooc, context_words)
    #    embeddings.update({words[i]:j})
        embedding[words[i]] = j
    """
    embeddings = {}
    for word in words:
        embeddings.update({word:make_vector(word, cooc, context_words)})
    return embeddings
    
def log_weight(vector):
    """Squash large counts: replace every number x by log(1 + x).

    Input:   vector, a list of numbers >= 0.
    Output:  a new list of floats of the same length. 0 stays 0.0.

        log_weight([0, 1])  ->  [0.0, 0.6931471805599453]

    Uses: math.log
    """
    weighted = []
    for number in vector:
        if number == 0:
            weighted.append(float(0.0))
        else:
            weighted.append(float(math.log(1 + number)))
    return weighted

def normalize(vector):
    """Scale a vector to length 1.

    Input:   vector, a list of numbers.
    Output:  a new list of floats (floats even when the input holds ints):
             every entry divided by the vector's length (its norm). A vector
             of length 0 comes back as a list of 0.0 of the same size.

        normalize([3, 4])  ->  [0.6, 0.8]
        normalize([0, 0])  ->  [0.0, 0.0]

    Uses: lab5.norm
    """
    unit = []
    length = lab5.norm(vector)
    for number in vector:
        if length == 0:
            unit.append(float(0.0))
        else:
            unit.append(float(number / length))
    return unit

# =============================================================================
# PART D - Using the vectors
# =============================================================================

def most_similar(word, embeddings, n):
    """The n words whose vectors are most similar to word's vector.

    Input:   word, a string; embeddings, a dictionary word -> vector;
             n, a non-negative integer.
    Output:  a list of (other_word, similarity) pairs, most similar first,
             with cosine similarity as the measure.
             
             The word itself is never in the list.
             Equal similarities are in alphabetical order.
             If n is larger than the number of other words, every other word is returned.
             If word is not in embeddings, the list is empty.


             most_similar("cat",   {"cat": [1, 2],      , 2)  -> [("kitten", 0.999), ("dog", 0.992)]
                                  "dog": [2, 3],
                                  "kitten": [1, 2.1],
                                  "car": [-1, 2]}

    Uses: lab5.cosine, lab3.most_common
    """
    # return list of tuples (other_word, similarity) 
    #cosine used to measure similarity
    # word in the list word not tested
    # if same similarity alphabetically first word used
    if word not in embeddings:
        return []
    result = []
    word_vectors = embeddings[word]
    sim_dict = {}
    for other_word, other_vector in embeddings.items(): # list of word-vector pairs
        if other_word == word:
            continue
        similarities = lab5.cosine(word_vectors, other_vector)
        sim_dict[other_word] = similarities
    result = lab3.most_common(sim_dict, n)
    return result

def odd_one_out(words, embeddings):
    """Which word does not belong?

    Input:   words, a list of at least two strings, all present in
             embeddings; embeddings, a dictionary word -> vector.
    Output:  the word whose total cosine similarity to the other words is
             lowest. If two words tie, the one that comes first in `words`.

    embeddings = {
    "apple": [1, 0],
    "banana": [0.9, 0.1],           -->  ["computer"]
    "computer": [-1, 0]}

words = ["apple", "banana", "computer"]

    Uses: lab5.cosine
    """
    answer = words[0] # select first word  from words
    lowest_sim = float("inf") # use the float constructor to creat infinity which is larger than the cosine's could ever be
    for word in words:
        running_sim = 0.0
        for other_word in words:
            if other_word != word: # ignore comparing to self
                running_sim += lab5.cosine(embeddings[word], embeddings[other_word]) # cosine running total
        if running_sim < lowest_sim: # if new low found
            lowest_sim = running_sim
            answer = word
    return answer
    
def load_puzzles(path):
    """Read odd-one-out puzzles from a file.

    Input:   path to a text file. Each puzzle is one line: the words,
             separated by spaces, then a semicolon, then the answer. Blank
             lines and lines whose first non-blank character is '#' are
             ignored. Case does not matter: everything is case-folded.
    Output:  a list of (words, answer) pairs: words is a list of strings,
             answer is a string.

        a line  "Cat dog  Table ; table"  ->  (["cat", "dog", "table"], "table")

    Uses: lab4.read_lines
    """
    puzzles = []
    puzz_list = lab4.read_lines(path) # list of string
    for line in puzz_list:
        line = line.strip().casefold() #remove end spaces then lowercase
        if line == "" or line.startswith("#"): # ignore these
            continue
        parts = line.split(";") # list of separate words and answer
        words = parts[0].split() # list of words
        answer = parts[1].strip() #remove end spaces to leave just word
        puzzles.append((words, answer))
    return puzzles

def evaluate(puzzles, embeddings):
    """How many puzzles does the model get right?

    Input:   puzzles, a list of (words, answer) pairs; embeddings, a
             dictionary word -> vector.
    Output:  a float between 0 and 1: the fraction of puzzles for which
             odd_one_out returns the answer. 
             
             A puzzle with any word missing
             from embeddings counts as wrong.
             
             No puzzles -> 0.0.

        puzzles = [(["cat", "dog", "wolf", "car"], "car"), (["dog", "wolf", "car"], "car")]
        embeddings = {"cat": [1, 0], "dog": [0.9, 0.1], "wolf": [0.8, 0.2], "car": [0, 1]}
        
    Uses: lab5.accuracy
    """
    if len(puzzles) == 0:
        return 0.0
    predicted = []
    actual = []
    for puzzle in puzzles:
        words = puzzle[0]
        answer = puzzle[1]
        actual.append(answer)
        if any(word not in embeddings for word in words): #check each word, if word in embeddings
            predicted.append(None)
        else:
            predicted.append(odd_one_out(words, embeddings))
    result = float(lab5.accuracy(predicted, actual))
    return result

def count_word_total(cooc):
    ''' find the total number of cooccurences of a word in the cooc dict.
    input the cooc dict and output a dict with a word as the key and its count as the value.
       
    '''
    word_total = {}
    for pair, count in cooc.items():
        word = pair[0] # assign word from tuple pair
        if word not in word_total: # add word with count to dict
            word_total[word] = 0 # make the value an int
        word_total[word] += count # add the counts to the countvalue
    return word_total

def ppmi(word, context_words, cooc, word_total, total_pairs):
    ''' calculate a vector value that isnt affected by negative cooccurences
    '''
    word_count = word_total.get(word, 0) # find count or return 0
    ppmi_vector = []
    for context_word in context_words:
        count = cooc.get((word, context_word), 0)
        if count == 0 or word_count == 0 or total_pairs == 0:
            ppmi_vector.append(0.0)
            continue
        context_count = word_total.get(context_word, 0) # count or return 0
        if context_count == 0:
            ppmi_vector.append(0.0)
            continue
        score = math.log( (count * total_pairs) / (word_count * context_count) )
        ppmi_vector.append(max(0.0, score))
    return ppmi_vector

# =============================================================================
# PROVIDED CODE - complete. Change train() only.
# =============================================================================

def save_embeddings(path, embeddings):
    lines = []
    for word, vector in embeddings.items():
        numbers = []
        for x in vector:
            numbers.append(f"{x:.6f}")
        lines.append(word + " " + " ".join(numbers))
    lab4.write_lines(path, lines)


def load_embeddings(path):
    embeddings = {}
    for line in lab4.read_lines(path):
        parts = line.split()
        if len(parts) > 1:
            vector = []
            for x in parts[1:]:
                vector.append(float(x))
            embeddings[parts[0]] = vector
    return embeddings


def train(corpus_paths, stopwords_path, window=4, n_context=2000):
    """The baseline pipeline. Improve it for the performance component, but
    keep its name, its first two parameters, and the shape of what it returns:
    a dictionary word -> list of numbers, every list the same length, keyed
    by whole lowercase words (the puzzles are made of those).

    The marking run calls this with a corpus that may differ from the one you
    were given, and with the stopwords.txt YOU submit. Curate that file."""
    text = load_corpus(corpus_paths)
    sentences = tokenize_sentences(split_sentences(text))
    stopwords = load_word_list(stopwords_path)
    cleaned = []
    for sentence in sentences:
        cleaned.append(remove_words(sentence, stopwords))
    counts = lab2.count_words(flatten(cleaned))
    context_words = select_context_words(counts, n_context)
    cooc = count_cooccurrences(cleaned, window)
    embeddings = {}
    word_total = count_word_total(cooc)
    # Calculate this only ONCE
    total_pairs = sum(cooc.values())
    for word in counts:
        ppmi_vector = ppmi(word, context_words, cooc, word_total, total_pairs)
        embeddings[word] = normalize(ppmi_vector)
    return embeddings


def explore(embeddings):
    """Type a word to see its neighbours; several words to find the odd one
    out; q to quit."""
    print(f"{len(embeddings)} words. Type a word, or several words, or q.")
    while True:
        line = input("> ").strip().casefold()
        if line == "q" or line == "":
            break
        words = line.split()
        unknown = remove_words(words, embeddings)
        if len(unknown) > 0:
            print("  not in the vocabulary:", " ".join(unknown))
        elif len(words) == 1:
            for other, score in most_similar(words[0], embeddings, 10):
                print(f"  {other:15} {score:.3f}")
        else:
            print("  odd one out:", odd_one_out(words, embeddings))


def corpus_files(folder):
    paths = []
    for name in sorted(os.listdir(folder)):
        if name.endswith(".txt"):
            paths.append(os.path.join(folder, name))
    return paths


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, "data")
    saved = os.path.join(data, "embeddings.txt")

    if len(sys.argv) > 1 and sys.argv[1] == "train":
        embeddings = train(corpus_files(os.path.join(data, "corpus")),
                           os.path.join(data, "stopwords.txt"))
        save_embeddings(saved, embeddings)
        puzzles = load_puzzles(os.path.join(data, "puzzles_dev.txt"))
        print(f"trained on {len(embeddings)} words; "
              f"dev accuracy {evaluate(puzzles, embeddings):.3f}; saved to {saved}")
    elif os.path.exists(saved):
        explore(load_embeddings(saved))
    else:
        print("No saved model yet. Run:  python cw1.py train")
