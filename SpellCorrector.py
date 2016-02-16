"""
A simple spell checker and corrector which can correct the word error.
TODO: Use linguistic model to correct the sentence error.
"""

import re, collections

def get_words(text):
    """
    Converts every word to lowercase
    :param text: input word sequence
    :return: separated word sequence in lowercase
    """
    return re.findall('[a-z]+', text.lower())

def langModel(wordseq):
    """
    Language Model: Using work frequency to get the probability of the word
    :param wordseq: input big word sequence
    :return: the frequency of each word in the word sequence
    """

    # specify the default value of a key to be 1, i.e., the smoothing in Language Model
    # if the word is not in the dictionary, the value will be 1.
    wordCount = collections.defaultdict(lambda: 1)
    for word in wordseq:
        wordCount[word] += 1
    return wordCount

dictionary = langModel(get_words(file('shakespeare.txt').read())) # all the words in the language model
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def dist1_words(word):
    """
    Assuming the word length is n, see below the number of each error type.
    Get all the possible similar words which has edit distance of 1 compared the input word
    :param word: input word
    :return: all the possible similar words which has edit distance of 1 compared the input word
    """

    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b] # n deletions
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1] # n-1 transpositions
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b] # 26n alterations
    inserts    = [a + c + b     for a, b in splits for c in alphabet] # 26(n+1) insertions
    return set(deletes + transposes + replaces + inserts)

def dist2_words(word):
    """
    Get all the possible similar words which has edit distance of 2 compared the input word
    and which is in the language model.
    :param word: input word
    :return: all the possible similar words which has edit distance of 2 compared the input word
    """
    return set(word2 for word1 in dist1_words(word) for word2 in dist1_words(word1))

def legal_words(words):
    """
    Get all the words in the dictionary.
    :param words: input word sequence
    :return: words in the dictionary
    """
    return set(w for w in words if w in dictionary)

def correct_word(word):
    """
    Correct one word
    :param word: input word
    :return: correct word
    """

    # treat the distance 1 error and distance 2 error as equal probability
    # the main idea to put the last candidates of [words] is that we treat novel word having frequency 1
    possibleWords = legal_words([word]) or legal_words(dist1_words(word)) or legal_words(dist2_words(word)) or [word]
    return max(possibleWords, key=dictionary.get)

def correct_words(sentence):
    """
    Correct word sequence
    :param words: input word sequence
    :return: correct word sequence
    """
    words = get_words(sentence)

    #return set(correct_word(word) for word in words )
    return ' '.join(correct_word(word) for word in words)

if __name__ == '__main__':
    # test samples
    print correct_word("spell")
    print correct_word("spel")
    print correct_word("checke")
    print correct_word("checer")
    print correct_words("teis is a simpl spel corrector")