#ifndef NODE_HPP
#define NODE_HPP
#include <__stddef_null.h>

template <typename T>
struct Node {
    T data = NULL;
    Node* next = nullptr;
    Node* prev = nullptr;
    explicit Node<T>(T d) : data(d), next(nullptr), prev(nullptr) {}
};

#endif //NODE_HPP
