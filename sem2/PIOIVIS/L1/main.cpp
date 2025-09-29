#include <iostream>
#include <vector>
#include "PriorityQueue.hpp"

using namespace std;

int main() {

    PriorityQueue<int> pq;
    int n; cin >> n;
    vector<int> arr(n, 0);
    for (int i = 0; i < n; i++) {
     cin >> arr[i];
    }

    pq.insert(arr);

    pq.insert(9);
    cout << "After inserting 9: " << endl;
    cout << "Top value: " << pq.top() << endl;
    cout << "Popped value: " << pq.pop() << endl;

    cout << "Other value: ";
    while (!pq.empty()) {
        cout << pq.top() << ' ';
        pq.pop();
    }

    return 0;
}
