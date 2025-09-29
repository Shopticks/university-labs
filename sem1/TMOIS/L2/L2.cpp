#include <iostream>
#include <vector>
#include <string>

using namespace std;

void DisplaySet(string messege, vector<pair<int, int>> set) {
    cout << messege << "{";
    if(set.size() > 0) {
        cout << "<" << set[0].first << ", " << set[0].second << ">";
        for(int i = 1; i < set.size(); i++){
            cout << ", <" << set[i].first << ", " << set[i].second << ">";
        }
    }
    cout << "}" << endl;
}

void DisplaySet(string messege, vector<int> set) {
    cout << messege << "{ ";
    if(set.size() > 0) {
        cout << set[0];
        for(int i = 1; i < set.size(); i++) {
            cout << ", " << set[i];
        }
        cout << ' ';
    }
    cout << "}" << endl;
}

pair<int, int> CheckSimilar(pair<int, int> _pair, vector<pair<int, int>> &Set) {

    for(int i = 0; i < Set.size(); i++) {
        if(Set[i] == _pair) {
            _pair = make_pair(rand() % 100 + 1, rand() % 100 + 1);
            i = -1;
        }
    }
    return _pair;
}

void InputSets(int &PSize, int &QSize, vector<pair<int, int>> &P, vector<pair<int, int>> &Q) {
    cout << "Введите размер множества P: "; cin >> PSize;
    while(PSize < 0) {
        cout << "Ошибка, введите корректный размер множества P: "; cin >> PSize;
    }
    cout << "Введите размер множества Q: "; cin >> QSize;
    while(QSize < 0) {
        cout << "Ошибка, введите корректный размер множества Q: "; cin >> QSize;
    }

    P.resize(PSize, pair<int, int>(0, 0));
    Q.resize(QSize, pair<int, int>(0, 0));

    cout << "Ввод множества (0 - автоматически, 1 - вручную): ";

    int value;cin >> value;
    while(value != 0 && value != 1) {
        cout << "Ошибка, введите корректное значение (0 или 1): "; cin >> value;
    }

    switch (value) {
        case 0:
            for(int i = 0; i < PSize; i++) {
                P[i] = CheckSimilar(make_pair(rand() % 100 + 1, rand() % 100 + 1), P);
            }
            for(int i = 0; i < QSize; i++) {
                Q[i] = CheckSimilar(make_pair(rand() % 100 + 1, rand() % 100 + 1), Q);
            }
            DisplaySet("Множество P: ", P);
            DisplaySet("Множество Q: ", Q);
            cout << endl;
            break;
        case 1:
            cout << "Введите множество P:\n";
            for(int i = 0; i < PSize; i++) {
                cout << i + 1 << " пара: " << endl;
                cin >> P[i].first >> P[i].second;
            }
            cout << "Введите множество Q:\n";
            for(int i = 0; i < QSize; i++) {
                cout << i + 1 << " пара: " << endl;
                cin >> Q[i].first >> Q[i].second;
            }
            cout << endl;
            break;
    }



}

void Inversion(int PSize, int QSize, vector<pair<int, int>> &P, vector<pair<int, int>> &Q) {
    vector<pair<int, int>> InvP(PSize), InvQ(QSize);
    for (int i = 0; i < PSize; i++) {
        InvP[i].first = P[i].second;
        InvP[i].second = P[i].first;
    }
    for (int i = 0; i < QSize; i++) {
        InvQ[i].first = Q[i].second;
        InvQ[i].second = Q[i].first;
    }

    DisplaySet("Инверсия множества P: ", InvP);
    DisplaySet("Инверсия множества Q: ", InvQ);
    cout << endl;
}

void Composition(int PSize, int QSize, vector<pair<int, int>> &P, vector<pair<int, int>> &Q) {
    vector<pair<int, int>> CompPQ, CompQP;
    for(int i = 0; i < PSize; i++) {
        for(int j = 0; j < QSize; j++) {
            if(P[i].second == Q[j].first)
                CompPQ.push_back(make_pair(P[i].first, Q[j].second));
        }
    }
    for(int i = 0; i < QSize; i++) {
        for(int j = 0; j < PSize; j++) {
            if(Q[i].second == P[j].first)
                CompQP.push_back(make_pair(Q[i].first, P[j].second));
        }
    }

    DisplaySet("Композиция множества P и Q: ", CompPQ);
    DisplaySet("Композиция множества Q и P: ", CompQP);
    cout << endl;
}

void CheckForEqualElements(vector<pair<int, int>> &DecMPQ) {
    for(int i = 0; i < DecMPQ.size(); i++) {
        for(int j = i + 1; j < DecMPQ.size(); j++) {
            if(DecMPQ[i].first == DecMPQ[j].first && DecMPQ[i].second == DecMPQ[j].second) {
                DecMPQ.erase(DecMPQ.begin() + j);
            }
        }
    }
}

void DecartMultiplication(vector<pair<int, int>> &P, vector<pair<int, int>> &Q) {
    vector<pair<int, int>> DecMPQ;
    for(pair<int, int> p : P) {
        for(pair<int, int> q : Q) {
            DecMPQ.push_back(make_pair(p.first, q.first));
            DecMPQ.push_back(make_pair(p.second, q.second));
        }
    }

    CheckForEqualElements(DecMPQ);

    DisplaySet("Декартово произведение P и Q: ", DecMPQ);
    cout << endl;
}

void CheckSimilar(vector<int> &ProjP1) {
    for(int i = 0; i < ProjP1.size(); i++) {
        for(int j = i + 1; j < ProjP1.size(); j++) {
            if(ProjP1[i] == ProjP1[j]) {
                ProjP1.erase(ProjP1.begin() + j);
            }
        }
    }
}

void Projection(vector<pair<int, int>> &P, vector<pair<int, int>> &Q) {
    vector<int> ProjP1, ProjP2;
    for(pair<int, int> p : P) {
        ProjP1.push_back(p.first);
        ProjP2.push_back(p.second);
    }
    vector<int> ProjQ1, ProjQ2;
    for(auto q : Q) {
        ProjQ1.push_back(q.first);
        ProjQ2.push_back(q.second);
    }

    CheckSimilar(ProjP1);
    CheckSimilar(ProjP2);
    CheckSimilar(ProjQ1);
    CheckSimilar(ProjQ2);

    DisplaySet("Проекция P на 1: ", ProjP1);
    DisplaySet("Проекция P на 2: ", ProjP2);
    DisplaySet("Проекция Q на 1: ", ProjQ1);
    DisplaySet("Проекция Q на 2: ", ProjQ2);
}

int main() {

    srand(time(0));

    int PSize;
    int QSize;
    vector<pair<int, int>> P;
    vector<pair<int, int>> Q;
    InputSets(PSize, QSize, P, Q);

    CheckForEqualElements(P);
    CheckForEqualElements(Q);
    PSize = P.size();
    QSize = Q.size();

    Inversion(PSize, QSize, P, Q);

    Composition(PSize, QSize, P, Q);

    DecartMultiplication(P, Q);

    Projection(P, Q);

    return 0;
}
