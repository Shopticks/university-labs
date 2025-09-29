#include "SegmentVector.h"

#include <iostream>
#include <cmath>

const int FACTOR = 1e6;
const double EPSILON = 1e-9;

SegmentVector::SegmentVector() : leftCorner(Point()), rightCorner(Point()) {}

SegmentVector::SegmentVector(const Point &a, const Point &b)
    : leftCorner(a), rightCorner(b) {}

SegmentVector::SegmentVector(const SegmentVector& other)
    : leftCorner(other.leftCorner), rightCorner(other.rightCorner) {}

Point SegmentVector::getLeftCorner() const {
    return this->leftCorner;
}

Point SegmentVector::getRightCorner() const {
    return this->rightCorner;
}

Point SegmentVector::getVectorCoords() const {
    return Point(rightCorner.x - leftCorner.x,
                 rightCorner.y - leftCorner.y,
                 rightCorner.z - leftCorner.z);
}

double SegmentVector::length() const {
    return std::sqrt(
        std::pow(rightCorner.x - leftCorner.x, 2) +
        std::pow(rightCorner.y - leftCorner.y, 2) +
        std::pow(rightCorner.z - leftCorner.z, 2)
        );
}

SegmentVector SegmentVector::operator+(const SegmentVector& other){
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    // Sum on coordinates
    Point sumVec(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);

    // Set corners
    Point newLeft = this->leftCorner;
    Point newRight(newLeft.x + sumVec.x, newLeft.y + sumVec.y, newLeft.z + sumVec.z);

    return SegmentVector(newLeft, newRight);
}

SegmentVector& SegmentVector::operator+=(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    // Sum of coordinates
    Point sumVec(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z);

    // Change current vector coordinates
    rightCorner.x = leftCorner.x + sumVec.x;
    rightCorner.y = leftCorner.y + sumVec.y;
    rightCorner.z = leftCorner.z + sumVec.z;

    return *this;
}

SegmentVector SegmentVector::operator-(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    Point diffVec(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);

    Point newLeft = this->leftCorner;
    Point newRight(newLeft.x + diffVec.x, newLeft.y + diffVec.y, newLeft.z + diffVec.z);

    return SegmentVector(newLeft, newRight);
}

SegmentVector& SegmentVector::operator-=(const SegmentVector& other){
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    Point diffVec(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);

    rightCorner.x = leftCorner.x + diffVec.x;
    rightCorner.y = leftCorner.y + diffVec.y;
    rightCorner.z = leftCorner.z + diffVec.z;

    return *this;
}

SegmentVector SegmentVector::operator*(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    Point crossVec(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    );

    Point newLeft = this->leftCorner;
    Point newRight(newLeft.x + crossVec.x, newLeft.y + crossVec.y, newLeft.z + crossVec.z);

    return SegmentVector(newLeft, newRight);
}

SegmentVector& SegmentVector::operator*=(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    Point crossVec(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    );

    this->rightCorner.x = this->leftCorner.x + crossVec.x;
    this->rightCorner.y = this->leftCorner.y + crossVec.y;
    this->rightCorner.z = this->leftCorner.z + crossVec.z;

    return *this;
}

SegmentVector SegmentVector::operator*(const double value) {
    Point v1 = this->getVectorCoords();

    Point newLeft = this->leftCorner;
    Point newRight(
        newLeft.x + v1.x * value,
        newLeft.y + v1.y * value,
        newLeft.z + v1.z * value
    );

    return SegmentVector(newLeft, newRight);
}

SegmentVector & SegmentVector::operator*=(const double value) {
    Point v1 = this->getVectorCoords();

    this->rightCorner.x = this->leftCorner.x + v1.x * value;
    this->rightCorner.y = this->leftCorner.y + v1.y * value;
    this->rightCorner.z = this->leftCorner.z + v1.z * value;

    return *this;
}

SegmentVector SegmentVector::operator/(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    if (std::abs(v2.x) < EPSILON || std::abs(v2.y) < EPSILON || std::abs(v2.z) < EPSILON) {
        throw std::invalid_argument("Division by zero (or near-zero) in vector components");
    }

    Point divVec(v1.x / v2.x, v1.y / v2.y, v1.z / v2.z);

    Point newLeft = this->leftCorner;
    Point newRight(newLeft.x + divVec.x, newLeft.y + divVec.y, newLeft.z + divVec.z);

    return SegmentVector(newLeft, newRight);
}

SegmentVector& SegmentVector::operator/=(const SegmentVector& other) {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    if (std::abs(v2.x) < EPSILON || std::abs(v2.y) < EPSILON || std::abs(v2.z) < EPSILON) {
        throw std::invalid_argument("Division by zero (or near-zero) in vector components");
    }

    Point divVec(v1.x / v2.x, v1.y / v2.y, v1.z / v2.z);

    this->rightCorner.x = this->leftCorner.x + divVec.x;
    this->rightCorner.y = this->leftCorner.y + divVec.y;
    this->rightCorner.z = this->leftCorner.z + divVec.z;

    return *this;
}

bool SegmentVector::operator>(const SegmentVector& other) const {
    double len1 = this->length();
    double len2 = other.length();

    return len1 > len2;
}

bool SegmentVector::operator>=(const SegmentVector& other) const {
    double len1 = this->length();
    double len2 = other.length();

    return len1 >= len2;
}

bool SegmentVector::operator<(const SegmentVector& other) const {
    double len1 = this->length();
    double len2 = other.length();

    return len1 < len2;
}

bool SegmentVector::operator<=(const SegmentVector& other) const {
    double len1 = this->length();
    double len2 = other.length();

    return len1 <= len2;
}

bool SegmentVector::operator==(const SegmentVector& other) const {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    return (std::abs(v1.x - v2.x) < EPSILON) &&
           (std::abs(v1.y - v2.y) < EPSILON) &&
           (std::abs(v1.z - v2.z) < EPSILON);
}

bool SegmentVector::operator!=(const SegmentVector &other) const {
    return !((*this) == other);
}

SegmentVector& SegmentVector::operator=(const SegmentVector& other) {
    if (this == &other) {
        return *this;
    }

    this->leftCorner = other.leftCorner;
    this->rightCorner = other.rightCorner;

    return *this;
}

double SegmentVector::operator^(const SegmentVector &other) const {
    Point v1 = this->getVectorCoords();
    Point v2 = other.getVectorCoords();

    double dotProduct = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
    double len1 = this->length();
    double len2 = other.length();

    if (len1 < EPSILON || len2 < EPSILON) {
        throw std::invalid_argument("Cannot calculate angle with zero-length vector");
    }
    return round(dotProduct / (len1 * len2) * FACTOR) / FACTOR;
}

std::ostream& operator<<(std::ostream &out, const SegmentVector &v) {
    out << "SegmentVector: ("
        << v.leftCorner.x << ", " << v.leftCorner.y << ", " << v.leftCorner.z
        << ") -> ("
        << v.rightCorner.x << ", " << v.rightCorner.y << ", " << v.rightCorner.z
        << ");";

    return out;
}

std::istream& operator>>(std::istream& in, SegmentVector& v) {
    int x1, y1, z1,
        x2, y2, z2;

    in  >> x1 >> y1 >> z1
        >> x2 >> y2 >> z2;

    Point left(x1, y1, z1);
    Point right(x2, y2, z2);

    v.leftCorner = left;
    v.rightCorner = right;

    return in;
}
