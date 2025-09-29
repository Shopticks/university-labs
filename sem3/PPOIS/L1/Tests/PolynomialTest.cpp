#include "gtest/gtest.h"
#include "Polynomial.h"

TEST(AriphmeticOperationsPolynomialTest, Addition) {
    auto    *answerCoefficients = new double[]{5, 4, 3, 2, 1},
            *firstCoefficients = new double[]{3, 1, 2, 2},
            *secondCoefficients = new double[]{2, 3, 1, 0, 1};

    Polynomial  answer(4, answerCoefficients),
                p1(3, firstCoefficients),
                p2(4, secondCoefficients);

    EXPECT_EQ(p1 + p2, answer);
    EXPECT_EQ(p2 + p1, answer);

    p1 += p2;

    EXPECT_EQ(p1, answer);

    delete[] answerCoefficients;
    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(AriphmeticOperationsPolynomialTest, Substraction) {
    auto    *firstAnswerCoefficients = new double[]{3, 1, 2, 2},
            *secondAnswerCoefficients = new double[]{0, 2, 1, 0, 1},
            *thirdAnswerCoefficients = new double[]{0, -2, -1, 0, -1},
            *firstCoefficients = new double[]{5, 4, 3, 2, 1},
            *secondCoefficients = new double[]{2, 3, 1, 0, 1},
            *thirdCoefficients = new double[]{2, 1};

    Polynomial  firstAnswer(3, firstAnswerCoefficients),
                secondAnswer(4, secondAnswerCoefficients),
                thirdAnswer(4, thirdAnswerCoefficients),
                p1(4, firstCoefficients),
                p2(4, secondCoefficients),
                p3(1, thirdCoefficients);

    EXPECT_EQ(p1 - p2, firstAnswer);
    EXPECT_EQ(p2 - p3, secondAnswer);
    EXPECT_EQ(p3 - p2, thirdAnswer);

    p1 -= p2;
    p3 -= p2;

    EXPECT_EQ(p1, firstAnswer);
    EXPECT_EQ(p3, thirdAnswer);

    delete[] firstAnswerCoefficients;
    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(AriphmeticOperationsPolynomialTest, Multiplitcation) {
    auto    *answerCoefficients = new double[]{1, 7, 14, 20},
            *firstCoefficients = new double[]{1, 2, 4},
            *secondCoefficients = new double[]{1, 5};

    Polynomial  answer(3, answerCoefficients),
                p1(2, firstCoefficients),
                p2(1, secondCoefficients);

    EXPECT_EQ(p1 * p2, answer);

    p1 *= p2;

    EXPECT_EQ(p1, answer);

    delete[] answerCoefficients;
    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(AriphmeticOperationsPolynomialTest, Division) {
    auto    *firstAnswerCoefficients = new double[]{-4, 3},
            *secondAnswerCoefficients = new double[]{0},
            *firstCoefficients = new double[]{-5, 1, -4, 3},
            *secondCoefficients = new double[]{1, 0, 1},
            *zeroCoefficients = new double[]{0, 0};

    Polynomial  firstAnswer(1, firstAnswerCoefficients),
                secondAnswer(1, secondAnswerCoefficients),
                p1(3, firstCoefficients),
                p2(2, secondCoefficients),
                p0(1, zeroCoefficients);

    EXPECT_EQ(p1 / p2, firstAnswer);
    EXPECT_EQ(p2 / p1, secondAnswer);

    EXPECT_EQ(p2 /= p1, secondAnswer);

    p2 = Polynomial(2, secondCoefficients);

    EXPECT_EQ(p1 /= p2, firstAnswer);

    EXPECT_ANY_THROW(p1 /= p0);

    delete[] firstAnswerCoefficients;
    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(ComparisonOperationsPolynomialTest, Equality) {
    auto    *firstCoefficients = new double[]{-1, 0.0000000000001, 3, 6, 1, 0, 0, 0, 0, 0, 0.0000000000001},
            *secondCoefficients = new double[]{-1, 0, 3, 6, 1};

    Polynomial  p1(10, firstCoefficients),
                p2(4, secondCoefficients);

    EXPECT_EQ(p1 == p2, true);

    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(ComparisonOperationsPolynomialTest, UnEquality) {
    auto    *firstCoefficients = new double[]{-1, 0.0000000000001, 3, 6, 1, 0, 0, 0, 0, 0, 0.0000000000001},
            *secondCoefficients = new double[]{-1, 0, 3, 6, 1};

    Polynomial  p1(10, firstCoefficients),
                p2(4, secondCoefficients);

    EXPECT_EQ(p1 != p2, false);

    delete[] firstCoefficients;
    delete[] secondCoefficients;
}

TEST(AccessOperatorsPolynomialTest, SquareBrackets) {
    auto *Coefficients = new double[](-1, 0.0000000000001, 3, 6, 1, 0, 0, 0, 0, 0, 0.0000000000001);

    Polynomial p(10, Coefficients);

    EXPECT_EQ(p[1], 0);
    EXPECT_EQ(p[2], 3);
    EXPECT_EQ(p[5], 0);
    EXPECT_EQ(p[10000], 0);

    delete[] Coefficients;
}

TEST(AccessOperatorsPolynomialTest, RoundBrackets) {
    auto *Coefficients = new double[](-1, 0.0000000000001, 3, 6, 1, 0, 0, 0, 0, 0, 0.0000000000001);

    Polynomial p(10, Coefficients);

    EXPECT_EQ(p(5), 1449);
    EXPECT_EQ(p(0), -1);

    delete[] Coefficients;
}

TEST(OtherFunctionsPolynomialTest, Normalize) {
    Polynomial p(-1, nullptr);

    p.normalize();
}