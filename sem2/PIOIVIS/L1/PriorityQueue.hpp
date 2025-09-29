#ifndef PRIORITYQUEUE_HPP
#define PRIORITYQUEUE_HPP

#include <vector>
#include <iostream>

/**
 * @brief A class containing functions for working with a priority queue
 *
 * @tparam T type of class
 */
template <typename T>
class PriorityQueue {
private:
    std::vector<T> heapArray;
    int size;
    int capacity;

    /**
     * @brief Function to prioritize heap
     *
     * @param i number of heap element
     */
    void heapify(int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < size && heapArray[left] > heapArray[largest])
            largest = left;

        if (right < size && heapArray[right] > heapArray[largest])
            largest = right;

        if (largest != i) {
            std::swap(heapArray[i], heapArray[largest]);
            heapify(largest);
        }
    }

    /**
     * @brief Function for sorting elements in a heap
     */
    void buildHeap() {
        for (int i = (size - 1) / 2; i >= 0; i--) {
            heapify(i);
        }
    }

    /**
     * @brief Function, that resize heap
     */
    void resizeHeap() {
        if (capacity == 0) capacity = 1;
        while (capacity <= size) {
            capacity <<= 1;
        }
        heapArray.resize(capacity);
    }
public:
    /**
     * @brief Constructor that initializes a class
     */
    explicit PriorityQueue() : size(0), capacity(0) {
        this->heapArray.resize(capacity);
    }

    /**
     * @brief Function to insert array to queue
     *
     * @param arr an array with data to insert
     */
    void insert(const std::vector<T>& arr) {
        int oldSize = size;
        size += arr.size();
        resizeHeap();
        for (int i = 0; i < arr.size(); ++i)
            heapArray[oldSize + i] = arr[i];
        buildHeap();
    }

    /**
     * @brief Function to insert data to queue
     *
     * @param value data to insert
     */
    void insert(T value) {
        if (capacity == 0) capacity = size;
        if (size >= capacity) {
            resizeHeap();
        }

        size++;
        int i = size - 1;
        heapArray[i] = value;

        while (i != 0 && heapArray[(i - 1) / 2] < heapArray[i]) {
            std::swap(heapArray[i], heapArray[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    }

    /**
     * @brief Function that return top element
     *
     * @return top (most priority) element
     */
    T top() {
        if (size <= 0)
            throw std::out_of_range("Empty priority queue");

        return heapArray[0];
    }

    /**
     * @brief Function that delete and return top element
     *
     * @return top (most priority) element
     */
    T pop() {
        if (size <= 0)
            throw std::out_of_range("PriorityQueue is empty");
        T root = heapArray[0];
        heapArray[0] = heapArray[size - 1];
        size--;
        heapify(0);
        return root;
    }

    /**
     * @brief Function "is queue empty?"
     *
     * @return 0 if queue has no element and 1 otherwise
     */
    bool empty() {
         return size == 0;
     }

};

#endif // PRIORITYQUEUE_HPP
