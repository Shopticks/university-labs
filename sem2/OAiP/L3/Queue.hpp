#ifndef QUEUE_HPP
#define QUEUE_HPP

#include "Node.hpp"
#include <iostream>

template<class T>
class Queue {
private:
    Node<T>* head = nullptr;
    Node<T>* lastElement = nullptr;

public:
    Queue(){}

    bool empty() {
        return head == nullptr;
    }

    void push_back(T value) {
        Node<T> *newNode = new Node<T>(value);

        if (head == nullptr) {
            head = newNode;
            lastElement = newNode;
        }
        else {
            newNode->prev = lastElement;
            lastElement->next = newNode;
            lastElement = newNode;
        }
    }
    void push_front(T value) {
        Node<T> *newNode = new Node<T>(value);

        if (head == nullptr) {
            head = newNode;
            lastElement = newNode;
        }
        else {
            newNode->next = head;
            head->prev = newNode;
            head = newNode;
        }
    }

    void pop_back(){
        if (head == nullptr)
            throw std::out_of_range("Queue is empty");

        Node<T> *temp = head;
        while (temp->next != lastElement) temp = temp->next;
        delete lastElement;
        lastElement = temp;
        lastElement->next = nullptr;
    }
    void pop_front() {
        if (head == nullptr)
            throw std::out_of_range("Queue is empty");

        Node<T> *toDelete = head;
        head = head->next;
        delete toDelete;
    }

    T front() {
        return (head == nullptr) ? 0 : head->data;
    }
    T back() {
        return (head == nullptr) ? 0 : lastElement->data;
    }

    Node<T>* Solve() {
        if (head == nullptr)
            throw std::out_of_range("Queue is empty");

        T min = head->data;
        Node<T> *temp = head->next;
        while (temp != nullptr) {
            if (temp->data < min)
                min = temp->data;

            temp = temp->next;
        }

        if (head->data == min)
            return nullptr;

        Node<T> *ans = nullptr;
        temp = head->next;
        while (temp->data != min) {
            if (ans == nullptr) {
                ans = temp;
            }
            temp = temp->next;
        }
        if (temp->prev != head) {
            head->next = temp;
            temp->prev->next = nullptr;
            temp->prev = head;
            ans->prev = nullptr;
        }

        return ans;
    }

    void SolveT() {
        if (head == nullptr)
            throw std::out_of_range("Queue is empty");

        int i = 1;
        Node<T> *temp = head;
        while (temp != nullptr) {
            bool isDelete = (temp->data % 2 == i % 2);
            if (isDelete) {
                if (temp->prev == nullptr)
                    head = temp->next,
                    temp->next->prev = nullptr;
                else
                    temp->prev->next = temp->next;
                Node<T>* toDelete = temp;
                temp = temp->next;
                delete toDelete;
            }
            else
                temp = temp->next;
            i++;
        }

        if (head == nullptr)
            throw std::out_of_range("Queue is NOW empty");

        double average = 0;
        i = 0;

        temp = head;
        while (temp != nullptr) {
            average += temp->data;
            temp = temp->next;
            i++;
        }

        std::cout << (average / i) << std::endl;
        Print();
    }

    void Print() {
        Node<T> *temp = head;
        std::cout << "Queue: ";
        while (temp != nullptr) {
            std::cout << temp->data << " ";
            temp = temp->next;
        }
        std::cout << std::endl;
    }
};

#endif //QUEUE_HPP
