#ifndef STACK_HPP
#define STACK_HPP

#include "Node.hpp"
#include <iostream>

template<class T>
class Stack {
private:
    Node<T>* head = nullptr;
    void PushToEnd(Node<T>* node) {
        if (head == nullptr) {
            head = node;
            node->next = nullptr;
            return;
        }

        Node<T>* temp = head;
        while (temp->next != nullptr) temp = temp->next;

        temp->next = node;
        node->next = nullptr;
    }

public:
    Stack(){}

    bool empty() {
        return head == nullptr;
    }
    void push(T value) {
        Node<T> *newNode = new Node<T>(value);

        newNode->next = head;
        head = newNode;
    }
    void pop(){
        if (head == nullptr)
            throw std::out_of_range("Stack is empty");

        Node<T> *toDelete = head;
        head = head->next;
        delete toDelete;
    }
    T top() {
        return (head == nullptr) ? 0 : head->data;
    }

    void Solve() {

        size_t size = 0;
        double average = 0;
        Node<T>* temp = head;
        while (temp != nullptr) {
            size++;
            average += temp->data;
            temp = temp->next;
        }

        average /= (size * 1.0);
        std::cout << "Average is " << average << std::endl;

        int nearest = head->data;
        Node<T> *toSwap = head, *preSwap;
        temp = head->next;

        while (temp->next != nullptr) {
            if (abs(average - nearest) > abs(average - temp->data)) {
                toSwap = temp;
                nearest = temp->data;
            }
            temp = temp->next;
        }

        std::swap(temp->data, toSwap->data);

        DisplayStack();
    }

    void DisplayStack() {
        if (head == nullptr) {
            std::cout << "Stack is empty\n";
            return;
        }
        std::cout << "stack: ";
        Node<T> *current = head;
        while (current != nullptr) {
            std::cout << current->data << ' ';
            current = current->next;
        }
        std::cout << '\n';
    }

    void DeleteStack() {
        while (head != nullptr) {
            Node<T> *temp = head;
            head = head->next;
            delete temp;
        }
    }
};

#endif //STACK_HPP
