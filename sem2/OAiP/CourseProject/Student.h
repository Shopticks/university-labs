#ifndef STUDENT_H
#define STUDENT_H
#include <fstream>

struct Student {
private:
    char *fullName;
    char *faculty;
    double averageGrade;
    bool hasPrivileges;
    double scholarshipAmount;

public:
    // Constructor
    explicit Student(char *fullName, char *faculty,
        double averageGrade, bool hasPrivileges, double scholarshipAmount);
    // Destructor
    ~Student();

    // Setters
    void setFullName(char *fullName);
    void setFaculty(char *faculty);
    void setAverageGrade(double grade);
    void setHasPrivileges(bool hasPrivileges);
    void setScholarshipAmount(double scholarshipAmount);

    // Getters
    char* getFullName();
    char* getFaculty();
    double getAverageGrade();
    bool getHasPrivileges();
    double getScholarshipAmount();

    // Other func
    void print();
    void print(std::ofstream &file);
    Student(const Student& other); // Copying constructor
    Student& operator=(const Student& other); // Assignment operator
};

#endif //STUDENT_H
