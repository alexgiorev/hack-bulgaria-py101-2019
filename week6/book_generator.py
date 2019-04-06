# how to run: python3 book_generator.py <number-of-chapters> <maximum-number-of-words-in-a-chapter>

import sys
import string
import random
import itertools

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 8

def randword():
    return ''.join(random.sample(string.ascii_lowercase,
                                 random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)))

def make_chapter(max_words):
    # returns a list of lines (no '\n' at the end)
    # the total number of words in the chapter will be less than or equal to @max_words
    
    lines = [] # result
    
    current_words = [] # the words of the current line
    Nwords_left = random.randint(1, max_words)
    while Nwords_left > 0:
        if random.randint(1, 10) == 1: # determines the newline frequency
            if current_words:
                lines.append(' '.join(current_words))
                current_words = []
        else:
            current_words.append(randword())
            Nwords_left -= 1
    lines.append(' '.join(current_words))
    return lines

def main():
    number_of_chapters = int(sys.argv[1])
    max_words = int(sys.argv[2])

    all_lines = []
    for chap_num in range(1, number_of_chapters + 1):
        all_lines.append(f'# Chapter {chap_num}')
        all_lines.extend(make_chapter(max_words))
        all_lines.append('\n')
    book = '\n'.join(all_lines)
    print(book)
    
main()
