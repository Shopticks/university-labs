#ifndef DATABASE_H
#define DATABASE_H

#include <iostream>
#include <fstream>
#include "Student.h"

namespace Database {

    void displayAll(const char* filename);
    bool addStudent(const char* filename, Student* student);
    bool changeStudentInfo(const char* filename, Student* student, int studentNumber);
    bool deleteStudent(const char* filename, int studentNumber);
    size_t getNumOfStudents(const char* filename);

    void linearSearchByName(const char* filename, const char* name);
    void binarySearchByGrade(const char* filename, double grade);

    void quickSortByScholarship(const char* filename);
    void selectionSortByGrade(const char* filename);
    void insertionSortByName(const char* filename);

    void identifyIncreasedScholarship(const char* storageFilename, const char* resultFilename,
        double minGrade, bool needPrivileges);

    void scholarshipStatistics(const char* storageFilename, const char* resultFilename);
}

#endif
