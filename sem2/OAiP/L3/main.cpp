#include "Queue.hpp"
#include <iostream>

template<typename T>
void Solution(Queue<T> q) {
    Node<T>* ans = q.Solve();

    if (ans == nullptr) {
        std::cout << "There are no satisfactory elements" << std::endl;
        return;
    }
    Node<T>* temp = ans;
    std::cout << "Answer: ";
    while (temp != nullptr) {
        std::cout << temp->data << " ";
        temp = temp->next;
    }
    std::cout << std::endl;

    q.Print();
}

int main() {

    Queue<int> qu;

    int choose;
    do {
        std::cout << "----- Instruction -----" << std::endl;
        std::cout << "1 - Add element to end" << std::endl;
        std::cout << "2 - Add element to front" << std::endl;
        std::cout << "3 - Remove element from end" << std::endl;
        std::cout << "4 - Remove element from front" << std::endl;
        std::cout << "5 - Display queue" << std::endl;
        std::cout << "6 - Solve problem" << std::endl;
        std::cout << "0 - Exit" << std::endl;
        std::cout << "Choose an option: ";
        std::cin >> choose;

        switch (choose) {
            case 1: {
                std::cout << "Enter an element to add: ";
                int value;
                std::cin >> value;
                qu.push_back(value);
                break;
            }
            case 2: {
                std::cout << "Enter an element to front: ";
                int value;
                std::cin >> value;
                qu.push_front(value);
                break;
            }
            case 3:
                qu.pop_back();
                break;

            case 4:
                qu.pop_front();
                break;

            case 5:
                qu.Print();
                break;

            case 6:
                Solution(qu);
                break;

            case 7:
                qu.SolveT();
                break;

            default:
                break;
        }
    } while (choose != 0);

    return 0;
}