#include <iostream>
#include "Stack.hpp"

template<typename T>
void Solution(Stack<T> st) {
    std::cout << "New ";
    st.Solve();
}

int main() {
    Stack<int> st;

    int choise;
    do {
        std::cout << '\n';
        std::cout << "0 - Выход из программы\n";
        std::cout << "1 - Вставка элемента в массив\n";
        std::cout << "2 - Получение последнего элемента\n";
        std::cout << "3 - Удаление последнего элемента\n";
        std::cout << "4 - Решение задачи\n";
        std::cout << "5 - Отобразить стек\n";
        std::cout << "6 - Удалить стек\n";
        std::cout << "Инструкция: ";
        std::cin >> choise;

        switch (choise) {
            case 0:
                break;
            case 1: {
                std::cout << "Введите элемент: ";
                int value;
                std::cin >> value;
                st.push(value);
                break;
            }
            case 2:
                std::cout << "Top element: " << st.top() << std::endl;
                break;
            case 3:
                std::cout << "Popped element: " << st.top() << std::endl;
                st.pop();
                break;
            case 4:
                Solution(st);
                break;
            case 5:
                st.DisplayStack();
                break;
            case 6:
                st.DeleteStack();
                break;

            default:
                throw "Unknown choice.";
        }

    }while (choise != 0);

}