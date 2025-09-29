//
// Created by Shoptick on 21.02.25.
//

#ifndef SET_HPP
#define SET_HPP

#include <unordered_map>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>

using namespace std;

class Set {
private:
    unordered_map<string, vector<string>> sets;
    vector<string> keys;
    int size;
    ifstream file;
    string setTemplate;

    pair<string, vector<string>> SplitLine(string line);
    string DeleteSpaces(string line);
    void AddNewSet(string line);
    bool IsSubSet(string firstSet, string secondSet);
    bool IsContainsSet(string firstSet, string secondSet);
    bool TemplateCheck(string line);
    bool IsSetEqual(string set, string value);
public:
    explicit Set();
    void ExtractFileInformation(string filePath);
    void DisplaySets();
    bool Solve(string firstSet, string secondSet);
};

#endif //SET_HPP
