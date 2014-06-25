#include<stdlib.h>
#include<stdio.h>
#include<string.h>


#define STRING_TERMINATOR '\0'

const char* dot_bracket_to_bracket(const char* dot_bracket)
{   //removes '.' symbol from the dot_bracket
    //returns a bracket...
    int i = 0;
    for(const char* c = dot_bracket; *c != STRING_TERMINATOR; c++)
    {   //find out the size of the string to return
        if(*c == '(' || *c == ')')
        {
            i++;
        }
    }
    i++; //leave emplacement for the STRING_TERMINATOR

    char* bracket = (char*) malloc(sizeof(char)* i);
    int j = 0;
    for(const char* c = dot_bracket; *c != STRING_TERMINATOR; c++)
    {
        if(*c == '(')
        {
            bracket[j] = '(';
            j++;
        }
        else if(*c == ')')
        {
            bracket[j] = ')';
            j++;
        }
    }
    return bracket;
}



UnlabeledRootedTree* bracket_to_unlabeled_tree(const char* bracket)
{   /* build an unlabeled rooted tree from the Vienna bracket
    * bracket means with '.' removed from the dot bracket
    */

    UnlabeledRootedTree* result = new UnlabeledRootedTree();
    UnlabeledNode* position = result->get_root();

    for(const char* c = bracket; *c != '\0'; c++)
    {
        if(*c == '(')
        {
            UnlabeledNode* child = new UnlabeledNode(position);
            position->add_to_children(child);
            position = child;
        }
        if(*c == ')')
        {
            position = position->get_parent();
        }
    }
    return result;
}




int main()
{
    //
    const char* a = "(((...)))";
    const char* b = "(((((....))..)))";
    const char* c = "((.))(.)((()...))";
    printf("%s\n", remove_dot(a));
    printf("%s\n", remove_dot(b));
    printf("%s\n", remove_dot(c));
    return 1;
}