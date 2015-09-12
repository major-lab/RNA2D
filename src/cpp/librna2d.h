
#ifndef LIBRNA2D_H
#define LIBRNA2D_H

#include <string>
#include <vector>
#include <iostream>
#include <cassert>
#include <algorithm>
#include <map>
#include <deque>



// simple check for balance and symbols used
bool is_valid_dot_bracket(std::string dot_bracket);


// only level 1, 3 and 5 implemented
std::string RNAshapes(std::string dot_bracket, int level);



#endif // LIBRNA2D_H
