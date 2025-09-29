#include "RPN.hpp"

bool RPN::isDigit(char c) {
    return (c >= '0' && c <= '9') || c == '.' || c == ',';
}

bool RPN::isLetter(char c) {
    return (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z');
}

// Operators priority
int RPN::Priority(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    if (op == '^') return 3;
    return 0;
}

// Make postfix from infix
void RPN::toPostfix() {
    nstd::stack<char> operators;
    size_t  len = strlen(infix),
            postfixSize = 0;

    // Не больше, чем инфиксная строка с пробелами
    postfix = new char[2 * len + 1];

    char currentNumber[32];
    int numberSize = 0;

    for (size_t i = 1; i < len; i++) {
        if (Priority(infix[i]) != 0 && (infix[i-1] == ')' || infix[i-1] == '(')) {
            throw std::invalid_argument("RPN::toPostfix(): Invalid operator");
        }
    }

    for (int i = 0; i < len; ++i) {
        char c = infix[i];

        if (c == ' ') continue;
        if (isDigit(c)) {
            currentNumber[numberSize++] = c;
        } else {
            if (numberSize > 0) {
                for (int j = 0; j < numberSize; j++) {
                    postfix[postfixSize++] = currentNumber[j];
                }
                postfix[postfixSize++] = ' ';
                numberSize = 0;
                memset(&currentNumber[0], 0, sizeof(currentNumber));
            }

            if (c == '(') {
                operators.push(c);
            } else if (c == ')') {
                while (!operators.empty() && operators.top() != '(') {
                    postfix[postfixSize++] = operators.top();
                    postfix[postfixSize++] = ' ';
                    operators.pop();
                }
                operators.pop();
            } else {
                if (isLetter(c) || !Priority(c))
                    throw std::invalid_argument("Invalid character '" + std::string(1, c) + "'");

                while (!operators.empty() && Priority(operators.top()) >= Priority(c)) {
                    postfix[postfixSize++] = operators.top();
                    postfix[postfixSize++] = ' ';
                    operators.pop();
                }
                operators.push(c);
            }
        }
    }

    if (numberSize > 0) {
        for (int i = 0; i < numberSize; i++) {
            postfix[postfixSize++] = currentNumber[i];
        }
        postfix[postfixSize++] = ' ';
        memset(&currentNumber[0], 0, sizeof(currentNumber));
    }

    while (!operators.empty()) {
        postfix[postfixSize++] = operators.top();
        postfix[postfixSize++] = ' ';
        operators.pop();
    }

    postfix[postfixSize] = '\0';
}

double RPN::evaluatePostfix() {
    nstd::stack<double> stack;
    char currentNumber[32];
    size_t  len = strlen(postfix),
            numberSize = 0;

    for (int i = 0; i < len; ++i) {
        char c = postfix[i];

        if (isDigit(c)) {
            currentNumber[numberSize++] = c;
        }
        else if (c == ' ') {
            if (numberSize > 0) {
                stack.push(atof(currentNumber));

                numberSize = 0;
                memset(&currentNumber[0], 0, sizeof(currentNumber));
            }
        }
        else {
            if (stack.size() < 2)
                throw std::invalid_argument("Insufficient number of arguments");

            double right = stack.top();
            stack.pop();
            double left = stack.top();
            stack.pop();

            switch (c) {
                case '+':
                    stack.push(left + right);
                    break;
                case '-':
                    stack.push(left - right);
                    break;
                case '*':
                    stack.push(left * right);
                    break;
                case '/':
                    if (right == 0.0)
                        throw std::invalid_argument("Divide by zero");
                    stack.push(left / right);
                    break;
                case '^':
                    stack.push(pow(left, right));
                    break;
                default:
                    throw std::invalid_argument("Unknown operator");
            }
        }
    }

    if (stack.size() != 1)
        throw std::invalid_argument("Incorrect postfix input");

    return stack.top();
}

char* RPN::getPostfix() {
    return postfix;
}

const double RPN::getAns() {
    return ans;
}
