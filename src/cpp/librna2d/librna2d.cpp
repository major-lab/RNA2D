#include "librna2d.h"


bool is_valid_dot_bracket(std::string dot_bracket)
{   // tests Vienna dot-bracket for illegal dot_bracket (or symbol)
    int counter = 0;

    for (unsigned int i = 0; i < dot_bracket.size(); ++i)
    {
        char c = dot_bracket[i];
        if (c == '(')               // stack
        {
            counter += 1;
        }
        else if (c == ')')          // unstack
        {
            counter -= 1;
        }
        else if (c != '.')          // illegal character
        {
            return false;
        }
        if (counter < 0)            // left unbalanced
        {
            return false;
        }
    }
    if (counter != 0)               // right unbalanced
    {
        return false;
    }
    else                            // correct dotbracket
    {
        return true;
    }
}


std::string only_paired(std::string dot_bracket)
{   // removes the "." characters from the dot_bracket
    assert (is_valid_dot_bracket(dot_bracket));  // only apply on legal dot_bracket
    std::string ret = std::string(dot_bracket);
    ret.erase(std::remove(ret.begin(), ret.end(), '.'), ret.end());
    return ret;
}


class Node{
public:
    Node(char label, Node parent)
    {
        parent_ = parent;
        label_ = label;
        children_ = std::vector<Node>();
    }
    ~Node();

    Node* parent_;
    std::string label_;
    std::vector<Node> children_;

};


std::vector<Node*> dot_bracket_to_tree(std::string dot_bracket)
{ // transform a dotbracket into a tree structure of P and U nodes
    Node root = Node('r', NULL);
    Node* position = &root;
    char c;
    for (size_t i = 0; i != dot_bracket.size(); ++i)
    {
        c = dot_bracket[i];
        if (c == '.')       // unpaired
        {
            position->children.push_back(Node('U', position));
        }
        else if (c == '(')  // paired
        {
            position->children.push_back(Node('P', position));
            position = position->children.back();
        }
        else
        {
            position = position->parent;
        }
    }
    return root.children;
}


void print_helper(Node* position, std::vector<char>& symbol_list,
                  char open_symbol, char close_symbol, char unpaired_symbol)
{ //
    Node children;
    if (position->label_ == 'P')
    {
        symbol_list.push_back(open_symbol);
        for (size_t i = 0; i != position->children_.size(); ++i)
        {
            children = position->children_[i];
            print_helper(children, symbol_list, open_symbol, close_symbol, unpaired_symbol);
        }
        symbol_list.push_back(close_symbol);
    }
    else if (position->label_ =='U')
    {
        symbol_list.push_back(unpaired_symbol);
    }
    return;
}


std::string print_tree(std::vector<Node> trees, char open_symbol='(', char close_symbol=')', char unpaired_symbol='.')
{ //
    std::vector< std::vector<char> > str_reprs = std::vector< std::vector<char> >();
    for (size_t i = 0; i != trees.size(); ++i)
    {
        std::vector<char> current = std::vector<char>();
        print_helper()
    }
}

def print_tree(trees, open_symbol='(', close_symbol=')', unpaired_symbol='.'):
    """print the P-U node tree"""


    str_reprs = []
    for tree in trees:
        cur = []
        print_helper(tree, cur)
        str_reprs.extend(cur)
    return "".join(str_reprs)


bool level1(Node* node)
{   // to be used in a BFS traversal only
    Node child;
    if ( (node->label == 'P') && (node->children.size() == 1) )
    {
        child = node->children[0];
        node->children = child.children;
        child = NULL;
        return true;
    }
    else
    {
        return false;
    }
}

void BFS_apply(Node* subTree, bool(*fun)(Node*))
{
    std::queue<Node*> Q = std::queue<Node*>();
    Q.enque(subTree);

    bool modified;
    Node* current_node;
    while(Q.size() > 0)
    {
        current_node = Q.pop();
        modified = (*fun)(current_node);
        if (modified)
        {
            Q.insert(0, current_node);
        }
        else if (current_node->label_ == 'P')
        {
            for (size_t i = 0; i != current_node->children_.size(); ++i)
            {
                Q.push_back(current_node->children_[i]);
            }
        }
    }
    return;
}


std::string preprocess(std::string dot_bracket)
{
    // ... -> .
    std::vector<char> step1 = std::vector<char>();
    char currentChar;
    char lastChar = NULL;
    for (size_t i = 0; i != dot_bracket.size(); ++i)
    {
        currentChar = dot_bracket[i];
        if ( (currentChar =='.') && (lastChar == currentChar))
        {
            // don't add
            continue;
        }
        else
        {
            step1.push_back(currentChar);
        }
        lastChar = currentChar;
    }

    std::cout << dot_bracket << std::endl;
    std::cout << std::string(step1.begin(), step1.end()) << std::endl;

    // (.) -> ()
    std::vector<char> step2 = std::vector<char>();
    step2.push_back(step1[0]);

    for(size_t i = 1; i != step1.size()-1; ++i)
    {
        if ( (step2.back() == '(') && (step1[i] == '.') && (step1[i+1] == ')') )
        {
            continue;
        }
        else
        {
            step2.push_back(step1[i]);
        }
    }
    step2.push_back(step1.back());

    return std::string(step2.begin(), step2.end());
}


std::string RNAshapes(std::string dot_bracket, int level)
{
    assert(level == 1 || level == 3 || level==5);

    // preprocess the dot bracket to remove useless patterns
    std::string cleaned = preprocess(dot_bracket);
    std::vector<Node*> trees = dot_bracket_to_tree(cleaned);

    // apply level 1
    Node* subtree;
    for (size_t i = 0; i != trees.size(); ++i)
    {
        subtree = trees[i];
        BFS_apply(subtree, (*level1));
    }
    std::string level1_str = print_tree(trees);
    if (level == 1)
    {
        return level1_str;
    }


    std::vector<char> level3 = std::vector<char>();
    for (size_t i = 0; i != level1_str.size(); ++i)
    {
        if (level1_str[i] != '_')
        {
            level3.push_back(level1_str);
        }
    }
    std::string level3_str = std::string(level3.begin(), level3.end());
    if (level == 3)
    {
        return level3_str;
    }

    //
    std::vector<char> level5 = std::vector<char>();
    for(size_t i = 0; i != level3_str.size(); ++i)
    {
        if (level3_str[i] == '[')
        {
            level5.push_back('(');
        }
        else if (level3_str[i] == ']')
        {
            level5.push_back(')');
        }
    }
    trees = dot_bracket_to_tree(std::string(level5.begin(), level5.end()));
    for (size_t i = 0; i != trees.size(); ++i)
    {
        subtree = trees[i];
        BFS_walk(subtree, (*level1));
    }
    return print_tree(trees);
}




