#ifndef FILEMANAGER_H
#define FILEMANAGER_H

#include "Student.h"
#include <iostream>
namespace FileManager {

    void ResizeArray(Student **&students, size_t size);
    // Read students and write it to array
    bool readStudentsFromFile(const char* filename, Student**& students, size_t& size);
    // Write students to file
    bool writeStudentsToFile(const char* filename, Student** students, size_t size);
    // Clear file from path
    void clearFile(const char* filename);

    bool writeIncreasedScholarshipStatisticsToFile(const char* filename, Student** students, size_t size);
    bool writeScholarshipStatisticsToFile(const char* filename, Student** students,
        size_t size, char* faculty, double minS, double maxS);

    size_t getNumberOfStudentsInFile(const char* filename);
}


#endif // FILEMANAGER_H
