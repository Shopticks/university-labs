#include <iostream>

using namespace std;

int main() {

    int n, ansSum = 0, ansMult = 1; cin >> n;
    int A[n][n], B[n];

    for (int i = 0; i < n; i++) {
        B[i] = 0;
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> A[i][j];
            ansSum += (A[i][j] != 0 ? 1 : 0);
            ansMult *= (A[i][j] > 0 ? A[i][j] : 1);
            if (A[i][j] < 0 && B[j] == 0) B[j] = 1;
        }
    }

    cout << "B: ";
    for (int i = 0; i < n; i++) {
        cout << B[i] << " ";
    }
    cout << endl;

    cout << "A:\n";
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << A[i][j] << " ";
        }
        cout << endl;
    }
    cout << "Sum: " << ansSum << endl;
    cout << "Multiplication: " << ansMult << endl;


    return 0;
}