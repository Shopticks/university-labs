/**
 * @details Work option №5
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unistd.h>  // fork, execvp
#include <sys/wait.h> // waitpid
#include <cstring>   // strerror

int main() {
    while (true) {
        std::cout << "mysh> ";
        std::string line;
        if (!std::getline(std::cin, line) || line == "exit") break; // EOF or input error

        std::istringstream iss(line);
        std::vector<std::string> args;
        std::string arg;

        
        while (iss >> arg) {
            args.push_back(arg);
        }

        if (args.empty()) continue; // Empty command

        // Conversion of an string array to char*
        std::vector<char*> c_args;
        for (auto& s : args) {
            c_args.push_back(&s[0]);
        }
        c_args.push_back(nullptr);

        pid_t pid = fork();
        if (pid < 0) {
            std::cerr << "fork failed: " << strerror(errno) << "\n";
            continue;
        }
        if (pid == 0) {
            // Child process
            execvp(c_args[0], c_args.data());
            // Error occured if execvp returned
            std::cerr << "exec failed: " << strerror(errno) << "\n";
            _exit(1);
        } else {
            // Parent process waiting
            int status;
            if (waitpid(pid, &status, 0) == -1) {
                std::cerr << "waitpid failed: " << strerror(errno) << "\n";
            }
        }
    }
    return 0;
}
