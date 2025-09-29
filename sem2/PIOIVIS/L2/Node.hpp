//
// Created by Shoptick on 21.02.25.
//

#ifndef NODE_HPP
#define NODE_HPP

#include <string>
#include <utility>
#include <vector>

struct Node {
    std::string name;
    std::vector<std::string> sets;

    explicit Node(std::string s) : name(std::move(s)) {}
};

#endif //NODE_HPP
