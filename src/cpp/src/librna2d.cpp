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


