#include "gtest/gtest.h"
#include "SegmentVector.h"

TEST(AriphmeticOperationsSegmentVectorTest, Addition) {
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(-5, -16, 3);
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -3, 1);

    SegmentVector   answer(answerFirstPoint, answerSecondPoint),
                    v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 + v2, answer);

    v1 += v2;

    EXPECT_EQ(v1, answer);
}

TEST(AriphmeticOperationsSegmentVectorTest, Substraction) {
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(9, 6, 3);
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -3, 1);

    SegmentVector   answer(answerFirstPoint, answerSecondPoint),
                    v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 - v2, answer);

    v1 -= v2;

    EXPECT_EQ(v1, answer);
}

TEST(AriphmeticOperationsSegmentVectorTest, ScalarMultiplication) {
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(-2, -14, 5);
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);

    SegmentVector   answer(answerFirstPoint, answerSecondPoint),
                    v1(v1FirstPoint, v1SecondPoint);

    EXPECT_EQ(v1 * 2, answer);

    v1 *= 2;

    EXPECT_EQ(v1, answer);
}

TEST(AriphmeticOperationsSegmentVectorTest, VectorsMultiplication) {
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(28, -10, -18);
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -3, 1);

    SegmentVector   answer(answerFirstPoint, answerSecondPoint),
                    v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 * v2, answer);

    v1 *= v2;

    EXPECT_EQ(v1, answer);
}

TEST(AriphmeticOperationsSegmentVectorTest, Division) {
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(6.5, 4.6, 3);
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-6, -7, 2);
    Point zeroFirstPoint(1, 2, 3), zeroSecondPoint(2, 2, 2);

    SegmentVector   answer(answerFirstPoint, answerSecondPoint),
                    v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint),
                    v0(zeroFirstPoint, zeroSecondPoint);

    EXPECT_EQ(v1 / v2, answer);

    v1 /= v2;

    EXPECT_EQ(v1, answer);

    EXPECT_ANY_THROW(v2 / v0);

    EXPECT_ANY_THROW(v1 /= v0);
}


TEST(AriphmeticOperationsSegmentVectorTest, Cos) {
    double answer = 0.969212;
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -3, 1);
    Point zeroFirstPoint(1, 2, 3), zeroSecondPoint(1, 2, 3);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint),
                    v0(zeroFirstPoint, zeroFirstPoint);

    EXPECT_EQ(v1 ^ v2, answer);
    EXPECT_ANY_THROW(v1 ^ v0);
}

TEST(ComparisonOperationsSegmentVectorTest, Equality) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-2, -1, 3);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 == v2, true);
}

TEST(ComparisonOperationsSegmentVectorTest, UnEquality) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -10, 13);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 != v2, true);
}

TEST(ComparisonOperationsSegmentVectorTest, Greater) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -10, 13);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 > v2, false);
}

TEST(ComparisonOperationsSegmentVectorTest, GreaterOrEqual) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -10, 13);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 >= v2, false);
}

TEST(ComparisonOperationsSegmentVectorTest, Less) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -10, 13);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 < v2, true);
}

TEST(ComparisonOperationsSegmentVectorTest, LessOrEqual) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);
    Point v2FirstPoint(2, 8, 1), v2SecondPoint(-5, -10, 13);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint),
                    v2(v2FirstPoint, v2SecondPoint);

    EXPECT_EQ(v1 <= v2, true);
}

TEST(OtherOperatorsSegmentVectorTest, Assignment) {
    Point v1FirstPoint(6, 4, 1), v1SecondPoint(2, -5, 3);

    SegmentVector   v1(v1FirstPoint, v1SecondPoint), v2;
    v2 = v1;

    EXPECT_EQ(v1 == v2, true);

    v1 = v1;

    EXPECT_EQ(v1, v1);
}

TEST(OtherFunctionsSegmentVectorTest, Getters) {
    Point vFirstPoint(6, 4, 1), vSecondPoint(2, -5, 3);
    Point answerFirstPoint(6, 4, 1), answerSecondPoint(2, -5, 3);

    SegmentVector v(vFirstPoint, vSecondPoint);

    EXPECT_EQ(v.getLeftCorner(), answerFirstPoint);
    EXPECT_EQ(v.getRightCorner(), answerSecondPoint);
}