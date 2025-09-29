#include <iostream>
#include <thread>
#include <cmath>
#include <functional>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <fstream>
#include <chrono>

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

double F(double value) {
    return std::sin(value);
}

std::atomic<bool> done_computing{false};
std::atomic<bool> done_writing{false};

void write_thread(SafeQueue<std::shared_ptr<Point>>& in_queue,
                  SafeQueue<std::shared_ptr<Point>>& out_queue,
                  const std::string& output_file) {

    std::ofstream file(output_file);

    if (!file.is_open()) {
        std::cerr << "Cannot open output file\n";
        return;
    }

    while (true) {
        std::shared_ptr<Point> p;
        if (in_queue.wait_and_pop(p)) {
            file << p->x << " " << p->y << "\n";
            file.flush();
            p->set_write_time();
            out_queue.push(p);
        } else if (done_computing && in_queue.empty()) {
            break;
        }
    }
}

void log_thread(SafeQueue<std::shared_ptr<Point>>& in_queue, const std::string& log_file) {
    std::ofstream log(log_file);
    if (!log.is_open()) {
        std::cerr << "Cannot open log file\n";
        return;
    }

    while (true) {
        std::shared_ptr<Point> p;
        if (in_queue.wait_and_pop(p)) {
            auto compute_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                p->compute_time.time_since_epoch()).count();
            auto write_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                p->write_time.time_since_epoch()).count();

            log << "Computed at: " << compute_ms << " ms, Written at: " << write_ms << " ms\n";
            log.flush();
        } else if (done_writing && in_queue.empty()) {
            break;
        }
    }
}

void compute_thread(SafeQueue<std::shared_ptr<Point>>& compute_queue, int n_points, double step) {
    for (int i = 0; i < n_points; ++i) {
        double x = i * step;
        double y = F(x);
        auto point = std::make_shared<Point>(x, y);
        compute_queue.push(point);

        // !DEBUG_ONLY
        // std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

int main() {
    auto start = std::chrono::system_clock::now();

    const int N_POINTS = 1'000'000;
    const double STEP = 0.1;
    const std::string OUTPUT_FILE = "output.txt";
    const std::string LOG_FILE = "log.txt";

    SafeQueue<std::shared_ptr<Point>> compute_to_write;
    SafeQueue<std::shared_ptr<Point>> write_to_log;

    std::thread t1(compute_thread, std::ref(compute_to_write), N_POINTS, STEP);
    std::thread t2(write_thread, std::ref(compute_to_write), std::ref(write_to_log), OUTPUT_FILE);
    std::thread t3(log_thread, std::ref(write_to_log), LOG_FILE);

    t1.join();
    done_computing = true;

    t2.join();
    done_writing = true;

    t3.join();

    std::cout << "Done. Check " << OUTPUT_FILE << " and " << LOG_FILE << std::endl;

    auto end = std::chrono::system_clock::now();
    auto seconds = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    std::cout << "Execution time: " << seconds << " milliseconds\n";    

    return 0;
}