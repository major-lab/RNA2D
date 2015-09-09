"""RNAshapes related functions"""


class UNode(object):
    def __init__(self, parent=None):
        self.parent = parent


class PNode(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []


def dot_bracket_to_tree(dot_bracket):
    """ transform a dotbracket into a tree structure of P and U nodes"""
    #assert is_valid_dot_bracket(dot_bracket)
    root = PNode(None)
    position = root
    for char in dot_bracket:
      if char == '.':    # unpaired
          position.children.append(UNode(position))
      elif char == '(':  # paired forward
          position.children.append(PNode(position))
          position = position.children[-1]
      else:              # paired backward
          position = position.parent
    return root.children


def print_tree(trees, open_symbol='(', close_symbol=')', unpaired_symbol='.'):
    """print the P-U node tree"""
    def print_helper(position, symbol_list):
        if isinstance(position, PNode):
            symbol_list.append(open_symbol)
            for children in position.children:
                print_helper(children, symbol_list)
            symbol_list.append(close_symbol)
        elif isinstance(position, UNode):
            symbol_list.append(unpaired_symbol)
        return

    str_reprs = []
    for tree in trees:
        cur = []
        print_helper(tree, cur)
        str_reprs.extend(cur)
    return "".join(str_reprs)


def level1(node):
    """to be used in a BFS traversal only"""
    # if node only has a single P child, remove self from the tree
    if (isinstance(node, PNode) and len(node.children) == 1):
        child = node.children[0]
        node.children = child.children
        child = None
        return True
    return False


def BFS_apply(tree, function):
    """BFS traversal application of the function"""
    queue = [tree]
    while len(queue) > 0:
      # dequeue the node
      current_node = queue.pop(0)

      # work on the current node
      modified = function(current_node)
      if modified:
          queue.insert(0, current_node)
      elif isinstance(current_node, PNode):
          for child in current_node.children:
              queue.append(child)
    return


def preprocess(dot_bracket):
    """ remove useless elements from the brackets using string functions"""
    # ... -> .
    processed = []
    lastchar = None
    for char in dot_bracket:
        if char == '.' and lastchar == '.':
            continue
        else:
            processed.append(char)
        lastchar = char
    db = "".join(processed)

    # (.) -> ()
    while db.count("(.)") > 0:
        db = db.replace("(.)", "()")

    return db


def RNAshapes(dot_bracket, level):
    """"the whole process wrapped"""
    assert level in [1, 3, 5]

    # first, preprocess the dot bracket (removing common patterns)
    db = preprocess(dot_bracket)
    trees = dot_bracket_to_tree(db)

    # level 1
    for tree in trees:
        BFS_apply(tree, level1)
    if level == 1:
        return print_tree(trees, open_symbol='[', close_symbol=']', unpaired_symbol='_')

    # level 3
    # "_" -> ""
    level3 = print_tree(trees, open_symbol='[', close_symbol=']', unpaired_symbol='_').replace("_", "")
    if level == 3:
        return level3

    # level 5
    # must remove nested stems (which were kept for level 3)
    level5 = level3
    level5 = level5.replace("[", "(").replace("]", ")")
    trees = dot_bracket_to_tree(level5)
    for tree in trees:
        BFS_apply(tree, level1)
    return print_tree(trees, open_symbol='[', close_symbol=']', unpaired_symbol='_')





# TESTING


import random
import random_dot_bracket
import subprocess
import shlex


def call_command(command, pipe=None, echo=False):
    """simple shell call interface for python"""
    if echo:
        print command

    process = subprocess.Popen(shlex.split(command.encode("ascii")),
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    output = process.communicate(input=pipe)
    return output


def test_random(n, levels=[1, 3, 5]):
    """ checks that the result is the same as the one given by RNAshapes"""
    errors = []
    for level in levels:
        for _ in range(n):
            dot_bracket = random_dot_bracket.add_unpaired_ends(random_dot_bracket.generate_random_dot_bracket(10, random.randint(0, 5)))
            command = "RNAshapes -D '{0}' -t {1}".format(dot_bracket, level)
            result, warning = call_command(command)
            result = result.strip()
            python_version = RNAshapes(dot_bracket, level)
            if python_version != result:
                errors.append((level, dot_bracket, python_version, result))
    return errors

