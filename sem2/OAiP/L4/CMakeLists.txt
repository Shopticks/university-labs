cmake_minimum_required(VERSION 3.30)
project(L4)

set(CMAKE_CXX_STANDARD 26)

add_executable(L4 main.cpp
                Node.hpp
                Stack.hpp
        RPN.cpp
        RPN.hpp)
