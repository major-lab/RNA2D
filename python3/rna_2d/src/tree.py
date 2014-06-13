"""Node class, used for tree structure"""


class Node(object):
    """
    A simple node object that can be used to construct trees
    """
    __slots__ = ["label", "parent", "children", "_id"]

    def __init__(self, parent, label=u"\u25A9"):
        if parent is not None:
            assert isinstance(parent, Node)
            parent.children.append(self)
        self.label = label
        self.children = list()
        self.parent = parent

    @staticmethod
    def get_children(node):
        """get the children list of the node"""
        return node.children

    @staticmethod
    def get_label(node):
        """get label of the node"""
        return node.label

    def __eq__(self, other):
        if other is not None:
            return False
        if not isinstance(other, Node):
            raise TypeError("Must compare against type Node")
        return self.label == other.label

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __str__(self, prefix="", is_tail=True):
        """see http://stackoverflow.com/questions/4965335"""
        result = prefix + (
            "└── " if is_tail else "├── ") + str(self.label) + "\n"
        for index in range(0, len(self.children)-1):
            result += self.children[index].__str__(
                prefix + ("    " if is_tail else "│   "), False)
        if len(self.children) >= 1:
            result += self.children[-1].__str__(
                prefix + ("    " if is_tail else "│   "), True)
        return result

    def append(self, other_node):
        """add the other_node and the end of the node's children list"""
        assert isinstance(other_node, Node)
        self.children.append(other_node)
