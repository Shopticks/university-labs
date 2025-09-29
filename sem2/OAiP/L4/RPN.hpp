#ifndef RPN_HPP
#define RPN_HPP

#include <iostream>
#include "Stack.hpp"

class RPN {
private:
    const char* infix;
    char* postfix;
    double ans;

    bool isDigit(char c);
    bool isLetter(char c);

public:
    RPN(const char* infix) : infix(infix), postfix(nullptr), ans(0.0) {
        toPostfix();
        ans = evaluatePostfix();
    };

    int Priority(char op);

    void toPostfix();

    double evaluatePostfix();

    char* getPostfix();

    const double getAns();
};



#endif //RPN_HPP
