/**
 * @author Иван Захаренков, гр. 421702
 * @file SegmentVector.h содержит объявления всех методов для класса SegmentVector и вспомогательную структуру Point.
 */

#ifndef L1_VECTOR_H
#define L1_VECTOR_H

#include <fstream>

/**
 * @struct Point
 * @brief Структура, представляющая точку в трехмерном пространстве.
 */
struct Point {
    double x; ///< Координата точки X
    double y; ///< Координата точки Y
    double z; ///< Координата точки Z

    /**
     * @brief Конструктор для точки по умолчанию.
     * @details Инициализирует точку с координатами (0, 0, 0).
     */
    Point() : x(0), y(0), z(0) {}

    /**
     * @brief Конструктор по умолчанию для точки.
     * @param x_ Координата точки X
     * @param y_ Координата точки Y
     * @param z_ Координата точки Z
     */
    Point(double x_, double y_, double z_) : x(x_), y(y_), z(z_) {}

    /**
     * @brief Оператор сравнения точек на равенство.
     * @param other Точка для сравнения
     * @return true, если координаты точек совпадают; false в противном случае
     */
    bool operator==(const Point &other) const {
        return this->x == other.x && this->y == other.y && this->z == other.z;
    }
};

/**
 * @class SegmentVector
 * @brief Класс, предназначенный для операций с векторами.
 * @details Вектор представляет собой отрезок и задается двумя концами (левый - начало, правый - конец).
 * Поддерживает основные арифметические операции, сравнение векторов и вычисление косинуса между векторами.
 */
class SegmentVector {
private:
    Point leftCorner; ///< Точка начала вектора (левый конец отрезка)
    Point rightCorner; ///< Точка конца вектора (правый конец отрезка)

public:
    /**
     * @brief Конструктор по умолчанию для вектора.
     * @details Создает нулевой вектор с началом и концом в точке (0, 0, 0).
     */
    explicit SegmentVector();

    /**
     * @brief Конструктор с параметрами для вектора.
     * @param a Точка начала вектора (левый конец отрезка)
     * @param b Точка конца вектора (правый конец отрезка)
     */
    explicit SegmentVector(const Point &, const Point &);

    /**
     * @brief Конструктор копирования для вектора.
     * @param other Вектор, который нужно скопировать
     */
    SegmentVector(const SegmentVector &);

    /**
     * @brief Получение точки начала вектора.
     * @return Точка начала вектора (левый конец отрезка)
     */
    [[nodiscard]] Point getLeftCorner() const;

    /**
     * @brief Получение точки конца вектора.
     * @return Точка конца вектора (правый конец отрезка)
     */
    [[nodiscard]] Point getRightCorner() const;

    /**
     * @brief Получение координат вектора.
     * @return Точка, представляющая векторные координаты (разность координат конца и начала)
     */
    [[nodiscard]] Point getVectorCoords() const;

    /**
     * @brief Вычисление длины вектора.
     * @return Длина вектора, вычисленная по формуле Пифагора (корень разности квадратов координат)
     */
    [[nodiscard]] double length() const;

    /**
     * @brief Оператор сложения векторов.
     * @param other Вектор для сложения
     * @return Новый вектор, полученный путем сложения координат текущего вектора с координатами переданного вектора
     * @details Начало результирующего вектора совпадает с началом текущего вектора
     */
    SegmentVector operator+(const SegmentVector &);

    /**
     * @brief Оператор присваивающего сложения.
     * @param other Вектор для сложения
     * @return Ссылка на измененный текущий вектор
     */
    SegmentVector& operator+=(const SegmentVector &);

    /**
     * @brief Оператор вычитания векторов.
     * @param other Вектор для вычитания
     * @return Новый вектор, полученный путем вычитания координат переданного вектора из координат текущего
     * @details Начало результирующего вектора совпадает с началом текущего вектора
     */
    SegmentVector operator-(const SegmentVector &);

    /**
     * @brief Оператор присваивающего вычитания.
     * @param other Вектор для вычитания
     * @return Ссылка на измененный текущий вектор
     */
    SegmentVector& operator-=(const SegmentVector &);

    /**
     * @brief Оператор векторного произведения.
     * @param other Вектор для вычисления векторного произведения
     * @return Новый вектор, представляющий собой векторное произведение текущего вектора на переданный
     * @details Начало результирующего вектора совпадает с началом текущего вектора
     */
    SegmentVector operator*(const SegmentVector &);

    /**
     * @brief Оператор присваивающего векторного произведения.
     * @param other Вектор для вычисления векторного произведения
     * @return Ссылка на измененный текущий вектор
     */
    SegmentVector& operator*=(const SegmentVector &);

    /**
     * @brief Оператор умножения вектора на скаляр.
     * @param value Скалярное значение для умножения
     * @return Новый вектор, полученный умножением координат текущего вектора на заданное число
     * @details Начало результирующего вектора совпадает с началом текущего вектора
     */
    SegmentVector operator*(double);

    /**
     * @brief Оператор присваивающего умножения на скаляр.
     * @param value Скалярное значение для умножения
     * @return Ссылка на измененный текущий вектор
     */
    SegmentVector& operator*=(double);

    /**
     * @brief Оператор поэлементного деления векторов.
     * @param other Вектор-делитель
     * @return Новый вектор, полученный делением координат текущего вектора на координаты переданного вектора
     * @throw std::invalid_argument при попытке деления на нулевую компоненту
     * @details Начало результирующего вектора совпадает с началом текущего вектора
     */
    SegmentVector operator/(const SegmentVector &);

    /**
     * @brief Оператор присваивающего поэлементного деления.
     * @param other Вектор-делитель
     * @return Ссылка на измененный текущий вектор
     * @throw std::invalid_argument при попытке деления на нулевую компоненту
     */
    SegmentVector& operator/=(const SegmentVector &);

    /**
     * @brief Оператор сравнения "больше".
     * @param other Вектор для сравнения
     * @return true, если длина текущего вектора больше длины переданного; false в противном случае
     */
    bool operator>(const SegmentVector &) const;

    /**
     * @brief Оператор сравнения "больше или равно".
     * @param other Вектор для сравнения
     * @return true, если длина текущего вектора больше или равна длине переданного; false в противном случае
     */
    bool operator>=(const SegmentVector &) const;

    /**
     * @brief Оператор сравнения "меньше".
     * @param other Вектор для сравнения
     * @return true, если длина текущего вектора меньше длины переданного; false в противном случае
     */
    bool operator<(const SegmentVector &) const;

    /**
     * @brief Оператор сравнения "меньше или равно".
     * @param other Вектор для сравнения
     * @return true, если длина текущего вектора меньше или равна длине переданного; false в противном случае
     */
    bool operator<=(const SegmentVector &) const;

    /**
     * @brief Оператор сравнения на равенство.
     * @param other Вектор для сравнения
     * @return true, если векторы эквивалентны (с учетом погрешности EPSILON = 1e-9); false в противном случае
     */
    bool operator==(const SegmentVector &) const;

    /**
     * @brief Оператор сравнения на неравенство.
     * @param other Вектор для сравнения
     * @return true, если векторы не эквивалентны; false в противном случае
     */
    bool operator!=(const SegmentVector &) const;

    /**
     * @brief Оператор присваивания.
     * @param other Вектор для копирования
     * @return Ссылка на текущий вектор после присваивания
     * @details Реализует защиту от самоприсваивания
     */
    SegmentVector& operator=(const SegmentVector &);

    /**
     * @brief Оператор вычисления косинуса угла между векторами.
     * @param other Вектор для вычисления угла
     * @return Значение косинуса угла между текущим вектором и переданным
     * @throw std::invalid_argument при попытке вычисления с нулевым вектором
     */
    double operator^(const SegmentVector &) const;

    /**
     * @brief Оператор вывода вектора в поток.
     * @param out Поток вывода
     * @param v Вектор для вывода
     * @return Ссылка на поток вывода после записи данных
     * @details Форматирует вывод в виде "SegmentVector: (x1, y1, z1) -> (x2, y2, z2);"
     */
    friend std::ostream &operator<<(std::ostream &, const SegmentVector &);

    /**
     * @brief Оператор ввода вектора из потока.
     * @param in Поток ввода
     * @param v Вектор для заполнения данными
     * @return Ссылка на поток ввода после чтения данных
     * @details Ожидает на вход шесть чисел, представляющих координаты начальной и конечной точек вектора
     */
    friend std::istream &operator>>(std::istream &, SegmentVector &);
};

#endif //L1_VECTOR_H