#include "Operations.h"

#pragma region Search

void Search::LinearSearchByName(Student **inputStudents, size_t inputSize,
    Student **&outputStudents, size_t &outputSize, const char *name) {

    outputStudents = new Student*[inputSize];
    outputSize = 0;

    for (size_t i = 0; i < inputSize; i++) {
        if (strcmp(inputStudents[i]->getFullName(), name) == 0) {
            outputStudents[outputSize++] = inputStudents[i];
        }
    }
}

void Search::BinarySearchByGrade(Student **inputStudents, size_t inputSize,
    Student **&outputStudents, size_t &outputSize, double grade) {

    size_t left = 0, right = inputSize - 1;
    while (left < right) {

        size_t mid = (left + right) / 2;

        if (inputStudents[mid]->getAverageGrade() < grade) {
            left = mid + 1;
        }
        else{
            right = mid;
        }
    }

    outputSize = 0;
    for (size_t i = left; i < inputSize; i++) {
        if (round(inputStudents[i]->getAverageGrade() * 100) / 100 == round(grade * 100) / 100) {
            outputStudents[outputSize++] = inputStudents[i];
        }
        else break;
    }
}

#pragma endregion

#pragma region Sorting

size_t Sorting::QuickSortPartition(Student **&arr, long long low, long long high) {

    double pivot = arr[high]->getScholarshipAmount();

    long long i = low - 1;

    for (long long j = low; j <= high - 1; j++) {
        if (arr[j]->getScholarshipAmount() < pivot)
            std::swap(arr[++i], arr[j]);
    }

    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}
void Sorting::QuickSortByScholarship(Student **&arr, long long low, long long high) {
    if (low < high) {

        long long pi = QuickSortPartition(arr, low, high);

        QuickSortByScholarship(arr, low, pi - 1);
        QuickSortByScholarship(arr, pi + 1, high);
    }
}

size_t Sorting::QuickSortPartitionReverse(Student **&arr, long long low, long long high) {
    double pivot = arr[high]->getScholarshipAmount();

    long long i = low - 1;

    for (long long j = low; j <= high - 1; j++) {
        if (arr[j]->getScholarshipAmount() > pivot)
            std::swap(arr[++i], arr[j]);
    }

    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}
void Sorting::QuickSortByScholarshipReverse(Student **&arr, long long low, long long high) {
    if (low < high) {

        long long pi = QuickSortPartitionReverse(arr, low, high);

        QuickSortByScholarshipReverse(arr, low, pi - 1);
        QuickSortByScholarshipReverse(arr, pi + 1, high);
    }
}

void Sorting::SelectionSortByGrade(Student **&arr, size_t size) {

    for (size_t i = 0; i < size - 1; i++) {
        size_t minIndex = i;
        for (size_t j = i + 1; j < size; j++) {
            if (arr[j]->getAverageGrade() < arr[minIndex]->getAverageGrade()) {
                minIndex = j;
            }
        }
        std::swap(arr[i], arr[minIndex]);
    }

}

void Sorting::SelectionSortByGradeReverse(Student **&arr, size_t size) {
    for (size_t i = 0; i < size - 1; i++) {
        size_t minIndex = i;
        for (size_t j = i + 1; j < size; j++) {
            if (arr[j]->getAverageGrade() > arr[minIndex]->getAverageGrade()) {
                minIndex = j;
            }
        }
        std::swap(arr[i], arr[minIndex]);
    }
}

void Sorting::InsertionSortByName(Student **&arr, size_t size) {
    for (size_t i = 1; i < size; ++i) {
        Student* key = arr[i];
        long long j = i - 1;

        // Сравнение строк через `std::string`
        while (j >= 0 && AdditionalFunctions::compareChars(arr[j]->getFullName(), key->getFullName())) {
            arr[j + 1] = arr[j];
            --j;
        }

        arr[j + 1] = key;
    }
}


#pragma endregion

#pragma region Additional functions

void AdditionalFunctions::findFaculties(Student **arr, size_t size, char **&faculties,
    size_t &facultiesSize) {
    faculties = new char*[size];
    facultiesSize = 0;

    faculties[facultiesSize++] = arr[0]->getFaculty();
    for (size_t i = 1; i < size; i++) {
        bool found = false;
        char* faculty = arr[i]->getFaculty();
        for (size_t j = 0; j < facultiesSize; j++) {
            if (strcmp(arr[i]->getFaculty(), faculties[j]) == 0) {
                found = true;
                break;
            }
        }
        if (!found) {
            faculties[facultiesSize++] = arr[i]->getFaculty();
        }
    }
}

bool AdditionalFunctions::isDigit(char *c) {
    size_t size = strlen(c);
    for (size_t i = 0; i < size; i++) {
        if (!((c[i] >= '0' && c[i] <= '9') || (c[i] == ',') || (c[i] == '.')))
            return false;
    }
    return true;
}

void AdditionalFunctions::deleteStudentsArray(Student **inputStudents, size_t inputSize) {
    if (inputStudents == nullptr || inputSize == 0)
        return;

    for (size_t i = 0; i < inputSize; i++) {
        if (inputStudents[i] != nullptr)
            delete inputStudents[i];
    }

    delete[] inputStudents;
}

bool AdditionalFunctions::compareChars(const char* a, const char* b) {
    if (a == b) return 0;      // Same pointer or both null
    if (!a) return -1;         // `a` is null (treated as smaller)
    if (!b) return 1;          // `b` is null (treated as smaller)

    while (*a && *b && *a == *b) {
        a++;
        b++;
    }
    return (*a - *b) > 0;
}

#pragma endregion
