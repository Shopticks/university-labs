project(Tests)

add_executable(Tests
    PolynomialTest.cpp
    SegmentVectorTest.cpp
)

target_include_directories(Tests PRIVATE
        ${CMAKE_SOURCE_DIR}/Polynomial
        ${CMAKE_SOURCE_DIR}/SegmentVector
)

target_link_libraries(Tests
        Polynomial
        SegmentVector
)