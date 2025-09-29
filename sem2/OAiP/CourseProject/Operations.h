#ifndef OPERATIONS_H
#define OPERATIONS_H

#include "Student.h"
#include <iostream>

namespace Search {
    void LinearSearchByName(Student** inputStudents, size_t inputSize,
        Student**& outputStudents, size_t& outputSize, const char* name);

    void BinarySearchByGrade(Student** inputStudents, size_t inputSize,
        Student**& outputStudents, size_t& outputSize, double grade);

}

namespace Sorting {
    void QuickSortByScholarship(Student**& students, long long low, long long high);
    size_t QuickSortPartition(Student**& students, long long low, long long high);

    void QuickSortByScholarshipReverse(Student**& students, long long low, long long high);
    size_t QuickSortPartitionReverse(Student**& students, long long low, long long high);

    void SelectionSortByGrade(Student**& students, size_t size);
    void SelectionSortByGradeReverse(Student**& students, size_t size);

    void InsertionSortByName(Student**& students, size_t size);
}

namespace AdditionalFunctions {
    void findFaculties(Student** inputStudents, size_t inputSize, char**& faculties, size_t& facultiesSize);
    bool isDigit(char* c);
    void deleteStudentsArray(Student** inputStudents, size_t inputSize);
    bool compareChars(const char* a, const char* b);
}

#endif // OPERATIONS_H