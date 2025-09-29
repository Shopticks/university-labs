#include "FileManager.h"
#include <fstream>
#include <cstring>
#include <iostream>

void FileManager::ResizeArray(Student**& students, size_t size) {
    if (size == 0) return;
    size_t capacity = 1;
    while (capacity <= size) capacity <<= 1;

    Student** newStudents = new Student*[capacity];
    if (students)
        for (size_t i = 0; i < size; i++) {
            newStudents[i] = students[i];
        }

    // if (students)
    //     delete[] students; // Delete the old array, not individual elements yet

    students = newStudents;
}

bool FileManager::readStudentsFromFile(const char *filename, Student **&students, size_t &size) {
    std::ifstream file (filename, std::ifstream::in);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << std::endl;
        return false;
    }

    // Read array size
    file.read(reinterpret_cast<char*>(&size), sizeof(size_t));

    if (size == 0)
        return students = nullptr, false;
    ResizeArray(students, size);
    //students = new Student*[size];

    for (size_t i = 0; i < size; i++) {
        // Read size of fName
        size_t fullNameLength;
        file.read(reinterpret_cast<char*>(&fullNameLength), sizeof(fullNameLength));
        char* fullName = new char[fullNameLength];
        file.read(fullName, fullNameLength);

        // Read size if faculty
        size_t facultyLength;
        file.read(reinterpret_cast<char*>(&facultyLength), sizeof(facultyLength));
        char* faculty = new char[facultyLength];
        file.read(faculty, facultyLength);

        // Read average grade
        double averageGrade;
        file.read(reinterpret_cast<char*>(&averageGrade), sizeof(averageGrade));

        // Read privileges
        bool hasPrivileges;
        file.read(reinterpret_cast<char*>(&hasPrivileges), sizeof(hasPrivileges));

        // Read scholarship amount
        double scholarshipAmount;
        file.read(reinterpret_cast<char*>(&scholarshipAmount), sizeof(scholarshipAmount));

        // Add info to array
        students[i] = new Student(fullName, faculty, averageGrade, hasPrivileges, scholarshipAmount);
    }

    return true;
}

bool FileManager::writeStudentsToFile(const char *filename, Student **students, size_t size) {
    std::ofstream file (filename, std::ofstream::out);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << std::endl;
        return false;
    }

    file.write(reinterpret_cast<char*>(&size), sizeof(size_t));
    for (size_t i = 0; i < size; i++) {
        size_t fullNameLength = strlen(students[i]->getFullName());
        file.write(reinterpret_cast<char*>(&fullNameLength), sizeof(fullNameLength));
        file.write(students[i]->getFullName(), fullNameLength);

        size_t facultyLength = strlen(students[i]->getFaculty());
        file.write(reinterpret_cast<char*>(&facultyLength), sizeof(facultyLength));
        file.write(students[i]->getFaculty(), facultyLength);

        double averageGrade = students[i]->getAverageGrade();
        file.write(reinterpret_cast<char*>(&averageGrade), sizeof(averageGrade));

        bool hasPrivileges = students[i]->getHasPrivileges();
        file.write(reinterpret_cast<char*>(&hasPrivileges), sizeof(hasPrivileges));

        double scholarshipAmount = students[i]->getScholarshipAmount();
        file.write(reinterpret_cast<char*>(&scholarshipAmount), sizeof(scholarshipAmount));
    }

    return true;
}

void FileManager::clearFile(const char *filename) {
    std::ofstream file(filename);
    file.close();
}

bool FileManager::writeIncreasedScholarshipStatisticsToFile(const char *filename, Student **students, size_t size) {
    std::ofstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << std::endl;
        return false;
    }

    file << size << " students:" << std::endl;
    for (int i = 0; i < size; i++) {
        file << "-----------------------" << std::endl;
        students[i]->print(file);
    }

    file.close();
    return true;
}

bool FileManager::writeScholarshipStatisticsToFile(const char *filename, Student **students,
    size_t size, char *faculty, double minS, double maxS) {

    std::ofstream file(filename, std::ofstream::app);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << std::endl;
        return false;
    }

    file << std::endl;
    file << "----- " << faculty << " -----" << std::endl;
    file << "Min scholarship: " << minS << std::endl;
    file << "Max scholarship: " << maxS << std::endl;
    for (int i = 0; i < size; i++) {
        file << "-----------------------" << std::endl;
        students[i]->print(file);
    }

    file.close();
    return true;
}

size_t FileManager::getNumberOfStudentsInFile(const char *filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Could not open file " << filename << std::endl;
        return 0;
    }
    size_t numberOfStudents;
    file.read(reinterpret_cast<char*>(&numberOfStudents), sizeof(numberOfStudents));
    return numberOfStudents;
}
