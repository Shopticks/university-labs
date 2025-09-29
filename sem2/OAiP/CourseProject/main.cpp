#include <iostream>
#include "Database.h"
#include "FileManager.h"
#include "Operations.h"

int main() {

    const char* storageFilename = "Storage.bin";
    const char* resultFilename = "result.txt";
    size_t charSize = 255;

    int choose = -1;
    while (choose != 0){
        std::cout << "----- Instruction -----";
        std::cout << '\n' << "0. Quit program";
        std::cout << '\n' << "1. Database operations";
        std::cout << '\n' << "2. Search";
        std::cout << '\n' << "3. Sorting";
        std::cout << '\n' << "4. Statistics";
        std::cout << '\n' << "Choose an option: ";
        std::cin >> choose;

        switch (choose) {
            case 1: {
                std::cout << "-----------------------" << std::endl;
                std::cout << "0. Return to main instructions" << std::endl;
                std::cout << "1. Display all students" << std::endl;
                std::cout << "2. Add new student" << std::endl;
                std::cout << "3. Delete student" << std::endl;
                std::cout << "4. Clear database" << std::endl;
                std::cout << "5. Edit student info" << std::endl;
                std::cout << "Choose an option: ";
                int choose2;
                std::cin >> choose2;
                switch (choose2) {
                    case 1: {
                        Database::displayAll(storageFilename);
                        break;
                    }
                    case 2: {
                        std::cin.ignore();

                        std::cout << "Enter student's full name: ";
                        char* fullName = new char[charSize];
                        std::cin.getline(fullName, charSize);
                        if (strcmp(fullName, "") == 0) {
                            std::cerr << "Invalid input" << std::endl;
                            break;
                        }

                        std::cout << "Enter student's faculty: ";
                        char* faculty = new char[charSize];
                        std::cin.getline(faculty, charSize);
                        if (strcmp(faculty, "") == 0) {
                            std::cerr << "Invalid input" << std::endl;
                            break;
                        }

                        std::cout << "Enter student's grade: ";
                        char* grade = new char[charSize];
                        std::cin.getline(grade, charSize);
                        double averageGrade;
                        if (AdditionalFunctions::isDigit(grade))
                            averageGrade = std::stof(grade);
                        else {
                            std::cout << "Invalid input" << std::endl;
                            break;
                        }

                        std::cout << "Enter student's privileges (1 or 0): ";
                        char* privileges = new char[charSize];
                        std::cin.getline(privileges, charSize);
                        bool hasPrivileges = false;
                        if (strcmp(privileges, "1") == 0)
                            hasPrivileges = true;
                        else if (strcmp(privileges, "0") == 0)
                            hasPrivileges = false;
                        else {
                            std::cout << "Invalid input" << std::endl;
                            break;
                        }

                        std::cout << "Enter student's scholarship: ";
                        char* scholarship = new char[charSize];
                        std::cin.getline(scholarship, charSize);
                        double scholarshipAmount;
                        if (AdditionalFunctions::isDigit(scholarship))
                            scholarshipAmount = std::stof(scholarship);
                        else {
                            std::cout << "Invalid input" << std::endl;
                            break;
                        }

                        Database::addStudent(storageFilename, new Student(fullName, faculty,
                            averageGrade, hasPrivileges, scholarshipAmount));

                        delete[] privileges;
                        delete[] scholarship;
                        delete[] grade;
                        delete[] faculty;
                        delete[] fullName;
                        break;
                    }
                    case 3: {
                        size_t studentNumber;
                        size_t cnt = FileManager::getNumberOfStudentsInFile(storageFilename);
                        if (cnt == 0) {
                            std::cerr << "Database is empty" << std::endl;
                            break;
                        }
                        std::cout << "Enter student number to delete (1-" << cnt << "): ";
                        std::cin.ignore();
                        char number[charSize];
                        std::cin.getline(number, charSize);
                        if (AdditionalFunctions::isDigit(number)){
                            int studentNumber = std::stoi(number);
                            if (Database::deleteStudent(storageFilename, studentNumber)) {
                                std::cout << "Student deleted successfully.\n";
                            }
                            else {
                                std::cerr << "Failed to delete student.\n";
                            }
                        }
                        else {
                            std::cerr << "Failed to delete student.\n";
                        }
                        break;
                    }
                    case 4: {
                        std::cout << "Confirmation (1-yes, 0-no): ";
                        std::cin.ignore();
                        char isCorrect[charSize];
                        std::cin.getline(isCorrect, charSize);

                        if (strcmp(isCorrect, "1") != 0) {
                            std::cout << "Aborting operation...\n";
                            break;
                        }

                        FileManager::clearFile(storageFilename);
                        break;
                    }
                    case 5: {
                        Student** students = nullptr;
                        size_t count = 0;

                        if (!FileManager::readStudentsFromFile(storageFilename, students, count)) {
                            std::cerr << "Database is empty or cannot be accessed.\n";
                            break;
                        }

                        int studentNumber;
                        std::cout << "Enter student number to edit (1-" << count << "): ";
                        char number[charSize];
                        std::cin.ignore();
                        std::cin.getline(number, charSize);
                        if (AdditionalFunctions::isDigit(number))
                            studentNumber = std::stoi(number);
                        else
                            break;

                        if (studentNumber < 1 || studentNumber > count) {
                            std::cerr << "Invalid student number.\n";
                            AdditionalFunctions::deleteStudentsArray(students, count);
                            break;
                        }

                        Student* oldStudent = students[studentNumber - 1];

                        char    fullName[charSize], faculty[charSize],
                                gradeStr[charSize], privStr[charSize],
                                scholStr[charSize];

                        std::cout << "Current full name: " << oldStudent->getFullName()
                                  << ". Enter new (press Enter to keep): ";
                        std::cin.getline(fullName, charSize);

                        std::cout << "Current faculty: " << oldStudent->getFaculty()
                                  << ". Enter new (press Enter to keep): ";
                        std::cin.getline(faculty, charSize);

                        std::cout << "Current average grade: " << oldStudent->getAverageGrade()
                                  << ". Enter new (press Enter to keep): ";
                        std::cin.getline(gradeStr, charSize);

                        std::cout << "Current privileges (0 or 1): " << oldStudent->getHasPrivileges()
                                  << ". Enter new (press Enter to keep): ";
                        std::cin.getline(privStr, charSize);

                        std::cout << "Current scholarship amount: " << oldStudent->getScholarshipAmount()
                                  << ". Enter new (press Enter to keep): ";
                        std::cin.getline(scholStr, charSize);

                        // Validate and build new values
                        const char* newFullName = strlen(fullName) > 0 ? fullName : oldStudent->getFullName();
                        const char* newFaculty = strlen(faculty) > 0 ? faculty : oldStudent->getFaculty();

                        double newGrade = oldStudent->getAverageGrade();
                        if (strlen(gradeStr) > 0) {
                            if (!AdditionalFunctions::isDigit(gradeStr)) {
                                std::cerr << "Invalid grade input.\n";
                                AdditionalFunctions::deleteStudentsArray(students, count);
                                break;
                            }
                            newGrade = std::stof(gradeStr);
                        }

                        bool newPrivilege = oldStudent->getHasPrivileges();
                        if (strlen(privStr) > 0) {
                            if (strcmp(privStr, "0") == 0)
                                newPrivilege = false;
                            else if (strcmp(privStr, "1") == 0)
                                newPrivilege = true;
                            else {
                                std::cerr << "Invalid privileges input.\n";
                                AdditionalFunctions::deleteStudentsArray(students, count);
                                break;
                            }
                        }

                        double newScholarship = oldStudent->getScholarshipAmount();
                        if (strlen(scholStr) > 0) {
                            if (!AdditionalFunctions::isDigit(scholStr)) {
                                std::cerr << "Invalid scholarship input.\n";
                                AdditionalFunctions::deleteStudentsArray(students, count);
                                break;
                            }
                            newScholarship = std::stof(scholStr);
                        }

                        // Create updated student
                        Student* updatedStudent = new Student(
                            const_cast<char*>(newFullName),
                            const_cast<char*>(newFaculty),
                            newGrade,
                            newPrivilege,
                            newScholarship
                        );

                        std::cout << "Check correct input:\n";
                        updatedStudent->print();
                        std::cout << "Confirmation of changes to records (1 - yes, 0 - no): ";
                        char isCorrectInput[charSize];
                        std::cin.getline(isCorrectInput, charSize);

                        if (strcmp(isCorrectInput, "1") != 0) {
                            std::cerr << "Aborting operation...\n";
                            delete updatedStudent;
                            AdditionalFunctions::deleteStudentsArray(students, count);

                            break;
                        }

                        // Perform the update
                        if (!Database::changeStudentInfo(storageFilename, updatedStudent, studentNumber)) {
                            std::cerr << "Failed to update student information.\n";
                            delete updatedStudent;
                        }

                        AdditionalFunctions::deleteStudentsArray(students, count);
                        break;
                    }
                    case 0: {
                        break;
                    }
                    default: {
                        std::cout << "Wrong choose. Returning to main instructions" << std::endl;
                        break;
                    }
                }

                break;
            }
            case 2: {
                std::cout << "----------------------" << std::endl;
                std::cout << "0. Return to main instructions" << std::endl;
                std::cout << "1. Linear search by name" << std::endl;
                std::cout << "2. Binary search by grade" << std::endl;
                std::cout << "Choose an option: ";
                int choose2;
                std::cin >> choose2;

                switch (choose2) {
                    case 1: {
                        char* name = new char[charSize];
                        std::cout << "Enter student's full name: ";
                        std::cin.ignore();
                        std::cin.getline(name, charSize);
                        Database::linearSearchByName(storageFilename, name);
                        break;
                    }
                    case 2: {
                        double grade;
                        std::cout << "Enter student's grade: ";
                        std::cin >> grade;
                        Database::binarySearchByGrade(storageFilename, grade);
                        break;
                    }
                    case 0: {
                        break;
                    }
                    default: {
                        std::cout << "Wrong choose. Returning to main instructions" << std::endl;
                        break;
                    }
                }
                break;
            }
            case 3: {
                std::cout << "----------------------" << std::endl;
                std::cout << "0. Return to main instructions" << std::endl;
                std::cout << "1. Quick sort by scholarship" << std::endl;
                std::cout << "2. Selection sort by grade" << std::endl;
                std::cout << "3. Insertion sort by name" << std::endl;
                std::cout << "Choose an option: ";
                int choose2;
                std::cin >> choose2;

                switch (choose2) {
                    case 1: {
                        Database::quickSortByScholarship(storageFilename);
                        break;
                    }
                    case 2: {
                        Database::selectionSortByGrade(storageFilename);
                        break;
                    }
                    case 3: {
                        Database::insertionSortByName(storageFilename);
                        break;
                    }
                    case 0: {
                        break;
                    }
                    default: {
                        std::cout << "Wrong choose. Returning to main instructions" << std::endl;
                        break;
                    }
                }
                break;
            }
            case 4: {
                std::cout << "----------------------" << std::endl;
                std::cout << "0. Return to main instructions" << std::endl;
                std::cout << "1. Identify students for an increased scholarship" << std::endl;
                std::cout << "2. Scholarship statistics" << std::endl;
                std::cout << "Choose an option: ";
                int choose2;
                std::cin >> choose2;

                switch (choose2) {
                    case 1: {
                        double grade = 0;
                        std::cout << "Enter student's grade: ";
                        std::cin >> grade;

                        int privileges = false;
                        std::cout << "Enter student's privileges (1 or 0): ";
                        std::cin >> privileges;

                        Database::identifyIncreasedScholarship(storageFilename,
                            resultFilename, grade, privileges > 0);

                        break;
                    }
                    case 2: {
                        Database::scholarshipStatistics(storageFilename, resultFilename);
                        break;
                    }
                    case 0: {
                        break;
                    }
                    default: {
                        std::cout << "Wrong choose. Returning to main instructions" << std::endl;
                        break;
                    }
                }
                break;
            }
            case 0: {
                std::cout << "Program exiting..." << std::endl;
                break;
            }
            default: {
                std::cerr << "Wrong choice." << std::endl;
                continue;
            }
        }
    }

    std::cout << "The program has been successfully completed!" << std::endl;

    return 0;
}
