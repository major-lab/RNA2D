"""wrapper over c++ implementation of Trie data structure"""

from ctypes import cdll
lib_trie = cdll.LoadLibrary('./libtrie.so')

#NOTE : with python3, all strings must be encoded, because cpp
# uses bytes, not the damn unicode

class Trie(object):
    def __init__(self):
        # constructor
        self.obj = lib_trie.new_trie()

    def add_word(self, word):
        # add a word to the trie
        lib_trie.add_word(self.obj, str.encode(word))

    def search_word(self, word):
        # search for the word
        return bool(lib_trie.search_word(self.obj, str.encode(word)))
