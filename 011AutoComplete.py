# This problem was asked by Twitter
# Implement an autocomplete system. That is, given a query string s and a
# set of all possible query strings, return all strings in the set that have
# s as a prefix.
# For example, given the query string de and the set of strings
# [dog, deer, deal], return [deer, deal].
#
# Limitations: Missing some way of identifying words which exist as substrings
# in the tree, for example deal and dealer

import unittest
import pytest


class Treenode:

    def __init__(self, character):
        self.children = {}  # dict of character to treenode
        self.character = character

    def get_child(self, character):
        try:
            return self.children[character]
        except KeyError:
            return None

    def add_child(self, character):
        newnode = self.get_child(character)
        if not newnode:
            newnode = Treenode(character)
            self.children[character] = newnode
        return newnode

    def has_children(self):
        return len(self.children) > 0


class Tree:
    def __init__(self):
        self.root = Treenode('')

    def add(self, word):
        currentnode = self.root
        for character in word:
            currentnode = currentnode.add_child(character)

    def find_node_matching_query(self, query):
        currentnode = self.root

        for character in query:
            childnode = currentnode.get_child(character)
            if childnode:
                # Found
                currentnode = childnode
            else:
                # Not found
                currentnode = None
                break
        return currentnode

    def find_all_matching_queries(self, query):
        subnode = self.find_node_matching_query(query)
        all_matching_words = []
        self.get_all_subtrees(subnode, query, all_matching_words)
        if len(all_matching_words):
            print('Prefix: "{}", Found {}'
                  .format(query,
                          ', '.join(all_matching_words)))
        else:
            print('Prefix: "{}", Not found'.format(query))

        return sorted(all_matching_words)

    def get_all_subtrees(self, node, word_so_far, all_matching_words):
        if node:
            if node.has_children():
                # There are children
                for character, childnode in node.children.items():
                    self.get_all_subtrees(childnode,
                                          word_so_far + character,
                                          all_matching_words)
            else:
                # No children, not this is the only identifying feature of
                # having found a word, and would hide any words that are
                # substrings of other words. Fixable with a flag on the
                # treenode to indicate a complete word
                all_matching_words.append(word_so_far)
                return word_so_far
        else:
            # Didn't match
            return ''


class SimpleTest(unittest.TestCase):

    def test_tree(self):
        tree = Tree()
        tree.add('cat')
        tree.add('dog')
        tree.add('deal')
        tree.add('deer')
        tree.add('deemed')

        self.assertEqual(tree.find_all_matching_queries(
            'd'), ['deal', 'deemed', 'deer', 'dog'])

        self.assertEqual(tree.find_all_matching_queries(
            'do'), ['dog'])

        self.assertEqual(tree.find_all_matching_queries(
            'de'), ['deal', 'deemed', 'deer'])

        self.assertEqual(tree.find_all_matching_queries(
            'dr'), [])

        self.assertEqual(tree.find_all_matching_queries(
            ''), ['cat', 'deal', 'deemed', 'deer', 'dog'])


#
# Same tests, but using pytest!
#


@pytest.fixture
def tree():
    t = Tree()
    for i in ['cat', 'dog', 'deal', 'deer', 'deemed']:
        t.add(i)
    return t


@pytest.mark.parametrize('input, expected', [
    ('d', ['deal', 'deemed', 'deer', 'dog']),
    ('do', ['dog']),
    ('de', ['deal', 'deemed', 'deer']),
    ('dr', []),
    ('', ['cat', 'deal', 'deemed', 'deer', 'dog'])
])
def test_tree(tree, input, expected):
        assert tree.find_all_matching_queries(input) == expected


if __name__ == "__main__":
    unittest.main()  # run all tests
