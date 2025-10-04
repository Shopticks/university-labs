#include "main.h"

std::atomic<bool> done_computing{false}; // Indicator of the end of the first thread
std::atomic<bool> done_writing{false};   // Indicator of the end of the second thread

/**
 * @details The function by which the calculations will be carried out
 */
double F(double value)
{
    return std::sin(value);
}

/**
 * @brief Compute thread
 * @details A computational thread that stores calculation information in the queue
 */
void compute_thread(SafeQueue<std::shared_ptr<Point>> &compute_queue, int n_points, double step)
{
    for (int i = 0; i < n_points; ++i)
    {
        double x = i * step;
        double y = F(x);
        auto point = std::make_shared<Point>(x, y); // Add results for other threads
        compute_queue.push(point);                  // Safe pushing

        // !!DEBUG ONLY!!
        // std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

/**
 * @brief Write computing results thread
 * @details A thread that writes results to the specified file
 */
void write_thread(SafeQueue<std::shared_ptr<Point>> &in_queue,
                  SafeQueue<std::shared_ptr<Point>> &out_queue,
                  const std::string &output_file)
{

    // Create and initialize stream for an output file
    std::ofstream file(output_file);

    if (!file.is_open())
    {
        std::cerr << "Cannot open output file\n";
        return;
    }

    while (true)
    {
        std::shared_ptr<Point> p;
        if (in_queue.wait_and_pop(p))
        { // Try to pop front element
            // Write it to file
            file << p->x << " " << p->y << "\n";
            file.flush();

            // Update write time
            p->set_write_time();

            // Push for log thread
            out_queue.push(p);
        }
        else if (done_computing && in_queue.empty())
        {
            break;
        }
    }
}

/**
 * @brief Log computed and writed time
 * @details A thread that writes logs to the specified file
 */
void log_thread(SafeQueue<std::shared_ptr<Point>> &in_queue, const std::string &log_file)
{
    // Create and initialize stream for a log file
    std::ofstream log(log_file);
    if (!log.is_open())
    {
        std::cerr << "Cannot open log file\n";
        return;
    }

    while (true)
    {
        std::shared_ptr<Point> p;
        if (in_queue.wait_and_pop(p))
        { // Try to pop front element

            // Conversion of time into a presentable view
            auto compute_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                                  p->compute_time.time_since_epoch())
                                  .count();
            auto write_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                                p->write_time.time_since_epoch())
                                .count();
            auto required_time = std::chrono::duration_cast<std::chrono::milliseconds>(
                                     p->write_time.time_since_epoch() - p->compute_time.time_since_epoch())
                                     .count();

            // Write time info into file
            log << "Computed at: " << compute_ms
                << " ms, Written at: " << write_ms << " ms. "
                << "Time required: " << required_time << " ms\n";
            log.flush();
        }
        else if (done_writing && in_queue.empty())
        {
            break;
        }
    }
}

int main()
{
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
    std::cout << "Execution time: " << seconds << " ms" << std::endl;

    return 0;
}