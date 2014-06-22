#include <sstream>
#include <string>
#include <assert.h>
#include <vector>
#include <algorithm>
#include <utility>
#include <iostream>
#include <stdio.h>


using namespace std;

// class Foo{
// public:
//     vector<int> V;
//     void bar(){
//         cout << "Hello" << endl;
//     }
//             void push(int x){
//                 V.push_back(x);
//             }
//                     void print(){
//                         for(int i=0; i<V.size(); i++)
//                         {
//                             cout << V[i] <<endl;
//                         }
//                     }
//                             vector<int> get_v()
//                             {
//                                 return V;
//                             }
// };
// 
// extern "C" {
//     Foo* Foo_new(){ return new Foo(); }
//       void Foo_bar(Foo* foo){ foo->bar(); }
//         void Foo_push(Foo* foo, int x){ foo->push(x); }
//           void print(Foo* foo){foo->print();}
//             vector<int> Foo_get_v(Foo* foo){foo->get_v();}
// }


struct shape_bracket
{
    bool closing;
    int position;
    int size;
};


bool compare(struct shape_bracket a, struct shape_bracket b)
{
    if (a.position < b.position)
    {
        return true;
    }
    else
    {
        return false;
    }
}


class Node
{   /*A simple node object that can be used to construct trees*/
    public:
        string label;
        vector<Node*> children;
        Node* parent;

        Node()
        {
            string label = "";
            vector<Node*> children;
            Node* parent = NULL;
        }

        Node(Node* par)
        {
            string label = "";
            vector<Node*> children;
            Node* parent = par;
        }

        Node(Node* par, string lab)
        {
            string label = lab;
            vector<Node*> children;
            Node* parent = par;
        }

        Node* get_parent()
        {/*get the parent*/
            return parent;
        }

        vector<Node*> get_children()
        {/*get the children vector*/
            return children;
        }

        string get_label()
        {/*get the label (string)*/
            return label;
        }

        void append(Node* other)
        {/**/
            children.push_back(other);
            std::cout << "children updated "<<std::endl;
        }
};


bool is_valid_dot_bracket(string dot_bracket)
{    /*returns wether or not the dot bracket is proper formed Vienna*/
    int count = 0;
    for(int i = 0; i < dot_bracket.length(); i++)
    {
        char c = dot_bracket[i];
        if(c == '(')
        {
            count += 1;
        }
        else if(c == ')')
        {
            count -= 1;
        }
        else if(c != '.')
        {
            return 0;
        }
        if(count < 0)
        {
            return 0;
        }
    }
    if(count != 0)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}


string only_paired_bracket(string dot_bracket)
{   /*removes unpaired symbol '.'*/
    vector<char> result;
    for(int i = 0; i < dot_bracket.size(); i++)
    {
        char c = dot_bracket[i];
        if(c == '(' || c == ')')
        {
            result.push_back(c);
        }
    }
    return string(result.begin(), result.end());
}


vector<pair<vector<int>, vector<int> > > get_stems(string dot_bracket)
{
    vector<int> list_opener;
    vector<int> list_stem_end;
    vector<pair<vector<int>,vector<int> > > stems;
    int i = 0;
    int length = dot_bracket.size() -1;
    while(i <= length)
    {/*outher while*/
        if(dot_bracket[i] == '(') // 1
        {
            list_opener.push_back(i);
        }

        else if(dot_bracket[i] == ')') // 2
        {
            pair<vector<int>, vector<int> > stem;
            while(i <= length) // 3
            {/*nested while*/
                if(dot_bracket[i] == ')') // 4
                {
                    int opener = list_opener.back();
                    list_opener.pop_back();
                    stem.first.push_back(opener);
                    stem.second.push_back(i);
                    if((list_opener.size()!= 0) &&
                        (find(list_stem_end.begin(), // 5
                                   list_stem_end.end(),
                                   list_opener.back()) != list_stem_end.end()))
                    {
                        list_stem_end.push_back(list_stem_end.back());
                        break; // 6
                    }
                }
                else if(dot_bracket[i] == '(') // 7
                {
                    if(list_opener.size() != 0) // 8
                    {
                        list_stem_end.push_back(list_opener.back());
                    }
                    i -= 1;
                    break; // 9
                }
                i += 1;
            }
            stems.push_back(stem);
        }
        i += 1;
    }
    return stems;
}


pair<Node*, Node*> build_stem(int length)
{/*builds a stem of given length and returns the root and the end of the stem*/
    Node root = new Node();
    Node* position = &root;
    for(int i = 1; i < length; i++)
    {
        Node child = new Node(position);
        position = &child;
    }
    return(pair<Node*, Node*>(&root, position));
}


Node* dot_bracket_to_tree(string dot_bracket)
{
    assert(is_valid_dot_bracket(dot_bracket));
    vector<pair<vector<int>, vector<int> > > stems = get_stems(dot_bracket);
    Node* root = new Node();
    vector<Node*> stack;
    stack.push_back(root);
    //figure out the abstract shape
    vector<struct shape_bracket > abstract_shape_5;
    for(int i = 0; i < stems.size(); i++)
    {
        shape_bracket first = {false, stems[i].first.back(), stems[i].first.size()};
        shape_bracket second = {true, stems[i].second.back(), stems[i].first.size()};
        abstract_shape_5.push_back(first);
        abstract_shape_5.push_back(second);
//         std::cout << "size " << first.size << " position " << first.position << std::endl;
//         std::cout << "size " << second.size << " position " << second.position << std::endl;
    }

    sort(abstract_shape_5.begin(), abstract_shape_5.end(), compare);
    std::cout << dot_bracket <<std::endl;
    for(int i = 0; i < abstract_shape_5.size(); i++)
    {
        char c;
        if(abstract_shape_5[i].closing == false)
        {
            c = '[';
        }
        else
        {
            c = ']';
        }
        std::cout << c ;
    }
    std::cout << "\n";
    for(int i = 0; i < abstract_shape_5.size(); i++)
    {
        std::cout << "position " << abstract_shape_5[i].position << " size "<< abstract_shape_5[i].size << std::endl;
//         std::cout << abstract_shape_5[i].closing << " " << abstract_shape_5[i].closing << std::endl;
        if(abstract_shape_5[i].closing == false) /*opening*/
        {
            pair<Node*, Node*> stem = build_stem(abstract_shape_5[i].size);
            std::cout << "got here " << std::endl;
            (stack.back())->append(stem.first);
            std::cout << "child length " << stack.back()->children.size() << "\n";
            stack.push_back(stem.second);
        }
        else /*closing*/
        {
            stack.pop_back();
        }
    }
    return root;
}


int main()
{
//    vector<pair<vector<int>, vector<int> > > stems = get_stems("(((()(()))))");
//     std::cout << stems.size()<<"\n";
//     for(int i=0; i<stems.size(); i++)
//     {
//         std::cout << "first back : " << stems[i].first.back() << " " << stems[i].first.size() <<"\n";
//         std::cout << "sec   back : " << stems[i].second.back() << "\n";
//         std::cout << "\n";
//     }
    Node* N = dot_bracket_to_tree("((())((()())))");
    return 1;
}
// Node* dot_bracket_to_tree(string dot_bracket)
// {
//     
// }
// 
// 
extern "C"
{
    
}