
#ifndef LIBRNA2D_H
#define LIBRNA2D_H

#include <string>
#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>
#include <map>
#include <deque>



struct Pair{
    int opening;
    int closing;
};


class Stem{
public:
    Stem()
    {
        opening= std::vector<int>();
        closing = std::vector<int>();
        pairs = std::vector<Pair>();
    }
    ~Stem();

    std::vector<int> opening;
    std::vector<int> closing;
    std::vector<Pair> pairs;
};


std::vector<Stem> getStems(std::string dot_bracket);

std::string RNAshapes(std::string dot_bracket);





#endif // LIBRNA2D_H
