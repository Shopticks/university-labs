cmake_minimum_required(VERSION 3.30)
project(CourseProject)

set(CMAKE_CXX_STANDARD 26)

add_executable(CourseProject main.cpp
        Database.cpp
        Database.h
        Student.cpp
        Student.h
        FileManager.cpp
        FileManager.h
        Operations.cpp
        Operations.h
)
