#include <iostream>
#include <thread>
#include <cmath>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <fstream>
#include <chrono>

/**
 * @brief Point class for function
 * 
 * @param x Independent variable
 * @param y Function result
 * 
 * @details Stores the argument and the converted value of the function. 
 * Also contains time intervals
 */
class Point {
public:
    double x;
    double y;
    std::chrono::steady_clock::time_point compute_time;
    std::chrono::steady_clock::time_point write_time;

    Point(double x_val, double y_val)
        : x(x_val), y(y_val), compute_time(std::chrono::steady_clock::now()) {}

    Point(Point&& other) noexcept
        : x(other.x),
          y(other.y),
          compute_time(other.compute_time),
          write_time(other.write_time) {}

    void set_write_time() {
        write_time = std::chrono::steady_clock::now();
    }
};

template<typename T>
class SafeQueue {
private:
    mutable std::mutex mut;
    std::queue<T> data_queue;
    std::condition_variable data_cond;

public:
    void push(T item) {
        std::lock_guard<std::mutex> lk(mut);
        data_queue.push(std::move(item));
        data_cond.notify_one();
    }

    bool wait_and_pop(T& item, std::chrono::milliseconds timeout = std::chrono::milliseconds(100)) {
        std::unique_lock<std::mutex> lk(mut);
        bool ready = data_cond.wait_for(lk, timeout, [this] { return !data_queue.empty(); });
        if (ready) {
            item = std::move(data_queue.front());
            data_queue.pop();
            return true;
        }
        return false;
    }

    bool try_pop(T& item) {
        std::lock_guard<std::mutex> lk(mut);
        if (data_queue.empty()) {
            return false;
        }
        item = std::move(data_queue.front());
        data_queue.pop();
        return true;
    }

    bool empty() const {
        std::lock_guard<std::mutex> lk(mut);
        return data_queue.empty();
    }
};

