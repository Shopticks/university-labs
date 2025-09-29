cmake_minimum_required(VERSION 4.0)

project(L1)

set(CMAKE_CXX_STANDARD 23)

add_subdirectory(Polynomial)
add_subdirectory(SegmentVector)

add_subdirectory(Tests)

add_executable(${PROJECT_NAME}
        main.cpp
)

target_link_libraries(${PROJECT_NAME}
    Polynomial
    SegmentVector
)

add_subdirectory(googletest)
enable_testing()
include(GoogleTest)
target_link_libraries(Tests GTest::gtest_main)