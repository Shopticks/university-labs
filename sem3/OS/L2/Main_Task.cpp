#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <ctime>
#include <iomanip>
#include <chrono>

void print_process_info() {
    pid_t pid = getpid();
    pid_t ppid = getppid();

    auto now = std::chrono::system_clock::now();
    std::time_t now_c = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

    std::tm local_time = *localtime(&now_c);

    std::cout << "PID: " << pid << ", Parent PID: " << ppid << ", Time: "
              << std::setw(2) << std::setfill('0') << local_time.tm_hour << ":"
              << std::setw(2) << std::setfill('0') << local_time.tm_min << ":"
              << std::setw(2) << std::setfill('0') << local_time.tm_sec << ":"
              << std::setw(3) << std::setfill('0') << ms.count()
              << std::endl;
}

int main() {
    pid_t pid1 = fork();

    if (pid1 == -1) {
        std::cerr << "Fork failed\n";
        return 1;
    }

    if (pid1 == 0) {
        // First child process
        print_process_info();
        _exit(0);
    } else {
        pid_t pid2 = fork();

        if (pid2 == -1) {
            std::cerr << "Fork failed\n";
            return 1;
        }

        if (pid2 == 0) {
            // Second child process
            print_process_info();
            _exit(0);
        } else {
            // Parent process
            print_process_info();

            system("ps -x");

            // Wait for end child processes
            waitpid(pid1, nullptr, 0);
            waitpid(pid2, nullptr, 0);
        }
    }

    return 0;
}
