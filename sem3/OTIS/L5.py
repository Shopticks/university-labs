import sys


class SequentialComparisonModel:
    def __init__(self):
        self.alternatives = {}

    def add_alternative(self, alt_id, name):
        self.alternatives[alt_id] = {
            'id': alt_id,
            'name': name,
            'scores': [],
            'avg': 0.0
        }

    def add_expert_score(self, alt_id, score):
        if alt_id in self.alternatives:
            self.alternatives[alt_id]['scores'].append(score)

    def calculate_averages(self):
        for alt in self.alternatives.values():
            if alt['scores']:
                alt['avg'] = sum(alt['scores']) / len(alt['scores'])
            else:
                alt['avg'] = 0.0

    def get_sorted_list(self):
        alt_list = list(self.alternatives.values())
        alt_list.sort(key=lambda x: x['avg'], reverse=True)
        return alt_list

    def solve(self, auto_mode=False):
        self.calculate_averages()
        sorted_alts = self.get_sorted_list()

        if not sorted_alts:
            print("Нет данных для анализа.")
            return

        print("\n" + "=" * 70)
        print(f"{'ЭТАП 1: РАНЖИРОВАНИЕ И ПРЕДВАРИТЕЛЬНЫЕ ОЦЕНКИ':^70}")
        print("=" * 70)
        print(f"{'ID':<5} | {'Альтернатива':<35} | {'Предв. оценка (avg)':<20}")
        print("-" * 70)
        for a in sorted_alts:
            print(f"{a['id']:<5} | {a['name']:<35} | {a['avg']:<20.2f}")

        print("\n" + "=" * 70)
        print(f"{'ЭТАП 2: ПОСЛЕДОВАТЕЛЬНЫЕ СРАВНЕНИЯ И КОРРЕКТИРОВКА':^70}")
        print("=" * 70)

        for i in range(len(sorted_alts) - 2):
            current = sorted_alts[i]
            next_1 = sorted_alts[i + 1]
            next_2 = sorted_alts[i + 2]

            sum_next = next_1['avg'] + next_2['avg']

            print(f"\n--- Шаг сравнения {i + 1} ---")
            print(f"Сравниваем лидер: [{current['id']}] (Балл: {current['avg']:.2f})")
            print(f"С суммой:         [{next_1['id']}] + [{next_2['id']}] (Сумма: {sum_next:.2f})")

            if auto_mode:
                print("[Авто-режим] Корректировка пропускается (считаем оценки верными).")
                continue

            while True:
                print(f"\nВОПРОС: Важнее ли цель '{current['name']}' совокупности двух последующих?")
                user_input = input("Введите 'д' (да) или 'н' (нет): ").lower().strip()

                if user_input in ['д', 'y', 'yes', 'да']:
                    if current['avg'] <= sum_next:
                        print(f"\n[!] ТРЕБУЕТСЯ КОРРЕКТИРОВКА!")
                        print(f"Вы сказали 'Да', но {current['avg']:.2f} <= {sum_next:.2f}.")
                        new_val = get_valid_float(
                            f"Введите новое значение для {current['id']} (больше {sum_next:.2f}): ",
                            min_val=sum_next + 0.01
                        )
                        current['avg'] = new_val
                        print(f"Оценка обновлена: {current['avg']}")
                    else:
                        print("Условие выполняется (Оценка > Суммы).")
                    break
                elif user_input in ['н', 'n', 'no', 'нет']:
                    if current['avg'] > sum_next:
                        print(f"\n[!] ТРЕБУЕТСЯ КОРРЕКТИРОВКА!")
                        print(f"Вы сказали 'Нет', но {current['avg']:.2f} > {sum_next:.2f}.")
                        new_val = get_valid_float(
                            f"Введите новое значение для {current['id']} (меньше или равно {sum_next:.2f}): ",
                            max_val=sum_next
                        )
                        current['avg'] = new_val
                        print(f"Оценка обновлена: {current['avg']}")
                    else:
                        print("Условие выполняется (Оценка <= Суммы).")
                    break
                else:
                    print("Ошибка ввода.")

        total_sum = sum(a['avg'] for a in sorted_alts)

        print("\n" + "=" * 75)
        print(f"{'РЕЗУЛЬТАТЫ':^70}")
        print("=" * 75)
        print(f"{'Ранг':<6} | {'ID':<4} | {'Альтернатива':<35} | {'Итог.Балл':<10} | {'Вес (Theta)':<10}")
        print("-" * 75)

        for idx, alt in enumerate(sorted_alts, 1):
            weight = alt['avg'] / total_sum if total_sum > 0 else 0
            print(f"{idx:<6} | {alt['id']:<4} | {alt['name']:<35} | {alt['avg']:<10.2f} | {weight:<10.4f}")

        print("-" * 75)
        if sorted_alts:
            best = sorted_alts[0]
            w = best['avg'] / total_sum if total_sum > 0 else 0
            print(f"\n>>> НАИЛУЧШЕЕ ПРЕДЛОЖЕНИЕ: [{best['id']}] {best['name']}")
            print(f">>> Вес: {w:.4f}")
        print("\n")


def get_valid_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).replace(',', '.'))
            if min_val is not None and val < min_val:
                print(f"Ошибка: Число должно быть >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Ошибка: Число должно быть <= {max_val}")
                continue
            return val
        except ValueError:
            print("Ошибка: Введите число.")


def get_valid_int(prompt, min_val=1):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Ошибка: Число должно быть >= {min_val}")
                continue
            return val
        except ValueError:
            print("Ошибка: Введите целое число.")


def run_test_1():
    print("\n--- ЗАПУСК ТЕСТА 1 (Вариант 11 из задания) ---")
    model = SequentialComparisonModel()
    data = [
        ("Z1", "Собственное производство", 31),
        ("Z2", "Затраты на рекламу", 100),
        ("Z3", "Расширение рынка", 72),
        ("Z4", "Снижение цен", 41)
    ]
    for aid, name, score in data:
        model.add_alternative(aid, name)
        model.add_expert_score(aid, score)

    model.solve(auto_mode=False)


def run_test_2():
    print("\n--- ЗАПУСК ТЕСТА 2 (Пример из методички - Транспорт) ---")
    print("Цели: Z1 (Метро), Z3 (Автобус), Z4 (Трамвай), Z2 (Такси)")
    print("Оценки: 100, 60, 40, 10")
    model = SequentialComparisonModel()

    model.add_alternative("Z1", "Построить метрополитен")
    model.add_expert_score("Z1", 100)

    model.add_alternative("Z3", "Закупить автобусы")
    model.add_expert_score("Z3", 60)

    model.add_alternative("Z4", "Проложить трамвай")
    model.add_expert_score("Z4", 40)

    model.add_alternative("Z2", "Развить такси")
    model.add_expert_score("Z2", 10)

    print("(!) В этом тесте вам будет предложено скорректировать оценку Z1.")
    model.solve(auto_mode=False)


def run_test_3():
    print("\n--- ЗАПУСК ТЕСТА 3 (Выбор языка программирования) ---")
    print("Симуляция 2 экспертов.")
    model = SequentialComparisonModel()

    model.add_alternative("L1", "Python")
    model.add_alternative("L2", "C++")
    model.add_alternative("L3", "Java")

    model.add_expert_score("L1", 90)
    model.add_expert_score("L2", 60)
    model.add_expert_score("L3", 70)

    model.add_expert_score("L1", 95)
    model.add_expert_score("L2", 50)
    model.add_expert_score("L3", 80)

    model.solve(auto_mode=True)


def run_manual_mode():
    print("\n--- РУЧНОЙ ВВОД ДАННЫХ ---")
    model = SequentialComparisonModel()

    num_alts = get_valid_int("Введите количество альтернатив (минимум 3): ", min_val=3)

    alt_ids = []
    for i in range(num_alts):
        aid = f"Z{i + 1}"
        while True:
            name = input(f"Название альтернативы {aid}: ").strip()
            if name:
                break
            print("Название не может быть пустым.")
        model.add_alternative(aid, name)
        alt_ids.append(aid)

    while True:
        print("\n--- Добавление эксперта ---")
        for aid in alt_ids:
            name = model.alternatives[aid]['name']
            score = get_valid_float(f"Оценка для '{name}' ({aid}): ", min_val=0)
            model.add_expert_score(aid, score)

        cont = input("Добавить еще одного эксперта? (д/н): ").lower()
        if cont not in ['д', 'y', 'yes', 'да']:
            break

    model.solve(auto_mode=False)


def main():
    while True:
        print("\n" + "=" * 30)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 30)
        print("1. Ручной ввод (Эксперты + Альтернативы)")
        print("2. Тест 1 (Вариант 11 - Компания 'Проспект')")
        print("3. Тест 2 (Пример из методички - Транспорт)")
        print("4. Тест 3 (IT - Выбор языка, 2 эксперта)")
        print("0. Выход")

        choice = input("Выберите пункт: ").strip()

        if choice == '1':
            run_manual_mode()
        elif choice == '2':
            run_test_1()
        elif choice == '3':
            run_test_2()
        elif choice == '4':
            run_test_3()
        elif choice == '0':
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()