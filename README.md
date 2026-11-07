# word-embeddings-python

A Python NLP project using PPMI word embeddings and cosine similarity to builds word embeddings from text and uses them to find and semantic similarity between words and identify the odd word out in a group.

Approach
The pipeline reads text files, splits them into sentences, tokenizes words and removes stopwords. It counts word co-occurrences within a configurable context window, then applies positive pointwise mutual information (PPMI) weighting and normalises the resulting vectors. Cosine similarity is used to compare words. For odd-one-out prediction, the program selects the word with the lowest total similarity to the other words in the group.

Technologies
•	Python 3
•	Python standard library
•	Dictionaries, sets, lists and modular functions

No third-party Python packages are required.

Results
Using the original training corpus and development puzzles, with a context window of four tokens and 2,000 context words.

Metric	Result
Corpus files	17
Input tokens before stopword removal	Approximately 2.43 million
Vocabulary size	70,560 words
Embedding dimensions	2,000
Accuracy across all development puzzles	65.8% (179/272)
Accuracy excluding puzzles containing words absent from the training corpora
	72.5% (179/247)
The filtered result excludes 25 puzzles. These are development results measured on data used for experimentation and parameter selection.

File Setup
Place the files in these locations:

Location	Contents
Main project folder	cw1.py, lab2.py, lab3.py, lab4.py, lab5.py
data/stopwords.txt	Stopword list
data/puzzles_dev.txt	Development puzzles
data/corpus/	Training corpus text files
Reproducing the reported results requires the original corpus, stopword list and development puzzles.

Running the Project
From the main project folder, train and save the embeddings using python cw1.py train. The program saves the model to data/embeddings.txt and prints the accuracy across all development puzzles.

Start the interactive explorer using python cw1.py explore. Enter one word to see its nearest neighbours, or several words to identify the odd one out. Enter q to quit.

My Contribution
I implemented the functions for text processing, vocabulary selection, co-occurrence counting, vector construction, similarity ranking and evaluation. I extended the training pipeline with PPMI weighting and compared context-window sizes and context-vocabulary sizes. I also replaced repeated list searches with dictionary lookups during vector construction.

The course supplied the function specifications and supporting code for saving, loading and interactively exploring embeddings.

I used ChatGPT for explanations, example inputs, assertions and stress-testing support, as documented in my coursework report.

Limitations and Future Work
Rare words may have insufficient context to produce useful embeddings. Similarity depends on patterns in the training text, and words absent from the vocabulary cannot be compared.
Possible extensions include lemmatisation, automated tests and comparison with pretrained embeddings.
