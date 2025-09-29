#include "Polynomial.h"

const double EPSILON = 1e-9;

Polynomial::Polynomial(size_t degree, const double* inputCoefficients) : size(degree + 1) {
    this->coefficients = new double[this->size]();

    if (inputCoefficients != nullptr) {
        for (size_t i = 0; i < this->size; ++i) {
            this->coefficients[i] = inputCoefficients[i];
        }
    }

    this->normalize();
}

Polynomial::~Polynomial() {
    delete[] this->coefficients;
}

Polynomial::Polynomial(const Polynomial &other) : size(other.size) {
    this->coefficients = new double[this->size];

    for (size_t i = 0; i < this->size; ++i) {
        this->coefficients[i] = other.coefficients[i];
    }

    this->normalize();
}

bool Polynomial::isPolynomialZero() const {
    return calculateDegree() == -1;
}

int Polynomial::calculateDegree() const {
    for (int i = this->size - 1; i >= 0; --i) {
        if (std::abs(coefficients[i]) > EPSILON) {
            return i;
        }
    }
    return -1;
}

void Polynomial::trimLeadingZeros() {
    int newDegree = this->calculateDegree(); // Last non-zero index

    if (newDegree == -1) {
        if (this->size != 1) {
            delete[] this->coefficients;
            this->coefficients = new double[1]{0.0};
            this->size = 1;
        }
        return;
    }

    int newSize = newDegree + 1;
    if (newSize == this->size)
        return;

    auto* newCoefficients = new double[newSize];
    for (int i = 0; i < newSize; ++i) {
        newCoefficients[i] = this->coefficients[i];
    }

    delete[] this->coefficients;
    this->coefficients = newCoefficients;
    this->size = newSize;
}

void Polynomial::optimizeCoefficients() {
    for (int i = 0; i < this->size; ++i) {
        if (std::abs(this->coefficients[i]) < EPSILON) {
            this->coefficients[i] = 0;
        }
    }
}

void Polynomial::normalize() {
    this->optimizeCoefficients();
    this->trimLeadingZeros();
}

Polynomial Polynomial::operator+(const Polynomial& other) {
    size_t maxSize = std::max(this->size, other.size);
    size_t minSize = std::min(this->size, other.size);

    auto* newCoefficients = new double[maxSize]();

    for (size_t i = 0; i < minSize; ++i) {
        newCoefficients[i] = this->coefficients[i] + other.coefficients[i];
    }

    if (this->size > other.size) {
        for (size_t i = minSize; i < this->size; ++i) {
            newCoefficients[i] = this->coefficients[i];
        }
    }
    else if (other.size > this->size) {
        for (size_t i = minSize; i < other.size; ++i) {
            newCoefficients[i] = other.coefficients[i];
        }
    }

    Polynomial result(maxSize, newCoefficients);

    result.normalize();

    return result;
}

Polynomial& Polynomial::operator+=(const Polynomial& other) {
    if (other.size > this->size) {
        auto* newCoefficients = new double[other.size]();

        for (size_t i = 0; i < this->size; ++i) {
            newCoefficients[i] = this->coefficients[i];
        }

        delete[] this->coefficients;
        this->coefficients = newCoefficients;
        this->size = other.size;
    }

    for (size_t i = 0; i < other.size; ++i) {
        this->coefficients[i] += other.coefficients[i];
    }

    this->normalize();

    return (*this);
}

Polynomial Polynomial::operator-(const Polynomial& other) {
    size_t maxSize = std::max(this->size, other.size);
    size_t minSize = std::min(this->size, other.size);

    auto* newCoefficients = new double[maxSize]();

    for (size_t i = 0; i < minSize; ++i) {
        newCoefficients[i] = this->coefficients[i] - other.coefficients[i];
    }

    if (this->size > other.size) {
        for (size_t i = minSize; i < this->size; ++i) {
            newCoefficients[i] = this->coefficients[i];
        }
    }
    else if (other.size > this->size) {
        for (size_t i = minSize; i < other.size; ++i) {
            newCoefficients[i] = -other.coefficients[i];
        }
    }

    Polynomial result(maxSize, newCoefficients);

    result.normalize();

    return result;
}

Polynomial& Polynomial::operator-=(const Polynomial& other) {
    if (other.size > this->size) {
        auto* newCoefficients = new double[other.size]();

        for (size_t i = 0; i < this->size; ++i) {
            newCoefficients[i] = this->coefficients[i];
        }

        delete[] this->coefficients;
        this->coefficients = newCoefficients;
        this->size = other.size;
    }

    for (size_t i = 0; i < other.size; ++i) {
        this->coefficients[i] -= other.coefficients[i];
    }

    this->normalize();

    return (*this);
}

Polynomial Polynomial::operator*(const Polynomial& other) {
    Polynomial result(*this);
    result *= other;
    return result;
}

Polynomial& Polynomial::operator*=(const Polynomial& other) {
    size_t newSize = this->size + other.size;
    auto* newCoefficients = new double[newSize]();

    for (int i = 0; i < this->size; ++i) {
        for (int j = 0; j < other.size; ++j) {
            newCoefficients[i + j] += this->coefficients[i] * other.coefficients[j];
        }
    }

    delete[] this->coefficients;
    this->coefficients = newCoefficients;
    this->size = newSize;
    this->normalize();

    return (*this);
}

Polynomial Polynomial::operator/(const Polynomial& other) {
    if (other.isPolynomialZero())
        throw std::invalid_argument("Division by zero polynomial");

    if (this->size < other.size)
        return Polynomial(0, nullptr);

    Polynomial dividend(*this);
    size_t quotientSize = this->size - other.size + 1;
    auto* quotientCoeffs = new double[quotientSize]();

    while (dividend.size >= other.size) {
        double leadingCoeff = dividend.coefficients[dividend.size - 1] / other.coefficients[other.size - 1];
        size_t degreeDiff = dividend.size - other.size;

        quotientCoeffs[degreeDiff] = leadingCoeff;

        for (size_t i = 0; i < other.size; ++i) {
            dividend.coefficients[i + degreeDiff] -= leadingCoeff * other.coefficients[i];
        }

        dividend.normalize();
    }

    Polynomial quotient(quotientSize - 1, quotientCoeffs);
    quotient.normalize();

    return quotient;
}

Polynomial& Polynomial::operator/=(const Polynomial& other) {
    if (other.isPolynomialZero())
        throw std::invalid_argument("Division by zero polynomial");

    if (this->size < other.size) {
        this->size = 1;
        delete[] this->coefficients;
        this->coefficients = new double[1]();

        return (*this);
    }

    size_t quotientSize = this->size - other.size + 1;
    auto* quotientCoeffs = new double[quotientSize]();

    while (this->size >= other.size) {
        double leadingCoeff = this->coefficients[this->size - 1] / other.coefficients[other.size - 1];
        size_t degreeDiff = this->size - other.size;

        quotientCoeffs[degreeDiff] = leadingCoeff;

        for (size_t i = 0; i < other.size; ++i) {
            this->coefficients[i + degreeDiff] -= leadingCoeff * other.coefficients[i];
        }

        this->normalize();
    }

    this->size = quotientSize;
    delete[] this->coefficients;
    this->coefficients = quotientCoeffs;

    this->normalize();

    return (*this);
}

bool Polynomial::operator==(const Polynomial& other) const {
    if (this->size != other.size)
        return false;

    for (int i = 0; i < this->size; ++i) {
        if (this->coefficients[i] != other.coefficients[i]) {
            return false;
        }
    }

    return true;
}

bool Polynomial::operator!=(const Polynomial& other) const {
    return !((*this) == other);
}

Polynomial & Polynomial::operator=(const Polynomial& other) {
    if (this == &other) {
        return (*this);
    }

    delete[] this->coefficients;

    this->size = other.size;

    this->coefficients = new double[this->size];
    for (size_t i = 0; i < this->size; ++i) {
        this->coefficients[i] = other.coefficients[i];
    }

    return (*this);
}

double Polynomial::operator[](int index) const {
    if (index >= this->size || index < 0)
        return 0;

    return coefficients[index];
}

double Polynomial::operator()(double value) const {
    double answer = 0;
    double powCoefficient = 1;

    for (int i = 0; i < this->size; ++i) {
        answer += this->coefficients[i] * powCoefficient;
        powCoefficient *= value;
    }

    return answer;
}

std::ostream& operator<<(std::ostream &out, const Polynomial &p) {
    out << "Polynomial of degree " << p.size - 1 << " with coefficients: [";
    for (int i = 0; i < p.size - 1; ++i) {
        out << p.coefficients[i] << ", ";
    }
    out << p.coefficients[p.size - 1] << "]";
    return out;
}

std::istream& operator>>(std::istream &in, Polynomial &p) {
    size_t degree;
    in >> degree;

    p = Polynomial(degree);
    for (int i = 0; i < p.size; ++i) {
        in >> p.coefficients[i];
    }

    return in;
}