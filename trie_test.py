"""
CS3C, Final Project - Trie Tests
Jonathan Gordon
"""

import unittest
from trie import *


class TestTrie(unittest.TestCase):

    def testEmptyTrie(self):
        """Test empty Trie"""
        trie = Trie()
        self.assertEqual(len(trie), 0)

    def testInsert1(self):
        """Test inserting 1 element"""
        trie = Trie()
        trie.insert("guitar")
        self.assertEqual(len(trie), 1)

        # try to insert a duplicate
        trie.insert("guitar")
        self.assertEqual(len(trie), 1)

    def testInitWithWords(self):
        trie = Trie(["cat", "dog", "dogs"])
        self.assertEqual(len(trie), 3)

    def testSearch(self):
        words = ["he", "hello", "hat", "sin", "sing", "sit", "saw",
                 "quit", "quite", "quiz"]
        trie = Trie(words)
        self.assertEqual(len(trie), 10)

        for word in words:
            self.assertTrue(trie.search(word))

        # try to find a word that does not exist
        self.assertFalse(trie.search("not_there"))

        # try to find an empty string
        self.assertFalse(trie.search(str()))

        # try to find just a prefix
        self.assertFalse(trie.search("qui"))

    def testStartWith(self):
        words = ["he", "hello", "hat", "sin", "sing", "sit", "saw",
                 "quit", "quite", "quiz"]
        trie = Trie(words)

        # starts_with should find the prefix
        self.assertTrue(trie.starts_with("qui"))

        # starts_with  find complete words
        self.assertTrue(trie.starts_with("quiz"))

        # starts_with should NOT find non-existent words
        self.assertFalse(trie.starts_with("jon"))

        # starts with should find empty string
        self.assertTrue(trie.starts_with(""))




    def testAutoComplete(self):
        words = ["he", "hello", "hat", "sin", "sing", "sit", "saw",
                 "quit", "quite", "quiz"]
        trie = Trie(words)

        expected = ["quit", "quite", "quiz"]
        auto_complete_results = list(trie.autocomplete("qu"))

        # print(list(trie.autocomplete("qu")))
        self.assertEqual(sorted(expected), sorted(auto_complete_results))

        # test empty prefix. should return all words
        auto_complete_results = list(trie.autocomplete(""))
        # print(auto_complete_results)
        self.assertEqual(sorted(words), sorted(auto_complete_results))

    def testDelete(self):
        words = ["he", "hello", "hat", "sin", "sing", "sit", "saw",
                 "quit", "quite", "quiz"]
        trie = Trie(words)

        # delete a leaf node
        self.assertTrue(trie.delete("hello"))
        # word should be gone
        self.assertFalse(trie.search("hello"))
        # prefix word should still be there
        self.assertTrue(trie.search("he"))

        # delete a word with children
        self.assertTrue(trie.delete("sin"))
        # word should be gone
        self.assertFalse(trie.search("sin"))
        # word that contained the prefix word should be there
        self.assertTrue(trie.search("sing"))

        # delete a word that does not exist
        self.assertFalse(trie.delete("missing"))
        # words still exist
        self.assertTrue(trie.search("sing"))

    def testInsertDeleteMulti(self):
        trie = Trie()
        trie.insert("hello")
        self.assertEqual(len(trie), 1)

        trie.delete("hello")
        self.assertEqual(len(trie), 0)

        trie.insert("hello")
        self.assertEqual(len(trie), 1)
        trie.insert("hello")
        self.assertEqual(len(trie), 1)
        trie.insert("hello")
        self.assertEqual(len(trie), 1)

        trie.delete("hello")
        self.assertEqual(len(trie), 0)
        trie.delete("hello")
        self.assertEqual(len(trie), 0)
        trie.delete("hello")
        self.assertEqual(len(trie), 0)
