cmake_minimum_required(VERSION 3.30)
project(L2)

set(CMAKE_CXX_STANDARD 26)

add_executable(L2 main.cpp
        Node.hpp
        Set.cpp
        Set.hpp)
