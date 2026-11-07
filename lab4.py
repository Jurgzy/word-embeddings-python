"""
ECS780P - Week 4 lab: files
============================

Run it:                   python lab4.py        (reads and writes files in this folder)
Check your own claims:    python test_lab4.py
Submit lab4.py only, by Friday 12:00.

Until now every text your programs used was typed into the code. Real text
lives in files. These four functions are how coursework 1 reads its corpus,
its stopwords and its puzzles, and how it saves what it learned. Coursework 1
imports read_text, read_lines and write_lines from this file.

Four functions. Each has a frame; you write what goes between. The file runs
right now: the reading functions return empty answers and the writing
functions do nothing until you write them.
"""


def read_text(path):
    """The whole file as one string.

    Input:   path, a string: where the file is, relative to the folder you
             run Python from. The file is UTF-8 text.
    Output:  one string holding everything in the file, in order, nothing
             removed: newlines included, spaces included. Windows line
             endings come back as "\\n", which is what Python's text mode
             does. An empty file gives "".

        a file holding  cat<newline>dog<newline>  ->  "cat\\ndog\\n"
    """
   
    # open the file with correct encoding
    with open(path, encoding = "utf-8") as f:
        text = f.read() # returns single string including new lines
    return text


def read_lines(path):
    """The file as a list of lines.

    Input:   path, as above.
    Output:  a list of strings, one per line, in order. Each line has its
             line ending removed ("\\n" or "\\r\\n") and nothing else changed:
             spaces and tabs inside or at the ends of a line are kept. A blank
             line is an empty string. A last line with no line ending is still
             a line. An empty file gives [].

        a file holding  cat<newline><newline>dog  ->  ["cat", "", "dog"]
    """
  #  lines = []
    with open(path, encoding = "utf-8") as f:
        lines = f.read().casefold().splitlines() # creates a list of strings with removes the spaces and new lines from the single string (same as lines = read_text(path).splitlines() )
    return lines


def write_lines(path, lines):
    """Write a list of strings to a file, one per line.

    Input:   path, as above; lines, a list of strings.
    Output:  nothing (None). After the call the file holds every string in
             lines, in order, each followed by "\\n", and nothing else. Any
             content the file had before is gone. An empty list gives an
             empty file. The file is UTF-8.

        write_lines(p, ["a", "b"])  then  read_text(p)  ->  "a\\nb\\n"
    """

    
    # call the file to write in
    with open(path, "w", encoding = "utf-8") as f: # call file to wipe and write
        for line in lines: # each string in list 
            f.write(line + "\n") # write the string and a new line
    
    return None # returns nothing, writes to file


def append_line(path, line):
    """Add one line to the end of a file.

    Input:   path, as above; line, a string.
    Output:  nothing (None). After the call the file holds what it held
             before, then line, then "\\n". If the file did not exist, it is
             created. Assume an existing file ends with a line ending, as
             every file written by write_lines does.

        append_line(p, "c")  on a file holding "a\\nb\\n"  ->  "a\\nb\\nc\\n"
    """
    with open(path, "a", encoding = "utf-8") as f: # call file to add string at the end
        f.write(line + "\n") # add string at the end with new line
    return None


# -----------------------------------------------------------------------------
# Runs only with `python lab4.py`. Reads alice.txt from this folder and writes
# two small files beside it. Leave it alone.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    text = read_text("alice.txt")
    lines = read_lines("alice.txt")
    print(f"{len(text) = }")
    print(f"{len(lines) = }")
    print(f"{lines[:2] = }")

    write_lines("sample.txt", ["first", "second"])
    append_line("sample.txt", "third")
    print(f"{read_lines('sample.txt') = }")

    append_line("log.txt", "ran lab4.py")
    print(f"{len(read_lines('log.txt')) = } run(s) so far")
