#include <iostream>
#include <string>
using namespace std;

double cycle(int n){
    double x1, x2, x3, result=1;
    for(int i=0; i<n; i++){
        x1 = (i + 1) * 2;
        x2 = 1 + i * 2;
        x3 = (i + 1) * 2 + 1;
        result *= (x1 / x2) * (x1 / x3);
    }
    return result;
}

double rec(int n){
    if(n <= 0){
        return 1;
    }
    else{
        double x1, x2, x3, r;
        x1 = n * 2;
        x2 = 1 + (n - 1) * 2;
        x3 = n * 2 + 1;
        r = (x1 / x2) * (x1 / x3);
        return r * rec(n - 1);
    }
}

int main(){
    string s;
    cin >> s;
    cout << s.size();
    return 0;
}