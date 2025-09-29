#ifndef NODE_HPP
#define NODE_HPP
#include <__stddef_null.h>

template <typename T>
struct Node {
    T data = NULL;
    Node* next = nullptr;

    explicit Node<T>(T d) : data(d), next(nullptr) {}
};

#endif //NODE_HPP
