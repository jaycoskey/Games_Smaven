#!/usr/bin/env python

import unittest
import yaml


from gtree import GTree


class TestGTree(unittest.TestCase):
    def test_word_1x1(self):
        gtree = GTree()
        # print(gtree)
        assert(not gtree.has_word('a'))

    def test_word_1x3(self):
        gtree = GTree()
        gtree.add_word('bet')
        # print(gtree)
        assert(gtree.has_word('bet'))

    def test_word_4x3(self):
        gtree = GTree()
        words = ['net', 'not', 'pet', 'pot']
        gtree.add_wordlist(words)
        # print(gtree)
        for word in words:
            assert(gtree.has_word(word))


if __name__ == '__main__':
    runner = unittest.main()
