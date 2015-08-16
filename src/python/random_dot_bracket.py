"""Random dot bracket generation"""

import math
import random
from rna2d import is_valid_dot_bracket

class _Node(object):
    """A simple node object that can be used to construct ordered trees"""
    def __init__(self, parent, label):
        assert label in ["unpaired", "paired"]
        self.label = label
        self.children = list()
        self.parent = parent

    def get_children(self):
        """get the children list of the node"""
        return self.children

    def insert_random(self, other_node):
        """insert the node at a random position"""
        assert isinstance(other_node, _Node)
        other_node.parent = self
        self.children.insert(random.randint(0, len(self.children)), other_node)
        return

    def append(self, other_node):
        """add the other_node and the end of the node's children list"""
        assert isinstance(other_node, _Node)
        other_node.parent = self
        self.children.append(other_node)
        return


class _OrderedTree(object):
    def __init__(self, dot_bracket="()"):
        assert is_valid_dot_bracket(dot_bracket)

        # initialize structures empty
        self.artificial_root = _Node(None, "paired")
        self.pairs = [self.artificial_root]
        position = self.artificial_root
        # fill it
        for character in dot_bracket:
            # unpaired
            if character == ".":
                position.append(_Node(position, "unpaired"))
            # pair opening
            elif character == "(":
                position.append(_Node(position, "paired"))
                self.pairs.append(position.children[-1])
                position = position.children[-1]
            # pair closing
            else:
                position = position.parent
        return


    def insert_random(self, other_node):
        """insert a node at a random position"""
        assert isinstance(other_node, _Node)
        # choose the insertion point
        insertion_node = self.pairs[random.randint(0, len(self.pairs)-1)]
        # perform insertion
        insertion_node.insert_random(other_node)
        # if it is a pair, add it to the pairs
        if (other_node.label == "paired"):
            self.pairs.append(other_node)
        return

    def __str__(self):
        """string representation is Vienna dot bracket"""
        return self.to_dot_bracket()

    def to_dot_bracket(self):
        """do a pre-order traversal of the tree to convert to dot brackets"""
        traversal_list = []
        def helper(position):
            for child in position.children:
                # unpaired
                if child.label == "unpaired":
                    traversal_list.append(".")
                # paired
                else:
                    traversal_list.append("(")
                    helper(child)
                    traversal_list.append(")")
            return
        helper(self.artificial_root)
        return "".join(traversal_list)

    def __repr__(self):
        return str(self)


def generate_random_dot_bracket(length, num_base_pairs):
    """generate a random valid RNA 2D structure of specified length"""
    assert isinstance(length, int), "length must be integer"
    assert length > 1, "cannot create structure of length {}".format(length)

    # choose how many nucleotides will be paired/unpaired
    num_unpaired = length - (2 * num_base_pairs)
    tree = _OrderedTree()
    paired = [_Node(None, "paired") for _ in range(num_base_pairs)]
    unpaired = [_Node(None, "unpaired") for _ in range(num_unpaired)]
    paired.extend(unpaired)
    random.shuffle(paired)
    for node in paired:
        tree.insert_random(node)
    return str(tree)

__all__ = ["generate_random_dot_bracket"]