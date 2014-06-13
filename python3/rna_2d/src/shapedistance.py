""" shapedistance module holds functions to create and compare abstract
shape (level 5, by Giergerich) based tree"""


from rna2d import(is_valid_dot_bracket, get_stems, only_paired)
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
        keys = [(k, self.shapes[k][1]) for k in keys]
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

    def build_stem(length):
        """builds a straight stem of given length"""
        assert length > 0
        root = Node(None)
        position = root
        for _ in range(0, length-1):
            child = Node(position)
            position = child
        return (root, position)

    stems = get_stems(dot_bracket)
    root = Node(None)
    stack = [root]
    abstract_shape_5 = []

    for stem in stems:
        abstract_shape_5.append(('o', stem[0][-1], len(stem[0])))
        abstract_shape_5.append(('c', stem[1][-1], len(stem[0])))
    abstract_shape_5.sort(key=lambda x: x[1])

    for decision in abstract_shape_5:
        if decision[0] == 'o':
            stem = build_stem(decision[2])
            stack[-1].append(stem[0])
            stack.append(stem[1])
        elif decision[0] == 'c':
            del(stack[-1])
    return root
