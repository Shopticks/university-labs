def dec_to_bin_mag(n):
    """Translation of a positive integer into a binary string."""
    if n == 0:
        return "0"
    res = ""
    while n > 0:
        res = str(n % 2) + res
        n = n // 2
    return res

def bin_to_dec_mag(b):
    """Translation of a binary string into a positive integer."""
    res = 0
    for i, bit in enumerate(reversed(b)):
        if bit == '1':
            res += 2 ** i
    return res

def add_bin_strings(a, b):
    """Bit-by-bit addition of two binary strings of the same length."""
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    res = ""
    carry = 0
    for i in range(max_len - 1, -1, -1):
        bit_sum = int(a[i]) + int(b[i]) + carry
        res = str(bit_sum % 2) + res
        carry = bit_sum // 2
    return str(carry), res

def sub_bin_strings(a, b):
    """Bit subtraction (a - b) for modules, assumed a >= b."""
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    res = ""
    borrow = 0
    for i in range(max_len - 1, -1, -1):
        diff = int(a[i]) - int(b[i]) - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        res = str(diff) + res
    return res

def invert_bits(b):
    """Bit inversion (0->1, 1->0)."""
    return "".join('1' if bit == '0' else '0' for bit in b)

def get_codes(val, bits=8):
    """Returns the direct, inverse and additional number codes."""
    mag_bin = dec_to_bin_mag(abs(val)).zfill(bits - 1)
    sign = '0' if val >= 0 else '1'
    
    direct = sign + mag_bin
    if val >= 0:
        return direct, direct, direct
    else:
        inverse = sign + invert_bits(mag_bin)
        _, twos_mag = add_bin_strings(invert_bits(mag_bin), "1".zfill(bits - 1))
        twos = sign + twos_mag
        return direct, inverse, twos

def direct_add(d1, d2):
    """Addition in direct code."""
    sign1, mag1 = d1[0], d1[1:]
    sign2, mag2 = d2[0], d2[1:]
    
    if sign1 == sign2:
        _, res_mag = add_bin_strings(mag1, mag2)
        return sign1 + res_mag
    else:
        val1, val2 = bin_to_dec_mag(mag1), bin_to_dec_mag(mag2)
        if val1 >= val2:
            res_mag = sub_bin_strings(mag1, mag2)
            return sign1 + res_mag
        else:
            res_mag = sub_bin_strings(mag2, mag1)
            return sign2 + res_mag

def print_header(title):
    print(f"\n╔{'═'*78}╗")
    print(f"║ {title.center(76)} ║")
    print(f"╚{'═'*78}╝")

def print_step(text):
    print(f" ├─ {text}")



def main():
    X1_dec = 9
    X2_dec = 19
    BITS = 8

    print_header("ОТЧЕТ ПО ЛАБОРАТОРНОЙ РАБОТЕ")
    print(f" Исходные данные: X1 = {X1_dec}, X2 = {X2_dec}")
    print(f" Разрядность сетки: {BITS} бит (1 знаковый + 7 значащих)")

    # === ЗАДАНИЕ 1 ===

    print_header("ЗАДАНИЕ 1. Перевод в двоичную систему и сложение в кодах")
    variants =[
        (X1_dec, X2_dec, "+/+"),
        (X1_dec, -X2_dec, "+/-"),
        (-X1_dec, X2_dec, "-/+"),
        (-X1_dec, -X2_dec, "-/-")
    ]

    for v1, v2, sign_name in variants:
        print(f"\n Вариант ({sign_name}): X1 = {v1}, X2 = {v2}")
        d1, i1, t1 = get_codes(v1, BITS)
        d2, i2, t2 = get_codes(v2, BITS)
        
        print(f"X1 ({v1:>3}): Прямой = {d1} | Обратный = {i1} | Доп. = {t1}")
        print(f"X2 ({v2:>3}): Прямой = {d2} | Обратный = {i2} | Доп. = {t2}")

        # Прямой код
        res_dir = direct_add(d1, d2)
        
        # Обратный код
        c_inv, res_inv = add_bin_strings(i1, i2)
        if c_inv == '1':
            _, res_inv = add_bin_strings(res_inv, "1".zfill(BITS))
            
        # Дополнительный код
        c_twos, res_twos = add_bin_strings(t1, t2)

        # Проверка
        expected = v1 + v2
        exp_d, exp_i, exp_t = get_codes(expected, BITS)

        print(f"Результаты сложения:")
        print(f"Прямой код:       {res_dir} (Ожидалось: {exp_d}) -> {'[ВЕРНО]' if res_dir==exp_d else '[ОШИБКА]'}")
        print(f"Обратный код:     {res_inv} (Ожидалось: {exp_i}) -> {'[ВЕРНО]' if res_inv==exp_i else '[ОШИБКА]'}")
        print(f"Дополнительный:   {res_twos} (Ожидалось: {exp_t}) -> {'[ВЕРНО]' if res_twos==exp_t else '[ОШИБКА]'}")

    # === ЗАДАНИЕ 2 ===

    print_header("ЗАДАНИЕ 2. Умножение модулей чисел")
    mag1 = dec_to_bin_mag(X1_dec)
    mag2 = dec_to_bin_mag(X2_dec)
    
    print_step(f"Модуль |X1| = {X1_dec} (10) = {mag1} (2)")
    print_step(f"Модуль |X2| = {X2_dec} (10) = {mag2} (2)")
    
    # Программное умножение столбиком
    product_bin = "0"
    print("\n   Процесс умножения (сдвиг и сложение):")
    for i, bit in enumerate(reversed(mag2)):
        if bit == '1':
            shifted = mag1 + "0" * i
            print(f"    + {shifted.rjust(10)} (сдвиг на {i})")
            _, product_bin = add_bin_strings(product_bin, shifted)
            
    product_dec = bin_to_dec_mag(product_bin)
    print(f"    ----------------")
    print(f"      {product_bin.rjust(10)} (2) = {product_dec} (10)")
    
    print("\n Определение знаков произведения:")
    print("  (+X1) * (+X2) -> Знак '+' (бит 0)")
    print("  (+X1) * (-X2) -> Знак '-' (бит 1)")
    print("  (-X1) * (+X2) -> Знак '-' (бит 1)")
    print("  (-X1) * (-X2) -> Знак '+' (бит 0)")

    # === ЗАДАНИЕ 3 ===

    print_header("ЗАДАНИЕ 3. Деление модулей чисел")
    print_step(f"Делимое |X1| = {X1_dec} (10) = {mag1} (2)")
    print_step(f"Делитель |X2| = {X2_dec} (10) = {mag2} (2)")
    
    remainder = X1_dec
    divisor = X2_dec
    quotient_bin = ""
    
    print("\n   Процесс деления (получение 5 разрядов после запятой):")
    for i in range(5):
        remainder *= 2
        if remainder >= divisor:
            quotient_bin += "1"
            remainder -= divisor
            print(f"    Шаг {i+1}: Остаток >= Делитель -> пишем 1, новый остаток = {remainder}")
        else:
            quotient_bin += "0"
            print(f"    Шаг {i+1}: Остаток < Делитель  -> пишем 0, остаток = {remainder}")
            
    print(f"\n Результат деления: 0.{quotient_bin} (2)")
    
    # Проверка
    check_dec = 0
    for i, bit in enumerate(quotient_bin):
        if bit == '1':
            check_dec += 2 ** -(i + 1)
            
    print(f" Проверка: 0.{quotient_bin} (2) = {check_dec:.5f} (10)")
    print(f" Точное значение: {X1_dec}/{X2_dec} = {X1_dec/X2_dec:.5f} (10)")

    print("\n Определение знаков частного:")
    print("  (+X1) / (+X2) -> Знак '+' (бит 0)")
    print("  (+X1) / (-X2) -> Знак '-' (бит 1)")
    print("  (-X1) / (+X2) -> Знак '-' (бит 1)")
    print("  (-X1) / (-X2) -> Знак '+' (бит 0)")

    # === ЗАДАНИЕ 4 ===

    print_header("ЗАДАНИЕ 4. Сложение чисел с плавающей точкой")
    
    M1_bin = "0." + mag1
    M2_bin = "0." + mag2
    P1_bin = "0.100"
    P2_bin = "0.101"
    
    P1_dec = bin_to_dec_mag(P1_bin.replace(".", ""))
    P2_dec = bin_to_dec_mag(P2_bin.replace(".", ""))
    
    print_step(f"Число 1: M1 = {M1_bin}, P1 = {P1_bin} (Порядок = {P1_dec})")
    print_step(f"Число 2: M2 = {M2_bin}, P2 = {P2_bin} (Порядок = {P2_dec})")
    
    delta_P = P2_dec - P1_dec
    print(f"\n 1. Выравнивание порядков: ΔP = P2 - P1 = {delta_P}")
    
    # Сдвиг мантиссы
    M1_shifted = "0." + "0" * delta_P + mag1
    print(f" 2. Сдвиг M1 вправо на {delta_P} разряд: M1' = {M1_shifted}")
    
    max_frac_len = max(len(M1_shifted[2:]), len(M2_bin[2:]))
    m1_frac = M1_shifted[2:].ljust(max_frac_len, '0')
    m2_frac = M2_bin[2:].ljust(max_frac_len, '0')
    
    _, sum_frac = add_bin_strings(m1_frac, m2_frac)
    M_res = "0." + sum_frac
    P_res = P2_bin
    
    print(f" 3. Сложение мантисс:")
    print(f"      {M1_shifted.ljust(10)}")
    print(f"    + {M2_bin.ljust(10)}")
    print(f"      {'-'*10}")
    print(f"      {M_res}")
    
    print(f"\n 4. Результат: M_res = {M_res}, P_res = {P_res}")
    
    # Проверка результата
    res_dec_frac = 0
    for i, bit in enumerate(sum_frac):
        if bit == '1':
            res_dec_frac += 2 ** -(i + 1)
            
    final_val = res_dec_frac * (2 ** P2_dec)
    print(f"\n [ПРОВЕРКА] Мантисса {M_res} = {res_dec_frac}")
    print(f" [ПРОВЕРКА] Итоговое значение: {res_dec_frac} * 2^{P2_dec} = {final_val}")
    print(f"[ПРОВЕРКА] Ожидалось: {X1_dec} + {X2_dec} = {X1_dec + X2_dec} -> {'[ВЕРНО]' if final_val == (X1_dec + X2_dec) else '[ОШИБКА]'}")

if __name__ == "__main__":
    main()