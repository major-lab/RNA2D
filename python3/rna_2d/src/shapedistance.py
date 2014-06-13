""" shapedistance module holds functions to create and compare abstract
shape (level 5, by Giergerich) based tree"""


from rna2d import(is_valid_dot_bracket, get_stems)
from zhangshasha import(Node, unlabeled_distance)


def build_stem(length):
    """builds a straight stem of given length"""
    assert length > 0
    root = Node(None)
    position = root
    for _ in range(0, length-1):
        child = Node(position)
        position = child
    return (root, position)


def dot_bracket_to_tree(dot_bracket):
    """creates a abstract shape base pair tree from the Vienna dot bracket"""
    assert is_valid_dot_bracket(dot_bracket), "invalid dotbracket"
    stems = get_stems(dot_bracket)
    root = Node(None)
    stack = [root]
    abstract_shape_5 = []

    for stem in stems:
        abstract_shape_5.append(('o', stem[0][-1], len(stem[0])))
        abstract_shape_5.append(('c', stem[1][-1], len(stem[0])))
    abstract_shape_5.sort(key=lambda x: x[1])

    abstract_shape = ""
    for decision in abstract_shape_5:
        if decision[0] == 'o':
            stem = build_stem(decision[2])
            stack[-1].append(stem[0])
            stack.append(stem[1])
            abstract_shape += '['
        elif decision[0] == 'c':
            del(stack[-1])
            abstract_shape += ']'+str(decision[2])
    return (root, abstract_shape)


def remove_unpaired(dot_bracket):
    """remove '.' character from dot_bracket"""
    assert is_valid_dot_bracket(dot_bracket), "invalid dot-bracket"
    return "".join([i for i in dot_bracket if i != '.'])


def compare_shapes():
    """compares dotBracket A to dotBracket B"""
    

