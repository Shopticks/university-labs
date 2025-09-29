#include <iostream>
#include <cstring>
#include <fstream>

struct Person {
    char surname[50]; // Last name
    int weight = 0;   // Weight
    int height = 0;   // Height
};

struct HashNode {
    Person data;
    HashNode* next;

    explicit HashNode(const Person& person) {
        strcpy(this->data.surname, person.surname);
        this->data.weight = person.weight;
        this->data.height = person.height;
        this->next = nullptr;
    }
};

class HashTable {
private:
    int size;         // Size of the hash table
    HashNode** table; // Array of pointers to linked lists

public:
    HashTable(int m) : size(m) {
        table = new HashNode*[size];
        for (int i = 0; i < size; ++i) {
            table[i] = nullptr;
        }
    }

    ~HashTable() {
        for (int i = 0; i < size; ++i) {
            HashNode* current = table[i];
            while (current != nullptr) {
                HashNode* temp = current;
                current = current->next;
                delete temp;
            }
        }
        delete[] table;
    }

    int hashFunction(int key) {
        return key % size;
    }

    void insert(const Person& person) {
        int index = hashFunction(person.weight);
        HashNode* newNode = new HashNode(person);

        if (table[index] == nullptr) {
            table[index] = newNode;
        } else {

            HashNode* current = table[index];
            while (current->next != nullptr) {
                current = current->next;
            }
            current->next = newNode;
        }
    }

    bool erase(int key) {
        int index = hashFunction(key);
        HashNode* current = table[index];
        HashNode* prev = nullptr;

        // Traverse the linked list at the hashed index
        while (current != nullptr) {
            if (current->data.weight == key) {
                if (prev == nullptr) {
                    // Node to delete is the head of the list
                    table[index] = current->next;
                } else {
                    // Node to delete is in the middle or end of the list
                    prev->next = current->next;
                }
                delete current; // Free memory
                return true;    // Successfully erased
            }
            prev = current;
            current = current->next;
        }

        return false; // Key not found
    }

    Person* search(int key) {
        int index = hashFunction(key);
        HashNode* current = table[index];

        while (current != nullptr) {
            if (current->data.weight == key) {
                return &current->data;
            }
            current = current->next;
        }

        return nullptr; // Not found
    }

    void printHashTable() {
        std::cout << "Hash Table:" << std::endl;
        for (int i = 0; i < size; ++i) {
            std::cout << i << ": ";
            HashNode* current = table[i];
            while (current != nullptr) {
                std::cout << "(" << current->data.surname << ", " << current->data.weight << ", "
                     << current->data.height << ") -> ";
                current = current->next;
            }
            std::cout << "nullptr" << std::endl;
        }
    }

    void clear() {
        for (int i = 0; i < size; ++i) {
            if (table[i] != nullptr) {
                delete table[i];
            }
        }
        delete[] table;

        table = new HashNode*[size];
        for (int i = 0; i < size; ++i) {
            table[i] = nullptr;
        }
    }
};

int main() {
    std::cout << "Enter hash table size: ";
    int m = 10;  // Size of the hash table
    std::cin >> m;

    HashTable hashTable(m);

    int choise = -1;
    while (choise != 0) {
        std::cout << "----- Instructions -----" << std::endl;
        std::cout << "1. Print hash table" << std::endl;
        std::cout << "2. Insert person" << std::endl;
        std::cout << "3. Erase person" << std::endl;
        std::cout << "4. Search person" << std::endl;
        std::cout << "5. Clear hash table" << std::endl;
        std::cout << "0. Exit" << std::endl;
        std::cout << "Enter your choice: ";
        std::cin >> choise;

        switch (choise) {
            case 1: {
                hashTable.printHashTable();
                break;
            }
            case 2: {
                char surname[50];
                std::cout << "Enter the surname: ";
                std::cin >> surname;

                int weight;
                std::cout << "Enter the weight: ";
                std::cin >> weight;

                int height;
                std::cout << "Enter the height: ";
                std::cin >> height;

                Person person;
                strcpy(person.surname, surname);
                person.weight = weight;
                person.height = height;

                hashTable.insert(person);

                break;
            }
            case 3: {
                int weight;
                std::cout << "Enter the weight: ";
                std::cin >> weight;

                if(!hashTable.erase(weight))
                    std::cout << "Key was not found" << std::endl;
                break;
            }
            case 4: {
                int weight;
                std::cout << "Enter the weight: ";
                std::cin >> weight;

                Person *person = hashTable.search(weight);
                if (person == nullptr) {
                    std::cout << "Key was not found" << std::endl;
                    break;
                }
                std::cout << "Found person:" << std::endl;
                std::cout << "Surname: " << person->surname << std::endl;
                std::cout << "Weight: " << person->weight << std::endl;
                std::cout << "Height: " << person->height << std::endl;
                break;
            }
            case 5: {
                hashTable.clear();
                break;
            }
            case 0: {
                break;
            }
            default:
                std::cout << "Invalid choice" << std::endl;
                break;
        }
    }



    return 0;
}