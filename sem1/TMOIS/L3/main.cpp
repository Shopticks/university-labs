#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> DeleteExcludedVertices(vector<vector<int>> G, vector<int> X, vector<int> Y) {
    bool needToDelete;
    for(int i = 0; i < G.size(); i++) {
        needToDelete = true;
        for(auto x : X) {
            if(G[i][0] == x) {
                needToDelete = false;
            }
        }
        if(needToDelete) G.erase(G.begin() + i);
    }

    for(int i = 0; i < G.size(); i++) {
        needToDelete = true;
        for(auto y : Y) {
            if(G[i][1] == y) {
                needToDelete = false;
            }
        }
        if(needToDelete) G.erase(G.begin() + i);
    }
    return G;
}

bool isUniqueSet(vector<int> X){        //Проверка на уникальность множеств
    for(int i = 0; i < X.size(); i++){
        for(int j = i + 1; j < X.size(); j++){
            if(X[i] == X[j]){
                return false;
            }
        }
    }
    return true;
}

vector<int> setDisplay(vector< vector<int>> G, int n){  //Проекция(образ, прообраз)
    vector<int> buffer, result;
    for(int i = 0; i < G.size(); i++){
        buffer.push_back(G[i][n]);
    }
    result.push_back(buffer[0]);
    for(auto item : buffer){
        for(int i = 0; i < result.size(); i++){
            if(item == result[i]){
                break;
            }
            if(i == result.size() - 1){
                result.push_back(item);
            }
        }
    }
    return result;
}

vector<int> equatationSet(int n){       //Заполнение множества через уравнение
    vector<int> Set;
    cout << "Enter size of the set: ";
    int size;
    cin >> size;
    for(int i = 0; i < size; i++){
        int x = 3*n + 2*i;
        Set.push_back(x);
    }
    return Set;
}

vector< vector<int>> equatationGraph(vector<int> X, vector<int> Y){     //Заполнение графика через уравнение
    vector< vector<int>> Graph;
    vector<int> buffer(2);
    for(int i = 0; i < Y.size(); i+=2){
        buffer[0] = X[0];
        buffer[1] = Y[i];
        Graph.push_back(buffer);
    }
    return Graph;
}

vector<int> randomSet(){  //Рандомное заполнение множества
    vector<int> Set;
    int size;
    cout << "Enter size of the set: ";
    cin >> size;
    int start, end;
    cout << "Enter the lower limit of the range of values: ";
    cin >> start;
    cout << "Enter the upper limit of the range of values: ";
    cin >> end;
    int iterations = 0;
    for(int i = 0; i < size; i++){
        int x = rand() % (end - start + 1) + start;
        Set.push_back(x);
        if(iterations > 100){
            Set.erase(Set.begin(), Set.end());
            cout << "Probmlems! The size of the set was changed to -1" << endl;
            Set.push_back(-1);
            return Set;
        }
        if(!isUniqueSet(Set)){
            Set.pop_back();
            i--;
            iterations++;
        }
    }
    return Set;

}

vector< vector<int>> randomGraph(vector<int> X, vector<int> Y){    //Рандомное заполнение графика
    int size;
    cout << "Enter size of the graph: ";
    cin >> size;
    vector< vector<int>> Graph;
    vector<int> buffer(2);

    int start = 0;
    int endX = X.size() - 1;
    int endY = Y.size() - 1;
    for(int i = 0; i < size; i++){
        buffer[0] = X[rand() % (endX - start + 1) + start];
        buffer[1] = Y[rand() % (endY - start + 1) + start];
        Graph.push_back(buffer);
    }
    return Graph;
}

vector<int> fillSet(){   // Ввод множества
    vector<int> Set;
    cout << "Enter size of the set: ";
    int size;
    cin >> size;
    int item;
    cout << "Enter elemements of the set: ";
    for(int i = 0; i < size; i++){
        cin >> item;
        Set.push_back(item);
    }
    return Set;
}

vector< vector<int>> fillGraph(){       //Ввод графика
    int size;
    cout << "Enter size of the graph: ";
    cin >> size;
    vector< vector<int>> graph(size, vector<int>(2));
    for(int i = 0; i<size; i++){
        cout << "Enter cortege № " << i+1 << ": ";
        cin >> graph[i][0] >> graph[i][1];
    }
    return graph;
}

vector<int> setDiff(vector<int> X, vector<int> Y){      //Разность множеств
    vector<int> result;
    for(auto item : X){
        for(int i = 0; i < Y.size(); i++){
            if(item == Y[i]){
                break;
            }
            if(i == Y.size()-1){
                result.push_back(item);
            }
        }
    }
    if(Y.size() == 0){
        for(auto item : X){
            result.push_back(item);
        }
    }
    return result;
}

vector<int> setIntersec(vector<int> X, vector<int> Y){      //Пересечние множеств
    vector<int> result;
    for(auto itemX : X){
        for(auto itemY : Y){
            if(itemX == itemY){
                result.push_back(itemX);
                break;
            }
        }
    }

    return result;
}

vector<int> setCombination(vector<int> diffResult_1, vector<int> intersecResult, vector<int> diffResult_2){   //Объединение множеств
    vector<int> result;
    for(auto item : diffResult_1){
        result.push_back(item);
    }
    for(auto item : diffResult_2){
        result.push_back(item);
    }
    for(auto item : intersecResult){
        result.push_back(item);
    }
    return result;
}

vector< vector<int>> graphDiff(vector< vector<int>> G, vector< vector<int>> P, vector<int> X, vector<int> Y){     //Разность графиков
    vector< vector<int>> result;
    for(auto item : G){
        for(int i = 0; i<P.size(); i++){
            if((item[0] == P[i][0]) && (item[1] == P[i][1])){
                break;
            }
            if(i == P.size() - 1){
                result.push_back(item);
            }
        }
    }
    return DeleteExcludedVertices(result, X, Y);
}

vector< vector<int>> graphIntersec(vector< vector<int>> G, vector< vector<int>> P, vector<int> X, vector<int> Y){     //Пересечение графиков
    vector< vector<int>> result;
    for(auto gItem : G){
        for(auto pItem : P){
            if((gItem[0] == pItem[0])&&(gItem[1] == pItem[1])){
                result.push_back(gItem);
                break;
            }
        }
    }
    return DeleteExcludedVertices(result, X, Y);
}

vector< vector<int>> graphCombination(vector< vector<int>> diffResult_1, vector< vector<int>> intersecResult, vector< vector<int>> diffResult_2){       //Объединение графиков
    vector< vector<int>> result;
    for(auto item : diffResult_1){
        result.push_back(item);
    }
    for(auto item : diffResult_2){
        result.push_back(item);
    }
    for(auto item : intersecResult){
        result.push_back(item);
    }
    return result;
}

void setOutput(vector<int> result){     //Вывод множеств в консоль
    cout<<"{ ";
    for(int i = 0; i < result.size();i++){
        if(i == result.size() - 1){
            cout << result[i];
        }
        else cout << result[i] << ", ";
    }
    cout<<" }";
}

void graphOutput(vector< vector<int>> result){      //Вывод графиков в консоль
    cout<<"{ ";
    for(int i = 0; i < result.size();i++){
        if(i == result.size() - 1){
            cout << "< " << result[i][0] << ", "<<result[i][1] << " >";
        }
        else cout << "< " << result[i][0] << ", " << result[i][1] << " >, ";
    }
    cout<<" }";
}

void inversion(vector<int> X, vector<int> Y, vector< vector<int>> G){       //Инверсия
    cout << "< { ";
    for(int i = 0; i < Y.size(); i++){
        if(i != Y.size()-1){
            cout << Y[i]<<", ";
        }
        else cout << Y[i];
    }
    cout <<" }; { ";
    for(int i = 0; i < X.size(); i++){
        if(i != X.size()-1){
            cout << X[i] << ", ";
        }
        else cout << X[i];
    }
    cout <<" }; { ";
    for(int i = 0; i < G.size(); i++){
        if(i == G.size()-1){
            cout <<"< " << G[i][1] << ", " << G[i][0] << " >";
            break;
        }
        cout << "< " << G[i][1] << ", " << G[i][0] << " >, ";
    }
    cout << " } >" << endl;
}

void composition(vector<int> X, vector<int> N, vector< vector<int>> G, vector< vector<int>> P){     //Композиция
    cout << "< { ";
    for(int i = 0; i < X.size(); i++){
        if(i != X.size()-1){
            cout << X[i] << ", ";
        }
        else cout << X[i];
    }

    cout <<" }; { ";
    for(int i = 0; i < N.size(); i++){
        if(i != N.size()-1){
            cout << N[i] << ", ";
        }
        else cout << N[i];
    }

    if(G.size() == 0 || P.size() == 0){
        cout << "{ } >";
        return ;
    }
    cout << " }; { ";
    vector< vector<int>> unfilteredRes, result;
    vector<int> buffer(2);
    for(auto gItem : G){     //Композиция графиков
        for(auto pItem : P){
            if(gItem[1] == pItem[0]){
                buffer[0] = gItem[0];
                buffer[1] = pItem[1];
                unfilteredRes.push_back(buffer);
                break;
            }
        }
    }
    for(int i = 0; i < unfilteredRes.size(); i++){  //Фильтрация композиции
        for(int j = i + 1; j < unfilteredRes.size(); j++){
            if((unfilteredRes[i][0] == unfilteredRes[j][0]) && (unfilteredRes[i][1] == unfilteredRes[j][1])){
                continue;
            }
            if(j == unfilteredRes.size() - 1){
                result.push_back(unfilteredRes[i]);
            }
        }
    }
    if(result.size() > 0 || unfilteredRes.size() == 1){
        result.push_back(unfilteredRes[unfilteredRes.size()-1]); // добавляем последний элемент, который не покрывается циклом фильтрации
    }
    for(int i = 0; i < result.size(); i++){
        if(i == result.size() - 1){
            cout << "< " << result[i][0] << ", " << result[i][1] << " >";
        }
        else cout << "< " << result[i][0] << ", " << result[i][1] << " >, ";
    }
    cout <<" } >"<<endl;
}

bool isUniqueGraph(vector< vector<int>> X){     //Проверка на уникальность графиков
    for(int i = 0; i < X.size(); i++){
        for(int j = i + 1; j < X.size(); j++){
            if(X[i][0] == X[j][0] && X[i][1] == X[j][1]){
                cout << "Enter only various corteges into the graph!";
                return false;
            }
        }
    }
    return true;
}

bool isGraphExists(vector<int> X, vector<int> Y, vector< vector<int>> G){       //Проверка на существование графика
    vector< vector<int>> result;
    vector<int> buffer(2);
    for(auto xItem : X){   //Декартово произведение двух множеств
        buffer[0] = xItem;
        for(auto yItem : Y){
            buffer[1] = yItem;
            result.push_back(buffer);
        }
    }
    for(auto item : G){     //Сравнение введенного графика с полученным декартовым произведением
                            //График не существует, если есть хоть один кортеж, которого нет в декартовом произведении
        for(int i = 0; i < result.size(); i++){
            if((item[0] == result[i][0] && (item[1] == result[i][1]))){
                break;
            }
            if(i == result.size() - 1){
                cout << "This graph doesn't exist!";
                return false;
            }
        }
    }
    return true;
}

int main(){
    vector<int> X,Y,M,N;
    vector< vector<int>> G, P;

    int option;
    cout << "Enter a number to create the correspondence. 1 - fill by youreslf, 2 - random, 3 - equatation" << endl;
    cout << "Enter a number: ";
    cin >> option;
    switch(option){
        case 1: {
            cout<<"CREATE CORRESPONDENCE 1"<<endl;
            cout<<"Create the X set"<<endl;
            X = fillSet();
            if(!isUniqueSet(X)){
                cout<<"Enter only various numbers into the set!";
                return 0;
            }
            cout<<"Create the Y set"<<endl;
            Y = fillSet();
            if(!isUniqueSet(Y)){
                cout<<"Enter only various numbers into the set!";
                return 0;
            }
            cout<<"Create the G graph"<<endl;
            G = fillGraph();
            if(!isGraphExists(X,Y,G) && !isUniqueGraph(G)){
                return 0;
            }
            cout<<endl;

            cout<<"CREATE CORRESPONDENCE 2"<<endl;
            cout<<"Create the M set"<<endl;
            M = fillSet();
            if(!isUniqueSet(M)){
                cout<<"Enter only various numbers into the set!";
                return 0;
            }
            cout<<"Create the N set"<<endl;
            N = fillSet();
            if(!isUniqueSet(N)){
                cout<<"Enter only various numbers into the set!";
                return 0;
            }
            cout<<"Create the P graph"<<endl;
            P = fillGraph();
            if(!isGraphExists(M,N,P) && !isUniqueGraph(P)){
                return 0;
            }
            break;
        }
        case 2: {
            cout<<"CREATE CORRESPONDENCE 1"<<endl;
            cout<<"Create the X set"<<endl;
            X = randomSet();
            cout<<"Create the Y set"<<endl;
            Y = randomSet();
            cout<<"Create the G graph"<<endl;
            G = randomGraph(X, Y);
            if(!isUniqueGraph(G)){
                return 0;
            }
            cout<<endl;

            cout<<"CREATE CORRESPONDENCE 2"<<endl;
            cout<<"Create the M set"<<endl;
            M = randomSet();
            cout<<"Create the N set"<<endl;
            N = randomSet();
            cout<<"Create the P graph"<<endl;
            P = randomGraph(M, N);
            if(!isUniqueGraph(P)){
                return 0;
            }
            break;
        }
        case 3: {
            cout<<"CREATE CORRESPONDENCE 1"<<endl;
            cout<<"Create the X set"<<endl;
            X = equatationSet(1);
            cout<<"Create the Y set"<<endl;
            Y = equatationSet(2);
            cout<<"Create the G graph"<<endl;
            G = equatationGraph(X, Y);
            if(!isUniqueGraph(G)){
                return 0;
            }
            cout<<endl;

            cout<<"CREATE CORRESPONDENCE 2"<<endl;
            cout<<"Create the M set"<<endl;
            M = equatationSet(1);
            cout<<"Create the N set"<<endl;
            N = equatationSet(4);
            cout<<"Create the P graph"<<endl;
            P = equatationGraph(M, N);
            if(!isUniqueGraph(P)){
                return 0;
            }
            break;
        }
        default: {
            cout << "Enter only numbers from 1 to 3";
            return 0;
        }
    }
    cout << "Correspondence 1" << endl;
    cout << "Set X: ";
    setOutput(X);
    cout << endl << "Set Y: ";
    setOutput(Y);
    cout << endl << "Graph G: ";
    graphOutput(G);
    cout << endl;
    cout << "Correspondence 2" << endl;
    cout << "Set M: ";
    setOutput(M);
    cout << endl << "Set N: ";
    setOutput(N);
    cout << endl << "Graph P: ";
    graphOutput(P);


    cout << endl << endl;
    cout << "Figuration X: ";
    setOutput(setDisplay(G, 1));
    cout << endl << "Prefiguration X: ";
    setOutput(setDisplay(G, 0));
    cout << endl;

    auto Xi = setIntersec(X,M);
    auto Yi = setIntersec(Y,N);
    cout<<"Intersection 1 and 2: < ";
    setOutput(Xi);
    cout<<"; ";
    setOutput(Yi);
    cout<<"; ";
    graphOutput(graphIntersec(G,P, Xi, Yi));
    cout<<" >"<<endl;

    Xi = setDiff(X,M);
    Yi = setDiff(Y,N);
    cout<<"Difference between 1 and 2: < ";
    setOutput(Xi);
    cout<<"; ";
    setOutput(Yi);
    cout<<"; ";
    graphOutput(graphDiff(G,P, Xi, Yi));
    cout<<" >"<<endl;

    Xi = setCombination(setDiff(X,M),setIntersec(X,M),setDiff(M,X));
    Yi = setCombination(setDiff(Y,N),setIntersec(Y,N),setDiff(N,Y));
    cout<<"Combination between 1 and 2: < ";
    setOutput(Xi);
    cout<<"; ";
    setOutput(Yi);
    cout<<"; ";
    graphOutput(graphCombination(graphDiff(G,P, Xi, Yi),
        graphIntersec(G,P, Xi, Yi),graphDiff(P,G, Xi, Yi)));
    cout<<" >"<<endl;

    cout<<"Inversion 1: ";
    inversion(X,Y,G);
    cout<<"Inversion 2: ";
    inversion(M,N,P);

    cout<<"Composition 1 and 2: ";
    composition(X, N, G, P);
    return 0;
}
