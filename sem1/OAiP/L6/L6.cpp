#include <iostream>

using namespace std;

void func(char *array, int size) {
    for(int i = 0; i < size; i++) {
        cout << array[i] << '\n';
    }
    cout << '\n';
    for(int i = 0; i < size; ++i) {
        for(int j = 0; j < i; ++j) {
            cout << ' ';
        }
        cout << array[i] << '\n';
    }
    cout << '\n';
    for(int i = 0; i < size; ++i) {
        for(int j = size - i - 2; j > -1; --j) {
            cout << ' ';
        }
        cout << array[i] << '\n';
    }
}

int main() {

    int n; cin >> n;
    char *array {new char[n + 1]};

    for(int i = 0; i < n; i++) {
        cin >> array[i];
    }
    
    array[n] = "\0";

    func(array, n);

    return 0;
}
