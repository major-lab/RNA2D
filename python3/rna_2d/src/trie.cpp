/*c++ lib implementation of Trie data structure
  with extern C declaration to allow dll*/

// g++ -c -fPIC trie.cpp -o trie.o
// g++ -shared -Wl,-soname,libtrie.so -o libtrie.so  trie.o


#include <iostream>
#include <vector>

using namespace std;

class Node
{
    public:
        Node() { content = ' '; marker = false; }
        ~Node() {}
        char get_content() { return content; }
        void setContent(char c) { content = c; }
        bool get_marker() { return marker; }
        void set_marker() { marker = true; }
        void appendChild(Node* child) { children.push_back(child); }
        vector<Node*> get_children() { return children; }

        Node* find_child(char c)
        { /*look into node's children to find c or return NULL*/
            for ( int i = 0; i < children.size(); i++ )
            {
                Node* tmp = children[i];
                if ( tmp->get_content() == c )
                {
                    return tmp;
                }
            }
            return NULL;
        }

    private:
        char content;
        bool marker;
        vector<Node*> children;

};


class Trie
{ /* Trie data structure */
    public:
        Trie()
        {
            root = new Node();
        }

        ~Trie()
        {
            // Free memory
        }

        void add_word(const char* s)
        {
            Node* current = root;
            int i = 0;
            for (const char* c = s; *c != '\0'; c++)
            {
                i++;
            }
            if (i == 0)
            {
                current->set_marker(); // an empty word
                return;
            }

            int strlen = i;
            i = 0;

            for (const char* c = s; *c != '\0'; c++)
            {
                Node* child = current->find_child(*c);
                if ( child != NULL )
                {
                    current = child;
                }

                else
                {
                    Node* tmp = new Node();
                    tmp->setContent(*c);
                    current->appendChild(tmp);
                    current = tmp;
                }

                if ( i == strlen -1 )
                {
                    current->set_marker();
                }
            i++;
            }
        }

        bool search_word(const char* s)
        {
            Node* current = root;
            while ( current != NULL )
            {
                for (const char* c = s; *c != '\0'; c++)
                {
                    Node* tmp = current->find_child(*c);
                    if ( tmp == NULL )
                    {
                        return false;
                    }
                    current = tmp;
                }

                if ( current->get_marker() )
                    return true;
                else
                    return false;
            }
            return false;
        }


    private:
        Node* root;
};


extern "C"
{   //shared lib interface
    // constructor
    Trie* new_trie(){ return new Trie(); }
    // add the word to the trie
    void  add_word(Trie* trie, const char* word){ trie->add_word(word); }
    // search for the word in the trie
    void  search_word(Trie* trie, const char* word){ trie->search_word(word); }

}


int main()
{
    // Test program
    Trie* trie = new Trie();
    trie->add_word("Hello");
    trie->add_word("Balloon");
    trie->add_word("Ball");

    if ( trie->search_word("Hell") )
        cout << "Found Hell" << endl;

    if ( trie->search_word("Hello") )
        cout << "Found Hello" << endl;

    if ( trie->search_word("Helloo") )
        cout << "Found Helloo" << endl;

    if ( trie->search_word("Ball") )
        cout << "Found Ball" << endl;

    if ( trie->search_word("Balloon") )
        cout << "Found Balloon" << endl;

    delete trie;
    const char* word = "works";

}