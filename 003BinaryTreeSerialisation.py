# Daily Coding Problem 003:
#
# This problem was asked by Google.
# Given the root to a binary tree, implement serialize(root), which serializes
# the tree into a string, and deserialize(s), which deserializes the string
# back into the tree.
#
# For example, given the following Node class
# class Node:
#     def __init__(self, val, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
# The following test should pass:
# node = Node('root', Node('left', Node('left.left')), Node('right'))
# assert deserialize(serialize(node)).left.left.val == 'left.left'


import unittest


class Node:
    """ Node, the basic unit of the binary tree, consisting of a value,
        a left node and a right node
        """

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def add_node_to_list(node, nodelist):
    """ Recursively add the node and its children to the nodelist
    """

    for child in [node.left, node.right]:
        if not child:
            # keyword 'end' indicates no child
            nodelist.append('end')
        else:
            # add the child value to the list and recurse
            nodelist.append(child.val)
            add_node_to_list(child, nodelist)


def create_node_from_list(nodelist):
    """ Pop a value from the front of the nodelist, use it to build a
        node and recurse into the children
    """

    if len(nodelist) == 0:
        return None

    val = nodelist.pop(0)
    if val == 'end':
        return None

    return Node(val,
                create_node_from_list(nodelist),
                create_node_from_list(nodelist))


def serialise(root):
    """ Given a binary tree with root node 'root' return a serialised string
        describing that tree.
        Note, no checking done on data in val, so could easily screw up the
        format of the serialised list
    """

    nodelist = [root.val]
    add_node_to_list(root, nodelist)
    return ','.join(nodelist)


def deserialise(text):
    """ Given a serialised string, build the binary tree
    """

    nodelist = text.split(',')
    node = create_node_from_list(nodelist)
    return node


class SimpleTest(unittest.TestCase):
    """ Basic tests for serialize and deserialize """

    def setUp(self):
        self.tree1 = Node('root',
                          Node('left',
                               Node('left.left')),
                          Node('right'))

        self.tree2 = Node('root',
                          Node('left1',
                               Node('left1.left2',
                                    Node('left1.left2.left3'),
                                    Node('left1.left2.right3')
                                    )
                               ),
                          Node('right1',
                               None,
                               Node('right1.right2')
                               )
                          )

        self.tree3 = Node('root',
                          None,
                          Node('right1',
                               Node('right1.left2',
                                    Node('right1.left2.left3'),
                                    Node('right1.left2.right3',
                                         None,
                                         Node('right1.left2.right3.right4')
                                         )
                                    )
                               )
                          )

    def compare(self, n1, n2):
        """ Compare two nodes and their children
            Returns True if the trees are the same shape and all values match,
            else returns False
        """

        if n1.val != n2.val:
            return False

        for c1, c2 in [[n1.left, n2.left], [n1.right, n2.right]]:
            if not c1 and not c2:
                # Node has no children, compare the values
                return n1.val == n2.val
            elif c1 and c2:
                # Both nodes have children, compare them
                return self.compare(c1, c2)
            else:
                return False

    def test_tree1(self):

        s = serialise(self.tree1)

        self.assertEqual(s, 'root,left,left.left,end,end,end,right,end,end')

        d = deserialise(s)
        self.assertTrue(self.compare(d, self.tree1))

        # Test a specific node of the tree
        self.assertEqual(deserialise(s).left.left.val, 'left.left')

    def test_tree2(self):

        s = serialise(self.tree2)
        self.assertEqual(s, 'root,'
                                'left1,'
                                    'left1.left2,'
                                        'left1.left2.left3,'
                                            'end,'
                                            'end,'
                                        'left1.left2.right3,'
                                            'end,'
                                            'end,'
                                    'end,'
                                'right1,'
                                    'end,'
                                    'right1.right2,'
                                        'end,'
                                        'end'
                         )

        d = deserialise(s)
        self.assertTrue(self.compare(d, self.tree2))

    def test_tree3(self):

        s = serialise(self.tree3)
        self.assertEqual(s, 'root,'
                                'end,'
                                'right1,'
                                    'right1.left2,'
                                        'right1.left2.left3,'
                                            'end,'
                                            'end,'
                                        'right1.left2.right3,'
                                            'end,'
                                            'right1.left2.right3.right4,'
                                                'end,'
                                                'end,'
                                    'end')

        d = deserialise(s)
        self.assertTrue(self.compare(d, self.tree3))


if __name__ == "__main__":
    unittest.main()  # run all tests
