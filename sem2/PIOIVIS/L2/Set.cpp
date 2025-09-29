//
// Created by Shoptick on 21.02.25.
//

#include "Set.hpp"

Set::Set() {
    size = 0;
}

void Set::ExtractFileInformation(string filePath) {
    file.open(filePath);

    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + filePath);
    }

    string line;
    while (getline(file, line)) {
        AddNewSet(line);
    }
    file.close();

    if (size == 0) {
        throw runtime_error("File is empty");
    }
}

string Set::DeleteSpaces(string line) {
    string ansLine;
    for (char c : line) {
        if (c != ' ') {
            ansLine += c;
        }
    }
    return ansLine;
}
bool Set::TemplateCheck(string line) {
    int eq = 0, lBrackets = 0, rBrackets = 0, ltBrackets = 0, gtBrackets = 0;
    for (char c : line) {
        if (c == '=') eq++;
        if (c == '{') lBrackets++;
        if (c == '}') rBrackets++;
    }
    return  eq == 1 && line[0] != '=' &&
            lBrackets == rBrackets && ltBrackets == gtBrackets;
}

pair<string, vector<string>> Set::SplitLine(string line) {
    string name;
    vector<string> values;
    line = DeleteSpaces(line);
    if (!TemplateCheck(line))
        throw logic_error("Wrong line format");

    int l = 0, r = 0;
    while ( line[r] != '=' ) r ++;

    name = line.substr(l, r - l);

    l = r + 2;
    r = l;
    if (line[l] != '}') {
        int Bracket = 0;
        while (r != line.size() - 1) {
            if (line[r] == ',' && Bracket == 0)
                if (r - l > 0)  values.push_back(line.substr(l, r - l)),
                                l = r + 1;
                else throw std::invalid_argument("Set don't contain value between ',' and ','");

            if (line[r] == '{') Bracket++;
            if (line[r] == '}') Bracket--;
            r++;
        }
        if (r - l > 0) values.push_back(line.substr(l, r - l));
        else throw std::invalid_argument("Set don't contain value between ',' and '}'");
    }

    return make_pair(name, values);
}

void Set::AddNewSet(string line) {
    auto newSet = SplitLine(line);
    sets[newSet.first] = newSet.second;
    keys.push_back(newSet.first);
    size ++;
}


void Set::DisplaySets() {
    for (auto &k: keys) {
        cout << k << ": {";
        for (int i = 0; i < sets[k].size(); i++) {
            cout << sets[k][i];
            if (i != sets[k].size() - 1) cout << ",";
        }
        cout << "}" << endl;
    }
}

bool Set::IsSetEqual(string setName, string value) {

    for (auto &k : sets[setName]) {
        if (k[0] != '{') continue;

        unordered_map<char, int> counter;
        for (int i = 1; i < value.size() - 1; i++) {
            counter[value[i]]--;
        }

        int count = 0;
        for (int i = 1; i < k.size() - 1; i++) {
            counter[k[i]]++;
            if (counter[k[i]] == 0) count ++;
        }
        if (count ) return true;
    }
    return false;
}

bool Set::IsSubSet(string firstSet, string secondSet) {

    unordered_map<string, bool> map;
    for (auto &k: sets[firstSet])
        map[k] = true;

    for (auto &k: sets[secondSet]) {
        if (k[0] == '{') {if(!IsSetEqual(firstSet, k)) return false;}
        else if (!map[k]) return false;
    }

    return true;
}

bool Set::IsContainsSet(string firstSet, string secondSet) {
    for (auto &k : sets[secondSet])
        if (k == firstSet) return true;
    return false;
}

bool Set::Solve(string firstSet, string secondSet) {

    if (!sets.contains(firstSet) || !sets.contains(secondSet)) return false;

    vector<string> keys;

    // if (sets[firstSet].size() == 0 ||
    //     sets[secondSet].size() == 0) return true;

    return  IsSubSet(firstSet, secondSet) ||
            IsSubSet(secondSet, firstSet) ||
            IsContainsSet(firstSet, secondSet) ||
            IsContainsSet(secondSet, firstSet);
}

