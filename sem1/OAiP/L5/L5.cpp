#include <iostream>

using namespace std;

int func(int **matrix, int size) {

    for(int i = 0; i < size; ++i) {
        for(int j = 0; j < size; ++j) {
            matrix[i][size] += matrix[i][j];
            matrix[size][j] += matrix[i][j];
        }
    }

    int check = matrix[size][0];

    for(int i = 0; i < size; ++i) {
        if(matrix[size][i] != check || matrix[i][size] != check) {
            return 0;
        }
    }

    return 1;

}

int main() {

    int n; cin >> n;
    n++;

    int **matrix {new int*[n]{}};
    for (int i = 0; i < n; i++) {
        matrix[i] = new int[n]{};
    }

    for(int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1; ++j) {
            cin >> matrix[i][j];
        }
    }

    cout << (!func(matrix, n - 1) ?
        "The matrix is not a magic square!" :
        "The matrix is a magic square!");

    for (int i = 0; i < n; ++i)
        delete [] matrix[i];
    delete [] matrix;

    return 0;
}