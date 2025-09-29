#include <iostream>
#include "RPN.hpp"

using namespace std;

int main() {

    // An example
    const char* infix = "1(*2-3)";

    RPN *rpn = new RPN(infix);

    cout << "Reverse Polish notation: " << rpn->getPostfix() << endl;

    cout << "Answer: " << rpn->getAns() << endl;

    delete rpn;

    return 0;
}
