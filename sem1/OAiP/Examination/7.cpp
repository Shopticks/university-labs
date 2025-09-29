#include <iostream>

using namespace std;

int main() {

    int n, ans = 0, zeros = 0, zzeros = 0; cin >> n;
    int *A = new int[n];

    for (int i = 0; i < n; ++i) {
        cin >> A[i];
        if ((i + 1) % 2 == 0) ans += A[i];
        if (A[i] < 0) A[i] = 0, zeros ++;
    }

    for (int i = 0; i < n; ++i) {
        if (A[i] == 0) {
            zzeros ++;
            if (zzeros == 1 || zzeros == zeros) continue;
            A[i] = (A[i - 1] + A[i + 1]) / 2;
        }
    }

    cout << ans << endl;
    for (int i = 0; i < n; ++i) {
        cout << A[i] << " ";
    }

    delete[] A;
    return 0;
}