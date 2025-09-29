#include <iostream>
#include <fstream>

using namespace std;

struct StudentInfo {
    char lastName[100];
    int group = 0;

    int mathMark = 0;
    int physMark = 0;
    int infoMark = 0;
    double averageMark = 0.0;

    bool NameGreater(StudentInfo studentInfo) {
        for(int i = 0; i <= 100; i++) {
            if(lastName[i] == '\0' || lastName[i] > studentInfo.lastName[i]) return true;
            if(studentInfo.lastName[i] == '\0' || lastName[i] < studentInfo.lastName[i]) return false;
        }
    }

    void CalculateAverageMark() {
        averageMark = (mathMark + physMark + infoMark) / 3.0;
    }
};

void PrintInformation(StudentInfo* studentInfo, const int studentCount) {
    cout << "-------------------------" << '\n';
    for (int i = 0; i < studentCount; i++) {
        cout << i + 1 << ". " << studentInfo[i].lastName << ", " << studentInfo[i].group << "\n";
        cout << "Отметки за семестр:\n";
        cout << "Математика: " << studentInfo[i].mathMark << '\n';
        cout << "Физика: " << studentInfo[i].physMark << '\n';
        cout << "Информатика: " << studentInfo[i].infoMark << '\n';
        cout << "Средняя отметка: " << studentInfo[i].averageMark << '\n';
        cout << "-------------------------" << '\n';
    }
}

#pragma region Add new student with information

void InputAndCheckMark(int &mark, const char* message, const bool readFromFile) {
    ifstream fin("Students_List.txt");
    while ((readFromFile ? fin : cin) >> mark) {
        if(mark > 10 || mark < 1) {
            cout << "Неверный формат оценки (необходимо ввести от 1 до 10, попробуйте ещё раз.\n";
        }
        else {
            break;
        }
        cout << message;
    }
    fin.close();
}

void InputStudent(StudentInfo*& studentInfo, const int studentCount,
    const int value, const bool readFromFile) {

    ifstream fin("Students_List.txt");

    if(value == 1 || value == 7) {
        cout << "Введите фамилию: ";
        (readFromFile ? fin : cin) >> studentInfo[studentCount].lastName;
    }

    if(value == 2 || value == 7) {
        cout << "Введите номер группы: ";
        (readFromFile ? fin : cin) >> studentInfo[studentCount].group;
    }

    if(value == 3 || value == 7) {
        cout << "Введите отметку по математике: ";
        InputAndCheckMark(studentInfo[studentCount].mathMark,
            "Введите отметку по математике: ", readFromFile);
    }

    if(value == 4 || value == 7) {
        cout << "Введите отметку по физике: ";
        InputAndCheckMark(studentInfo[studentCount].physMark,
            "Введите отметку по физике: ", readFromFile);
    }

    if(value == 5 || value == 7) {
        cout << "Введите отметку по информатике: ";
        InputAndCheckMark(studentInfo[studentCount].infoMark,
            "Введите отметку по информатике: ", readFromFile);
    }

    studentInfo[studentCount].CalculateAverageMark();
    fin.close();
}

void AddStudent(StudentInfo*& studentInfo, const int studentCount, const bool readFromFile) {
    StudentInfo* newStudentInfo = new StudentInfo[studentCount + 1];
    for (int i = 0; i < studentCount; i++) {
        newStudentInfo[i] = studentInfo[i];
    }
    studentInfo = newStudentInfo;
    InputStudent(studentInfo, studentCount, 7, readFromFile);
}

#pragma endregion Add new student with information

void SolveProblem(const StudentInfo* studentInfo, const int studentCount) {
    double generalAverageMark = 0.0;
    for (int i = 0; i < studentCount; i++) {
        generalAverageMark += studentInfo[i].averageMark;
    }
    generalAverageMark /= studentCount;

    cout << "Решение задачи:\n";
    for(int i = 0; i < studentCount; i++) {
        if(studentInfo[i].averageMark > generalAverageMark) {
            cout << studentInfo[i].lastName << ", " << studentInfo[i].group << "\n";
        }
    }
}

void EditStudent(StudentInfo*& studentInfo, const int studentCount) {
    int numberOfStudent;
    cout << "Введите номер студента, которого необходимо изменить: ";
    while (cin >> numberOfStudent) {
        if(numberOfStudent > studentCount) {
            cout << "Студента не существует, введите корректного студента. Количество студентов: ";
            cout << studentCount << "\n";
        } else if(numberOfStudent < 1) {
            cout << "Номера студентов начинаются с 1. Введите корректное число!" << '\n';
        }
        else break;

        cout << "Введите номер студента, которого необходимо изменить: ";
    }

    cout << "--------Инструкция--------" << '\n';
    cout << "Изменение фамилии - 1, группы - 2, отметок: математика - 3, физика - 4, информатика - 5" << '\n';
    int editIndex;
    cout << "Ввод инструкции: ";
    while (cin >> editIndex) {
        if(!(editIndex >= 1 && editIndex <= 5)) {
            cout << "Введите корректное значение (диапазон 1 - 5)" << '\n';
        }
        else break;
        cout << "Ввод инструкции: ";
    }

    switch (editIndex) {
        case 1:
            InputStudent(studentInfo, numberOfStudent - 1, 1, 0);
            break;

        case 2:
            InputStudent(studentInfo, numberOfStudent - 1, 2, 0);
            break;

        case 3:
            InputStudent(studentInfo, numberOfStudent - 1, 3, 0);
            break;

        case 4:
            InputStudent(studentInfo, numberOfStudent - 1, 4, 0);
            break;

        case 5:
            InputStudent(studentInfo, numberOfStudent - 1, 5, 0);
            break;
    }
}

void DeleteStudent(StudentInfo*& studentInfo, const int studentCount) {
    int numberOfStudent;
    cout << "Введите номер удаляемого студента: ";
    while (cin >> numberOfStudent) {
        if(!(numberOfStudent >= 1 && numberOfStudent <= studentCount)) {
            cout << "Введите корректный номер студента!" << '\n';
        }
        else break;
        cout << "Введите номер удаляемого студента: ";
    }

    StudentInfo* newStudentInfo = new StudentInfo[studentCount - 1];
    for (int i = 0; i < studentCount; i++) {
        if(numberOfStudent == i + 1) continue;
        newStudentInfo[(i + 1 > numberOfStudent ? i - 1 : i)] = studentInfo[i];
    }
    delete[] studentInfo;
    studentInfo = newStudentInfo;
}

void SortStudents(StudentInfo*& studentInfo, const int studentCount) {

    cout << "Инструкция" << '\n';
    cout << "Сортировка по: 1 - фамилии, 2 - группе, " <<
                 "оценке: 3 - математики, 4 - физики, " <<
                 "5 - информатики, 6 - средней арифметической" << '\n';
    int sortIndex;
    cout << "Ввод инструкции: ";
    while (cin >> sortIndex) {
        if(!(sortIndex >= 1 && sortIndex <= 6)) {
            cout << "Введите корректное значение (диапазон 1 - 6)" << '\n';
        }
        else break;
        cout << "Ввод инструкции: ";
    }

    switch (sortIndex) {
        case 1:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].NameGreater(studentInfo[j]))
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;

        case 2:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].group > studentInfo[j].group)
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;
        case 3:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].mathMark > studentInfo[j].mathMark)
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;
        case 4:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].physMark > studentInfo[j].physMark)
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;
        case 5:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].infoMark > studentInfo[j].infoMark)
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;
        case 6:
            for(int i = 0; i < studentCount; i++) {
                for(int j = i + 1; j < studentCount; j++) {
                    if(studentInfo[i].averageMark > studentInfo[j].averageMark)
                        swap(studentInfo[i], studentInfo[j]);
                }
            }
        break;
    }
}

void ReadOrWriteFile(StudentInfo*& studentInfo, int& studentCount) {
    int value;
    cout << "Инструкция: " << '\n';
    cout << "Ввод с заменой - 1, ввод без замены - 2, вывод - 3, выход - 4" << '\n';
    cout << "Введите инструкцию: ";
    while (cin >> value) {
        if(!(value >= 1 && value <= 4)) {
            cout << "Введите корректную инструкцию!" << '\n';
        }
        else break;
        cout << "Введите инструкцию: ";
    }

    switch (value) {
        case 1: {
            ifstream fin("Students_List.txt");
            if(studentCount != -1)
                delete[] studentInfo;
            studentInfo = new StudentInfo();
            fin >> studentCount;
            StudentInfo* newStudentInfo = new StudentInfo[studentCount];
            for(int i = 0; i < studentCount; i++) {
                fin >> newStudentInfo[i].lastName;
                fin >> newStudentInfo[i].group;
                fin >> newStudentInfo[i].mathMark;
                fin >> newStudentInfo[i].physMark;
                fin >> newStudentInfo[i].infoMark;
                newStudentInfo[i].CalculateAverageMark();
            }
            studentInfo = newStudentInfo;
            fin.close();
            break;
        }

        case 2: {
            ifstream fin("Students_List.txt");
            int pr;
            fin >> pr;
            StudentInfo* newStudentInfo = new StudentInfo[studentCount + pr];
            for(int i = 0; i < studentCount + pr; i++) {
                if(i + 1 > studentCount) {
                    fin >> newStudentInfo[i].lastName >> newStudentInfo[i].group
                    >> newStudentInfo[i].mathMark >> newStudentInfo[i].physMark
                    >> newStudentInfo[i].infoMark;
                    newStudentInfo[i].CalculateAverageMark();
                }
                else newStudentInfo[i] = studentInfo[i];
            }
            delete[] studentInfo;
            studentCount += pr;
            studentInfo = newStudentInfo;
            fin.close();
            break;
        }

        case 3: {
            ofstream fout("Students_List.txt");
            fout << studentCount << '\n';
            for(int i = 0; i < studentCount; i++) {
                fout << studentInfo[i].lastName << '\n';
                fout << studentInfo[i].group << '\n';
                fout << studentInfo[i].mathMark << '\n';
                fout << studentInfo[i].physMark << '\n';
                fout << studentInfo[i].infoMark << '\n';
            }
            fout.close();
            break;
        }

        default:
            break;
    }
}


int main() {
    //setlocale(LC_ALL, "ru");

    int studentCount = -1;
    StudentInfo* studentInfo;

    cout << "Инструкция: \n";
    cout << "1 - Создание, 2 - Просмотр, 3 - Добавление,\n " <<
                 "4 - Решение задачи, 5 - Редактирование, 6 - Удаление,\n " <<
                 "7 - Сортировка, 8 - Вывод-ввод в файл, 9 - Выход" << '\n';

    while (true) {
        cout << "Ввод инструкции: ";
        int value;
        cin >> value;

        switch (value) {
            case 1:
                if(studentCount != -1)
                    delete[] studentInfo;
                studentInfo = new StudentInfo();
                studentCount = 0;
                break;

            case 2:
                if(studentCount > 0)
                    PrintInformation(studentInfo, studentCount);
                else cout << "Ошибка, необходимо инициализировать и(или) добавить какой-нибудь элемент" <<
                             "в массив" << '\n';
                break;

            case 3:
                if(studentCount != -1) {
                    AddStudent(studentInfo, studentCount, 0);
                    studentCount++;
                }
                else cout << "Ошибка, необходимо инициализировать массив" << '\n';
                break;

            case 4:
                if(studentCount > 0)
                    SolveProblem(studentInfo, studentCount);
                else cout << "Ошибка, необходимо инициализировать и(или) добавить какой-нибудь элемент" <<
                             "в массив" << '\n';
                break;

            case 5:
                if(studentCount > 0)
                    EditStudent(studentInfo, studentCount);
                else cout << "Ошибка, необходимо инициализировать и(или) добавить какой-нибудь элемент" <<
                             "в массив" << '\n';
                break;

            case 6:
                if(studentCount > 0) {
                    DeleteStudent(studentInfo, studentCount);
                    studentCount--;
                }
                else cout << "Ошибка, необходимо инициализировать и(или) добавить какой-нибудь элемент" <<
                             "в массив" << '\n';
                break;

            case 7:
                if(studentCount > 0)
                    SortStudents(studentInfo, studentCount);
                else cout << "Ошибка, необходимо инициализировать и(или) добавить какой-нибудь элемент" <<
                 "в массив" << '\n';
                break;

            case 8:
                ReadOrWriteFile(studentInfo, studentCount);
                break;

            case 9:
                return 0;
                break;

            default:
                cout << "Введите корректное значение\n";
                break;
        }
    }
}