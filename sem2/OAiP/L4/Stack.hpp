#ifndef STACK_HPP
#define STACK_HPP

#include "Node.hpp"
#include <iostream>
namespace nstd {
    template<class T>
class stack {
    private:
        Node<T>* head = nullptr;
        size_t stackSize = 0;
    public:
        stack(){}

        bool empty() {
            return head == nullptr;
        }
        void push(T value) {
            Node<T> *newNode = new Node<T>(value);

            newNode->next = head;
            head = newNode;
            stackSize++;
        }
        void pop(){
            if (head == nullptr)
                throw std::out_of_range("Stack is empty");

            stackSize --;
            Node<T> *toDelete = head;
            head = head->next;
            delete toDelete;
        }
        T top() {
            return (head == nullptr) ? 0 : head->data;
        }
        int size() const {
            return stackSize;
        }
    };
}

#endif //STACK_HPP
