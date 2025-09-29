#include <iostream>

class AVLTree {
private:
    struct Node {
        int key;
        unsigned char height;
        Node* left;
        Node* right;

        explicit Node(int k) : key(k), left(nullptr), right(nullptr), height(1) {}
    };

    Node* root;

    // Helper function to get the height of a node
    unsigned char height(Node* p) const {
        return p ? p->height : 0;
    }

    // Helper function to calculate the balance factor
    int bfactor(Node* p) const {
        return height(p->right) - height(p->left);
    }

    // Helper function to fix the height of a node
    void fixHeight(Node* p) {
        unsigned char hl = height(p->left);
        unsigned char hr = height(p->right);
        p->height = (hl > hr ? hl : hr) + 1;
    }

    // Right rotation around p
    Node* rotateRight(Node* p) {
        Node* q = p->left;
        p->left = q->right;
        q->right = p;
        fixHeight(p);
        fixHeight(q);
        return q;
    }

    // Left rotation around q
    Node* rotateLeft(Node* q) {
        Node* p = q->right;
        q->right = p->left;
        p->left = q;
        fixHeight(q);
        fixHeight(p);
        return p;
    }

    // Balancing a node
    Node* balance(Node* p) {
        fixHeight(p);
        if (bfactor(p) == 2) {
            if (bfactor(p->right) < 0)
                p->right = rotateRight(p->right);
            return rotateLeft(p);
        }
        if (bfactor(p) == -2) {
            if (bfactor(p->left) > 0)
                p->left = rotateLeft(p->left);
            return rotateRight(p);
        }
        // Balance don't need
        return p;
    }

    // Find the node with the minimum key
    Node* findMin(Node* p) const {
        return p->left ? findMin(p->left) : p;
    }

    // Remove the node with the minimum key
    Node* removeMin(Node* p) {
        if (!p->left)
            return p->right;
        p->left = removeMin(p->left);
        return balance(p);
    }

    // Recursive insertion function
    Node* insert(Node* p, int k) {
        if (!p) return new Node(k);
        if (k < p->key)
            p->left = insert(p->left, k);
        else
            p->right = insert(p->right, k);
        return balance(p);
    }

    // Recursive removal function
    Node* remove(Node* p, int k) {
        if (!p) return nullptr;
        if (k < p->key)
            p->left = remove(p->left, k);
        else if (k > p->key)
            p->right = remove(p->right, k);
        else { // k == p->key
            Node* q = p->left;
            Node* r = p->right;
            delete p;
            if (!r) return q;
            Node* min = findMin(r);
            min->right = removeMin(r);
            min->left = q;
            return balance(min);
        }
        return balance(p);
    }

    // Search value function
    bool search(Node* p, int k) {
        if (!p) return false;
        if (k < p->key)
            return search(p->left, k);
        else
            return search(p->right, k);
    }

    // Recursive in-order function
    void printInOrder(Node* node) const {
        if (!node) return;
        printInOrder(node->left);
        std::cout << node->key << " ";
        printInOrder(node->right);
    }

    // Recursive pre-order function
    void printPreOrder(Node* node) const {
        if (!node) return;
        std::cout << node->key << " ";
        printPreOrder(node->left);
        printPreOrder(node->right);
    }

    // Recursive post-order function
    void printPostOrder(Node* node) const {
        if (!node) return;
        printPostOrder(node->left);
        printPostOrder(node->right);
        std::cout << node->key << " ";
    }

    // Recursive function to print tree
    void printTreeRec(const std::string& prefix, const Node* node, bool isLeft)
    {
        if( node != nullptr )
        {
            std::cout << prefix;

            std::cout << (isLeft ? "├── " : "└── " );

            std::cout << node->key << std::endl;

            printTreeRec( prefix + (isLeft ? "│   " : "    "), node->left, true);
            printTreeRec( prefix + (isLeft ? "│   " : "    "), node->right, false);
        }
    }

public:


    AVLTree() : root(nullptr) {}

    // Insert a key into the AVL tree
    void insert(int key) {
        root = insert(root, key);
    }

    // Remove a key from the AVL tree
    void remove(int key) {
        root = remove(root, key);
    }

    // Find a key from the AVL tree
    bool search(int key) {
        return search(root, key);
    }

    // Balance tree
    void balance() {
        root = balance(root);
    }

    // Print in-order
    void printInOrder() const {
        printInOrder(root);
        std::cout << std::endl;
    }

    // Print tree
    void printTree() {
        printTreeRec("", root, false);
    }

    // Print pre-order
    void printPreOrder() const {
        printPreOrder(root);
        std::cout << std::endl;
    }

    // Print post-order
    void printPostOrder() const {
        printPostOrder(root);
        std::cout << std::endl;
    }

};

int main() {
    AVLTree tree;
    int choice = -1;

    while (choice != 0) {
        std::cout << "----- Instructions -----" << std::endl;
        std::cout << "1. Insert" << std::endl;
        std::cout << "2. Remove" << std::endl;
        std::cout << "3. Find element" << std::endl;
        std::cout << "4. Print array" << std::endl;
        std::cout << "5. Print tree" << std::endl;
        std::cout << "0. Exit" << std::endl;
        std::cout << "Enter your choice: ";
        std::cin >> choice;

        switch (choice) {
            case 1: {
                std::cout << "Enter element to insert: ";
                int value;
                std::cin >> value;
                tree.insert(value);
                break;
            }
            case 2: {
                std::cout << "Enter element to remove: ";
                int value;
                std::cin >> value;
                tree.remove(value);
                break;
            }
            case 3: {
                std::cout << "Enter element to find: " << std::endl;
                int value;
                std::cin >> value;

                std::cout << (tree.search(value) ? "Element found!" : "Element not found!") << std::endl;
                break;
            }
            case 4: {
                std::cout << "1. Pre-order" << std::endl;
                std::cout << "2. Post-order" << std::endl;
                std::cout << "3. In-order" << std::endl;
                std::cout << "0. Exit" << std::endl;
                std::cout << "Enter type: ";
                int value;
                std::cin >> value;

                switch (value) {
                    case 1: {
                        tree.printPreOrder();
                        break;
                    }
                    case 2: {
                        tree.printPostOrder();
                        break;
                    }
                    case 3: {
                        tree.printInOrder();
                        break;
                    }
                    case 0: {
                        break;
                    }
                }
                break;
            }
            case 5: {
                tree.printTree();
                break;
            }
            case 0: {
                break;
            }
            default: {
                std::cout << "Invalid choice" << std::endl;
                break;
            }
        }
    }

    return 0;
}