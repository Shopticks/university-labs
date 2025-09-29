#include <iostream>
#include <string>
#include <unistd.h>
#include <sys/types.h>
#include <vector>
#include <sstream>
#include <cstdlib>

int main() {
    std::cout << "Process " << getpid() << " with parent " << getppid() << " starts." << std::endl;

    // Get number of processes
    std::cout << "Enter number of processes: ";
    int N;
    std::cin >> N;
    if(N == 0) return 0;
    if(N < 0)
        throw std::invalid_argument("The argument of execution process out of range.");

    // Get parent processes number
    std::cout << "Enter parents for next " << N << " processes: ";
    std::vector<int> parent(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> parent[i];
    }
    for (int i = 0; i < N; ++i) {
        if (parent[i] < 0 || parent[i] > N)
            std::cerr << "Value need to be >= 0. Reenter value for " << i << " process: ";
            std::cin >> parent[i--];
    }

    // Get execution process number
    std::cout << "Enter number of execution process (1 - " << N << "): ";
    int execNumber;
    std::cin >> execNumber;
    while (execNumber <= 0 || execNumber > N){
        std::cerr << "Value need to be from 1 to " << N << ". Reenter value: ";
        std::cin >> execNumber;
    }
    execNumber -= 1;

    if(execNumber >= N || execNumber < 1)
        throw std::invalid_argument("The argument of execution process out of range.");

    // Get execution command
    std::cout   << "Enter the command to be executed by the "
                << execNumber << " process: ";
    std::cin.ignore();

    std::string line;
    while (line.empty()) {
        std::getline(std::cin, line);
    }

    // Translate these command to arguments
    std::istringstream iss(line);
    std::vector<std::string> args;
    std::string arg;
    while (iss >> arg) {
        args.push_back(arg);
    }

    // Change type for execution params type (string to char*)
    std::vector<char*> c_args;
    for (auto& s : args) {
        c_args.push_back(&s[0]);
    }
    c_args.push_back(nullptr);

    // The root process is 1 (1-indexed)
    int myNumber = 1;

    // For every child process
    for (int childNum = 1; childNum <= static_cast<int>(N); ++childNum) {
        // If the process is a parent of the child's process
        if (parent[childNum] == myNumber) {
            pid_t pid = fork();
            if (pid < 0) {
                std::cerr << "fork failed\n";
                exit(1);
            }
            if (pid == 0) {
                // Child process
                myNumber = childNum + 1;

                // If process number need to complete exec
                if (myNumber == execNumber) {
                    std::cout << "Process " << getpid() << " (parent " << getppid() << ") is executing: " << args[0] << std::endl;
                    execvp(c_args[0], c_args.data());
                    std::cerr << "exec failed\n";
                    _exit(1);
                }
                continue;
            } else {
                // Parent process
                std::cout << "Process " << getpid() << " has forked child process " << pid << std::endl;
            }
        }
    }

    std::cout << "Process " << getpid() << " with parent " << getppid() << " completes his work." << std::endl;

    sleep(10); // To check to see all processes in some activity monitor

    return 0;
}