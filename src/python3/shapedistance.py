""" shapedistance module holds functions to create and compare abstract
shape (level 5, by Giergerich) based tree"""


from rna2d import(is_valid_dot_bracket, only_paired)
from zhangshasha import(Node, unlabeled_distance)


class ShapeSet(object):
    """abstract shape level 5 with annotation
    we only care about global similarity, not local
    in this class"""

    __slots__ = ["shapes"]

    def __init__(self):
        self.shapes = dict()  # maps {pairs_dot_bracket => (tree, count)}

    def __len__(self):
        return len(self.shapes)

    def __getitem__(self, item):
        assert is_valid_dot_bracket(item), "invalid dot-bracket"
        return self.shapes[only_paired(item)]

    def __contains__(self, item):
        assert is_valid_dot_bracket(item), "invalid dot-bracket"
        return only_paired(item) in self.shapes

    def add(self, item):
        """adds the dot-bracket to the shape dict"""
        assert is_valid_dot_bracket(item), "invalid dot-bracket"
        item = only_paired(item)
        actual = self.shapes.get(item, (dot_bracket_to_tree(item), 0))
        self.shapes[item] = (actual[0], actual[1] + 1)

    def get_keys(self):
        """get the ordered list of the dict keys"""
        keys = list(self.shapes.keys())
        keys.sort()
        keys.sort(key=len)  # will only work since the sort is stable
        keys = [(k, self.shapes[k]) for k in keys]  # (dotB, (Node, qt))
        return keys

    @staticmethod
    def __is_all_pairs(dot_bracket):
        """tells whether or not the dot-bracket has "." symbol"""
        for symbol in dot_bracket:
            if symbol == '.':
                return False
        return True


def dot_bracket_to_tree(dot_bracket):
    """creates a abstract shape base pair tree from the Vienna dot bracket"""
    assert is_valid_dot_bracket(dot_bracket), "invalid dot-bracket"
    root = Node()
    position = root
    for c in dot_bracket:
        if c == '(':
            child = Node(position)
            position.append(child)
            position = child
        elif c == ')':
            position = position.parent
        else:
            continue
    return root
