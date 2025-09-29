cmake_minimum_required(VERSION 3.30)
project(L3)

set(CMAKE_CXX_STANDARD 26)

add_executable(L3 main.cpp
        Queue.hpp
        Node.hpp)
