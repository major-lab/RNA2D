#include <string>
#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>



bool is_valid_dot_bracket(std::string dot_bracket)
{ // tests Vienna dot-bracket for illegal dot_bracket (or symbol)
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
{ // removes the "." characters from the dot_bracket
    assert (is_valid_dot_bracket(dot_bracket));  // only apply on legal dot_bracket
    std::string ret = std::string(dot_bracket);
    ret.erase(std::remove(ret.begin(), ret.end(), '.'), ret.end());
    return ret;
}


struct Pair{
    int opening;
    int closing;
};



struct Stem{
    std::vector<int> opening;
    std::vector<int> closing;
    std::vector<Pair> pairs;
};



std::vector<Stem> getStems(std::string dot_bracket)
{ // return the stems in the dot_bracket
    assert (is_valid_dot_bracket((dot_bracket)));
    std::vector<Stem> stems = std::vector<Stem>();
    std::vector<int> openers = std::vector<int>();
    std::vector<int> stem_starts = std::vector<int>();

    int i = 0;
    int length = dot_bracket.size();
    Stem current_stem;
    Pair base_pair;
    int opener;
    while (i < length)
    {
        // opening
        if (dot_bracket[i] == '(')
        {
            openers.push_back(i);
            if (stems.empty())
            {
                stem_starts.push_back(i);
            }
        }

        // closing
        else if (dot_bracket[i] == ')')
        {
            // initialize new stem
            current_stem.opening = std::vector<int>();
            current_stem.closing = std::vector<int>();
            current_stem.pairs  = std::vector<Pair>();

            while (i < length)
            {
                if (dot_bracket[i] == ')')
                {
                    // pop the opening position
                    opener = openers.back();
                    openers.pop_back();

                    // create new base pair
                    base_pair.opening = opener;
                    base_pair.closing = i;

                    // add to new stem
                    current_stem.opening.push_back(opener);
                    current_stem.closing.push_back(i);
                    current_stem.pairs.push_back(base_pair);

                    // check if the stem is completed (its opening position was added)
                    if (std::find(stem_starts.begin(), stem_starts.end(), opener) == stem_starts.end())
                    {
                        break;
                    }
                }
                else if (dot_bracket[i] == '(')
                {
                    stem_starts.push_back(i);
                    i -= 1;
                    break;
                }
                i += 1;
            }
            stems.push_back(current_stem);
        }
        i += 1;
    }
    return stems;
}


std::vector<std::string> RNAshapes(std::string dot_bracket)
{ // convert dot_bracket to RNA abstract shapes lvl 1, 3 and 5
    std::vector<Stem> stems = get_stems(structure)

    // build the level 1 for each stems
    std::vector<int> range_occupied = std::vector<int>();
    dict_lvl1 = dict()
    Stem stem;
    std::vector<int> range_open;
    std::vector<int> range_close;
    std::vector<int> range_occupied = std::vector<int>();

    for (int j = 0; j != stems.size(); ++j)
    {
        stem = stems[j];
        range_open = std::vector<int>();
        range_close = std::vector<int>();

        for (int k = stem[0].back(); k != stem[0][0]+1; k++)
        {
            range_open.push_back(k);
            range_occupied.push_back(k);
        }
        for (int k = stem[1][0]; k!= stem[1].back(); k++)
        {
            range_close.push_back(k);
            range_occupied.push_back(k);
        }

        // convert stems to level 1 abstract shape, for each stem
        char c;

        // OPENING
        std::vector<char> opening = std::vector<char>();
        for (int index = 0; index != range_open.size(); ++index)
        {
            c = structure[range_open[index]];

            if (c == '(') && (opening.back() != '['))
            {
                opening.push_back('[');
            }
            else if ( (c == '.') && (opening.back() != '_') )
            {
                opening.push_back('_');

        }

        // CLOSING
        std::vector<char> closing = std::vector<char>();
        for (int index = 0; index != range_close.size(); ++index)
        {
            c = structure[range_close[index]];

            if ( (c == ')') && (closing.back() != ']') )
            {
                closing.push_back(']');
            }
            else if ( (c == '.') && (closing.back() != '_'))
            {
                closing.push_back('_');
            }
        }

        // rebalance the brackets
        while (opening.count('[') < closing.count(']'))
        {
            opening.insert(0, '[');
        }
        while (opening.count('[') > closing.count(']'))
        {
            closing.push_back(']');
        }

        dict_lvl1[str(min(stem[0]))] = opening
        dict_lvl1[str(min(stem[1]))] = closing
    }

    // assemble level 1
    level_1 = " "
    for i, element in enumerate(structure):
        level_1 += dict_lvl1.get(str(i), '').strip()
        if element == "." and level_1.back() != '_' and not i in range_occupied:
            level_1 += '_'

    level_1 = level_1.strip().replace("[_]", "[]")
    level_1 = level_1.replace(" ", '')
    level_1_str = std::string(level_1.begin(), level_1.end());

    // from level 1, build level 3 (remove unpaired '_' symbols)
    std::vector<char> level_3 = std::vector<char>();
    for(int i = 0; i != level_1.size(); ++i)
    {
        if (level_1[i] != '_')
        {
            level_3.push_back(level_1[i]);
        }
    }
    std::string level_3_str = std::string(level_3.begin(), level_3.end());

    // from level 3, build level 5 by removing nested stems
    std::vector<char> level_5 = level_3;
    while level_5.count("[[]]") > 0:
        level_5 = level_5.replace("[[]]", "[]")

    std::vector<std::string> result = {level_5_str, level_3_str, level_1_str};
    return result;
}


int main(int argc, char *argv[])
{
    std::string TEST = "(((..))..(.)..)";
    std::cout << "testing " << TEST << std::endl;
    std::vector<Stem> res = getStems(TEST);
    for (size_t i = 0; i != res.size(); ++i)
    {
        for(size_t j = 0; j != res[i].opening.size(); ++j)
        {
            std::cout << res[i].opening[j] << " " << res[i].closing[j] << std::endl;
        }

        std::cout << "end of stem " << i << std::endl;
    }
    return 1;

}


std::string shape_level_5(std::string dot_bracket){
    char db[dot_bracket.size()];
    int dblen=0;
    for( int i=0; i<dot_bracket.size(); ++i ){
        if( dot_bracket[i]!='.' )
        {
            char c = dot_bracket[i];
            c = c==')'?']':(c=='('?'[':c);
            db[dblen++]=c;
        }
    }

    //compute the idb (integer dot bracket) of the db
    int buddies[dblen];
    int stack[dblen];
    int sp=-1;
    int maxsp = -1; //needed to know if a db is only filled with '.'
    for( int i=0;i<dblen;++i ){
        if(db[i]=='['){
            stack[++sp]=i;
        } else if( db[i]==']' ){
            buddies[i]=stack[sp];
            buddies[stack[sp]]=i;
            --sp;
        }
        maxsp = maxsp>sp?maxsp:sp;
    }

    int slen = 1; //1 and not 0 because if db[0] != '.' then there is no room for the first (
    //1find length of shape
    for( int i=1; i<dblen; ++i ){
        if( ( buddies[i-1]-buddies[i]!=1 ) | ( db[i]!=db[i-1] ) ) ++slen;
    }
    // fill the shape
    std::vector<char> shape = std::vector<char>(slen+1);

    int next=0;
    if(maxsp>-1)shape[next++]='[';
    for( int i=1; i<dblen; ++i ){
        if( ( ( buddies[i-1]-buddies[i]!=1 ) | ( db[i]!=db[i-1] ) ) )
            shape[next++]=db[i];
    }
    std::string result = std::string(shape.begin(), shape.begin() + next); //shape[next]=0;
    return result;
}

