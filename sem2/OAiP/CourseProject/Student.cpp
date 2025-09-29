#include "Student.h"
#include <cstring>
#include <iostream>
#include <ostream>

#define GREEN_COLOR "\033[32m"
#define RESET_COLOR "\x1B[0m"

// Constructor
Student::Student(char *fullName, char *faculty, double averageGrade, bool hasPrivileges, double scholarshipAmount) {
    // Allocate memory for fullName and copy the content

    this->faculty = nullptr;
    if (fullName != nullptr) {
        this->fullName = new char[strlen(fullName) + 1];
        strcpy(this->fullName, fullName);
    }

    // Allocate memory for faculty and copy the content
    if (faculty != nullptr) {
        this->faculty = new char[strlen(faculty) + 1];
        strcpy(this->faculty, faculty);
    }

    // Initialize other fields
    this->averageGrade = averageGrade;
    this->hasPrivileges = hasPrivileges;
    this->scholarshipAmount = scholarshipAmount;
}

// Destructor
Student::~Student() {
    // Free dynamically allocated memory
    delete[] fullName;
    delete[] faculty;
}

#pragma region Setters

void Student::setFullName(char *fullName) {
    // Free existing memory before allocating new memory
    delete[] this->fullName;
    this->fullName = new char[strlen(fullName) + 1];
    strcpy(this->fullName, fullName);
}

void Student::setFaculty(char *faculty) {
    // Free existing memory before allocating new memory
    delete[] this->faculty;
    this->faculty = new char[strlen(faculty) + 1];
    strcpy(this->faculty, faculty);
}

void Student::setAverageGrade(double grade) {
    this->averageGrade = grade;
}

void Student::setHasPrivileges(bool hasPrivileges) {
    this->hasPrivileges = hasPrivileges;
}

void Student::setScholarshipAmount(double scholarshipAmount) {
    this->scholarshipAmount = scholarshipAmount;
}

#pragma endregion

#pragma region Getters

char* Student::getFullName() {
    return fullName;
}

char* Student::getFaculty() {
    return faculty;
}

double Student::getAverageGrade() {
    return averageGrade;
}

bool Student::getHasPrivileges() {
    return hasPrivileges;
}

double Student::getScholarshipAmount() {
    return scholarshipAmount;
}

#pragma endregion

void Student::print() {
    std::cout << RESET_COLOR << "Full Name: " << GREEN_COLOR << this->fullName << std::endl;
    std::cout << RESET_COLOR << "Faculty: " << GREEN_COLOR << this->faculty << std::endl;
    std::cout << RESET_COLOR << "Average Grade: " << GREEN_COLOR << this->averageGrade << std::endl;
    std::cout << RESET_COLOR << "Has Privileges: " << GREEN_COLOR << this->hasPrivileges << std::endl;
    std::cout << RESET_COLOR << "Scholar Amount: " <<  GREEN_COLOR << this->scholarshipAmount << std::endl;
    std::cout << RESET_COLOR;
}

void Student::print(std::ofstream &file) {
    file << "Full Name: " << this->fullName << std::endl;
    file << "Faculty: " << this->faculty << std::endl;
    file << "Average Grade: " << this->averageGrade << std::endl;
    file << "Has Privileges: " << this->hasPrivileges << std::endl;
    file << "Scholar Amount: " << this->scholarshipAmount << std::endl;
}

Student::Student(const Student& other) {
    fullName = new char[strlen(other.fullName) + 1];
    strcpy(fullName, other.fullName);
    faculty = new char[strlen(other.faculty) + 1];
    strcpy(faculty, other.faculty);
    averageGrade = other.averageGrade;
    hasPrivileges = other.hasPrivileges;
    scholarshipAmount = other.scholarshipAmount;
}

Student& Student::operator=(const Student& other) {
    if (this != &other) {
        delete[] fullName;
        delete[] faculty;
        fullName = new char[strlen(other.fullName) + 1];
        strcpy(fullName, other.fullName);
        faculty = new char[strlen(other.faculty) + 1];
        strcpy(faculty, other.faculty);
        averageGrade = other.averageGrade;
        hasPrivileges = other.hasPrivileges;
        scholarshipAmount = other.scholarshipAmount;
    }
    return *this;
}