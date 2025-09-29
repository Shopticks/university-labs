#include <iostream>
#include "Set.hpp"
#include <unordered_map>

int main() {
    Set set;
    set.ExtractFileInformation("input.txt");
    set.DisplaySets();

    cout << set.Solve("A", "B") << endl;
    return 0;
}
