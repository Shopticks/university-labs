#include "Database.h"
#include "FileManager.h"
#include "Operations.h"
#define BLUE_COLOR "\033[34m"
#define RESET_COLOR "\033[0m"

void Database::displayAll(const char *filename) {
    size_t size = 0;
    Student **students = nullptr;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "File is empty: " << filename << std::endl;
        return;
    }

    for (size_t i = 0; i < size; i++) {
        std::cout << BLUE_COLOR << i + 1 << RESET_COLOR << ". ";
        students[i]->print();
        delete students[i];
    }

    delete[] students;
}

bool Database::addStudent(const char *filename, Student *student) {
    Student **students = nullptr;
    size_t size = 0;

    FileManager::readStudentsFromFile(filename, students, size);

    FileManager::ResizeArray(students, size + 1);
    students[size] = student;

    FileManager::writeStudentsToFile(filename, students, size + 1);

    AdditionalFunctions::deleteStudentsArray(students, size + 1);

    return true;
}

bool Database::changeStudentInfo(const char* filename, Student* student, int studentNumber) {
    Student** students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "File error: " << filename << std::endl;
        return false;
    }

    if (size == 0) {
        std::cerr << "File is empty: " << filename << std::endl;
        return false;
    }

    studentNumber--;

    if (studentNumber >= size) {
        std::cerr << "Student number out of range.\n";
        AdditionalFunctions::deleteStudentsArray(students, size);
        return false;
    }

    delete students[studentNumber];
    students[studentNumber] = student;

    bool success = FileManager::writeStudentsToFile(filename, students, size);
    AdditionalFunctions::deleteStudentsArray(students, size);

    return success;
}

bool Database::deleteStudent(const char* filename, int studentNumber) {
    Student** students = nullptr;
    size_t size = 0;

    // Step 1: Read all students from the file
    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "Error opening file: " << filename << "\n";
        return false;
    }

    if (size == 0) {
        std::cerr << "File is empty: " << filename << "\n";
        AdditionalFunctions::deleteStudentsArray(students, size);
        return false;
    }


    studentNumber--;


    if (studentNumber < 0 || static_cast<size_t>(studentNumber) >= size) {
        std::cerr << "Invalid student number.\n";
        AdditionalFunctions::deleteStudentsArray(students, size);
        return false;
    }

    Student* toDelete = students[studentNumber];

    Student** newStudents = new Student*[size - 1];
    size_t j = 0;
    for (size_t i = 0; i < size; ++i) {
        if (i != static_cast<size_t>(studentNumber)) {
            newStudents[j++] = students[i];
        }
    }

    bool success = FileManager::writeStudentsToFile(filename, newStudents, size - 1);

    AdditionalFunctions::deleteStudentsArray(students, size);

    delete[] newStudents;
    return success;
}

size_t Database::getNumOfStudents(const char *filename) {
    size_t size = FileManager::getNumberOfStudentsInFile(filename);
    if (size == 0) {
        std::cerr << "Find 0 students. Database is empty" << std::endl;
        return 0;
    }
    return size;
}

void Database::linearSearchByName(const char *filename, const char *name) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "Find 0 students. Database is empty" << std::endl;
        return;
    }

    Student **outputStudents = nullptr;
    size_t outputSize = 0;

    Search::LinearSearchByName(students, size, outputStudents, outputSize, name);

    if (outputSize == 0) {
        std::cerr << "No students found" << std::endl;
        return;
    }

    std::cout << outputSize << " students found:" << std::endl;
    for (size_t i = 0; i < outputSize; i++) {
        std::cout << "-----------------------" << std::endl;
        outputStudents[i]->print();
    }

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::binarySearchByGrade(const char *filename, double grade) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "Find 0 students. Database is empty" << std::endl;
        return;
    }
    Sorting::SelectionSortByGrade(students, size);

    Student **outputStudents = new Student*[size];
    size_t outputSize = 0;

    Search::BinarySearchByGrade(students, size, outputStudents, outputSize, grade);

    if (outputSize == 0) {
        std::cerr << "No students found" << std::endl;
        return;
    }

    std::cout << outputSize << " students found:" << std::endl;
    for (size_t i = 0; i < outputSize; i++) {
        std::cout << "----------------------" << std::endl;
        outputStudents[i]->print();
    }

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::quickSortByScholarship(const char *filename) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "File is empty: " << filename << std::endl;
        return;
    }

    Sorting::QuickSortByScholarship(students, 0, size - 1);

    FileManager::writeStudentsToFile(filename, students, size);

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::selectionSortByGrade(const char *filename) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "File is empty: " << filename << std::endl;
        return;
    }

    Sorting::SelectionSortByGrade(students, size);

    FileManager::writeStudentsToFile(filename, students, size);

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::insertionSortByName(const char *filename) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(filename, students, size)) {
        std::cerr << "File is empty: " << filename << std::endl;
        return;
    }

    Sorting::InsertionSortByName(students, size);

    FileManager::writeStudentsToFile(filename, students, size);

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::identifyIncreasedScholarship(const char *storageFilename, const char *resultFilename,
    double minGrade, bool needPrivileges) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(storageFilename, students, size)) {
        std::cerr << "File is empty: " << storageFilename << std::endl;
        return;
    }

    Student **outputStudents = new Student*[size];
    size_t outputSize = 0;
    for (size_t i = 0; i < size; i++) {
        if (students[i]->getAverageGrade() >= minGrade)
            if (!needPrivileges || (needPrivileges && needPrivileges == students[i]->getHasPrivileges()))
                outputStudents[outputSize++] = students[i];
    }

    if (outputSize == 0) {
        std::cerr << "No students found" << std::endl;
        return;
    }

    Sorting::SelectionSortByGradeReverse(outputStudents, outputSize);

    FileManager::writeIncreasedScholarshipStatisticsToFile(resultFilename, outputStudents, outputSize);

    AdditionalFunctions::deleteStudentsArray(students, size);
}

void Database::scholarshipStatistics(const char *storageFilename, const char *resultFilename) {
    Student **students = nullptr;
    size_t size = 0;

    if (!FileManager::readStudentsFromFile(storageFilename, students, size)) {
        std::cerr << "File is empty: " << storageFilename << std::endl;
        return;
    }
    FileManager::clearFile(resultFilename);

    char** faculties;
    size_t facultiesSize = 0;
    AdditionalFunctions::findFaculties(students, size, faculties, facultiesSize);

    for (size_t i = 0; i < facultiesSize; i++) {
        Student** outputStudents = new Student*[size];
        size_t outputSize = 0;

        double minScholarship = INT_MAX;
        double maxScholarship = INT_MIN;
        for (size_t j = 0; j < size; j++) {
            if (strcmp(students[j]->getFaculty(), faculties[i]) == 0) {
                outputStudents[outputSize++] = students[j];

                minScholarship = (minScholarship > students[j]->getScholarshipAmount() ?
                    students[j]->getScholarshipAmount() : minScholarship);
                maxScholarship = (maxScholarship < students[j]->getScholarshipAmount() ?
                     students[j]->getScholarshipAmount() : maxScholarship);
            }
        }
        Sorting::QuickSortByScholarshipReverse(outputStudents, 0, outputSize - 1);
        FileManager::writeScholarshipStatisticsToFile(resultFilename, outputStudents, outputSize,
            faculties[i], minScholarship, maxScholarship);

        delete[] outputStudents;
    }

    AdditionalFunctions::deleteStudentsArray(students, size);
}
