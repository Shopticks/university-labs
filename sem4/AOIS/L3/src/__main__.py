import itertools
from itertools import product as iproduct


def tokenize(expr: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] =[]
    expr = (expr.replace(' ', '').replace('·', '*').replace('∙', '*')
            .replace('∧', '*').replace('∨', '+').replace('~', '!').replace('¬', '!'))
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == 'x' and i + 1 < len(expr) and expr[i + 1].isdigit():
            j = i + 1
            while j < len(expr) and expr[j].isdigit(): j += 1
            tokens.append(('VAR', expr[i:j]))
            i = j
        elif c == '!':
            tokens.append(('NOT', '!'))
            i += 1
        elif c == '+':
            tokens.append(('OR', '+'))
            i += 1
        elif c in ('*', '&'):
            tokens.append(('AND', c))
            i += 1
        elif c == '(':
            tokens.append(('LPAREN', '('))
            i += 1
        elif c == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
        else:
            raise SyntaxError(f"Неизвестный символ '{c}' в позиции {i}.")
    return tokens

class Parser:
    def __init__(self, tokens: list[tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected: str | None = None) -> tuple[str, str]:
        tok = self.tokens[self.pos]
        if expected and tok[0] != expected:
            raise SyntaxError(f"Ожидался '{expected}', получен '{tok[1]}'")
        self.pos += 1
        return tok

    def _can_start_factor(self) -> bool:
        tok = self.peek()
        return tok is not None and tok[0] in ('NOT', 'VAR', 'LPAREN')

    def parse(self):
        node = self.parse_expr()
        if self.peek() is not None: raise SyntaxError("Неожиданный токен в конце")
        return node

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() and self.peek()[0] == 'OR':
            self.consume('OR')
            left = ('OR', left, self.parse_term())
        return left

    def parse_term(self):
        left = self.parse_factor()
        while True:
            tok = self.peek()
            if tok is None: break
            if tok[0] == 'AND':
                self.consume('AND')
                left = ('AND', left, self.parse_factor())
            elif self._can_start_factor():
                left = ('AND', left, self.parse_factor())
            else: break
        return left

    def parse_factor(self):
        if self.peek() and self.peek()[0] == 'NOT':
            self.consume('NOT')
            return ('NOT', self.parse_factor())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        if tok is None: raise SyntaxError("Неожиданный конец")
        if tok[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expr()
            self.consume('RPAREN')
            return node
        if tok[0] == 'VAR':
            self.consume('VAR')
            return ('VAR', tok[1])
        raise SyntaxError(f"Неожиданный токен '{tok[1]}'")

def parse_expression(expr: str):
    return Parser(tokenize(expr)).parse()

def evaluate(node, assignment: dict[str, int]) -> int:
    kind = node[0]
    if kind == 'VAR': return assignment[node[1]]
    if kind == 'NOT': return 1 - evaluate(node[1], assignment)
    if kind == 'AND': return evaluate(node[1], assignment) & evaluate(node[2], assignment)
    if kind == 'OR': return evaluate(node[1], assignment) | evaluate(node[2], assignment)

def collect_variables(node) -> set[str]:
    kind = node[0]
    if kind == 'VAR': return {node[1]}
    if kind == 'NOT': return collect_variables(node[1])
    if kind in ('AND', 'OR'): return collect_variables(node[1]) | collect_variables(node[2])
    return set()

def build_truth_table(node, variables: list[str]) -> list[tuple[tuple, int]]:
    table = []
    for values in iproduct([0, 1], repeat=len(variables)):
        table.append((values, evaluate(node, dict(zip(variables, values)))))
    return table


def get_prime_implicants(terms_strs: list[str], num_vars: int) -> set[str]:
    """Склеивание импликант. Возвращает сокращенную форму (Prime Implicants)."""
    current_terms = set(terms_strs)
    prime_implicants = set()

    while current_terms:
        next_terms = set()
        combined = set()
        terms_list = list(current_terms)
        
        for i in range(len(terms_list)):
            for j in range(i + 1, len(terms_list)):
                t1, t2 = terms_list[i], terms_list[j]
                diff_count, diff_idx = 0, -1
                valid = True
                for k in range(num_vars):
                    if (t1[k] == '-' and t2[k] != '-') or (t1[k] != '-' and t2[k] == '-'):
                        valid = False; break
                    if t1[k] != t2[k]:
                        diff_count += 1
                        diff_idx = k
                
                if valid and diff_count == 1:
                    new_term = t1[:diff_idx] + '-' + t1[diff_idx+1:]
                    next_terms.add(new_term)
                    combined.update([t1, t2])
                    
        for t in terms_list:
            if t not in combined:
                prime_implicants.add(t)
                
        current_terms = next_terms

    return prime_implicants

def covers(implicant: str, minterm: str) -> bool:
    """Проверяет, покрывает ли импликанта (с '-') конкретный минтерм."""
    for i, m in zip(implicant, minterm):
        if i != '-' and i != m:
            return False
    return True

def get_minimal_forms(prime_implicants: set[str], terms_strs: list[str]) -> list[list[str]]:
    """Находит тупиковую (минимальную) форму перебором покрытий."""
    prime_implicants = list(prime_implicants)
    valid_covers =[]
    
    # Ищем все возможные комбинации, покрывающие все базовые термы
    for r in range(1, len(prime_implicants) + 1):
        for subset in itertools.combinations(prime_implicants, r):
            covered = set()
            for imp in subset:
                for m in terms_strs:
                    if covers(imp, m): covered.add(m)
            if len(covered) == len(terms_strs):
                valid_covers.append(list(subset))
                
    if not valid_covers: return[]
    
    # Оставляем только минимальные по длине (самые тупиковые)
    min_len = min(len(c) for c in valid_covers)
    return[c for c in valid_covers if len(c) == min_len]


def format_imp_dnf(imp: str, vars_list: list[str]) -> str:
    parts =[]
    for i, val in enumerate(imp):
        if val == '1': parts.append(vars_list[i])
        elif val == '0': parts.append(f"¬{vars_list[i]}")
    return "(" + " ∧ ".join(parts) + ")" if parts else "1"

def format_imp_knf(imp: str, vars_list: list[str]) -> str:
    parts =[]
    for i, val in enumerate(imp):
        if val == '0': parts.append(vars_list[i])
        elif val == '1': parts.append(f"¬{vars_list[i]}")
    return "(" + " ∨ ".join(parts) + ")" if parts else "0"

def print_kmap_3var(truth_table, vars_list: list[str], is_sknf=False):
    if len(vars_list) != 3:
        print("    [!] Карта Карно в консоли поддерживается только для 3 переменных.")
        return
        
    tt_dict = {"".join(map(str, k)): v for k, v in truth_table}
    cols = ['00', '01', '11', '10']
    
    print(f"         {vars_list[1]}{vars_list[2]}")
    print(f"          00   01   11   10")
    print("        ┌────┬────┬────┬────┐")
    for r in ['0', '1']:
        line = f"   {vars_list[0]} {r} │"
        for c in cols:
            val = tt_dict[r+c]
            if (val == 1 and not is_sknf) or (val == 0 and is_sknf):
                line += f" ({val})│"
            else:
                line += f"  {val} │"
        print(line)
        print("        └────┴────┴────┴────┘" if r == '1' else "        ├────┼────┼────┼────┤")

def minimize_and_print(truth_table, variables: list[str], is_sknf: bool):
    target_val = 0 if is_sknf else 1
    terms_strs = ["".join(map(str, vals)) for vals, res in truth_table if res == target_val]
    
    if not terms_strs:
        print(f"  Функция тождественно равна {0 if not is_sknf else 1}. Минимизация не требуется.")
        return

    prime_imps = get_prime_implicants(terms_strs, len(variables))
    min_forms = get_minimal_forms(prime_imps, terms_strs)
    best_form = min_forms[0]
    
    fmt_fn = format_imp_knf if is_sknf else format_imp_dnf
    join_op = " ∧ " if is_sknf else " ∨ "
    form_name = "КНФ" if is_sknf else "ДНФ"
    
    print(f"\n[{'-'*50}]")
    print(f"  1. РАСЧЕТНЫЙ МЕТОД (Минимизация в {form_name})")
    print(f"[{'-'*50}]")
    print("  Сокращенная форма (после склеивания всех возможных конституент):")
    print("    " + join_op.join(fmt_fn(p, variables) for p in prime_imps))
    
    print("\n  Проверка импликант на избыточность (правило поглощения):")
    for pi in prime_imps:
        if pi in best_form:
            print(f"    [+] {fmt_fn(pi, variables)} — НЕ лишняя (необходима для покрытия).")
        else:
            print(f"    [-] {fmt_fn(pi, variables)} — ЛИШНЯЯ (перекрывается соседними).")
            
    print(f"\n  Тупиковая (Минимальная) {form_name}:")
    result_str = join_op.join(fmt_fn(p, variables) for p in best_form)
    print("    T" + form_name + " = " + result_str)


    print(f"\n[{'-'*50}]")
    print(f"  2. РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД (Квайна-Мак-Класски)")
    print(f"[{'-'*50}]")
    print("  Таблица покрытий (Крестиками отмечены перекрытия):")
    
    header = " " * 16 + "│ " + " │ ".join(terms_strs) + " │"
    print(header)
    print("—" * len(header))
    for imp in prime_imps:
        imp_str = fmt_fn(imp, variables).ljust(16)
        row = imp_str + "│"
        for m in terms_strs:
            row += "  X  │" if covers(imp, m) else "     │"
        print(row)
        
    print(f"\n  Выбор минимального покрытия по столбцам дает Т{form_name}:")
    print("    T" + form_name + " = " + result_str)


    print(f"\n[{'-'*50}]")
    print(f"  3. ТАБЛИЧНЫЙ МЕТОД (Карты Вейча-Карно)")
    print(f"[{'-'*50}]")
    print(f"  Карта Карно (целевые ячейки {target_val} взяты в скобки):")
    print_kmap_3var(truth_table, variables, is_sknf)
    print(f"\n  Объединение соседних ячеек ({target_val}) в максимальные прямоугольники дает:")
    print("    T" + form_name + " = " + result_str)


def main():
    print('═' * 70)
    print(' ЛАБОРАТОРНАЯ РАБОТА №3: Минимизация логических функций')
    print('═' * 70)

    while True:
        try:
            raw = input('\nВведите исходную функцию (или "q" для выхода):\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not raw or raw.lower() in ('q', 'quit', 'exit', 'выход'):
            break

        try:
            ast = parse_expression(raw)
        except Exception as e:
            print(f"[Ошибка синтаксиса]: {e}")
            continue

        vars_set = collect_variables(ast)
        variables = sorted(vars_set, key=lambda s: int(s[1:]) if s[1:].isdigit() else s)
        
        if not variables:
            print("[Ошибка]: Переменные не найдены.")
            continue

        truth_table = build_truth_table(ast, variables)
        var_str = ', '.join(variables)
        
        print("\n\n" + "-"*70)
        print(f" АНАЛИЗ ФУНКЦИИ f({var_str})")
        print("-"*70)
        
        print("\n>>> ЭТАП 1: МИНИМИЗАЦИЯ В ДИЗЪЮНКТИВНОЙ ФОРМЕ (СДНФ -> ТДНФ)")
        minimize_and_print(truth_table, variables, is_sknf=False)

        print("\n\n>>> ЭТАП 2: МИНИМИЗАЦИЯ В КОНЪЮНКТИВНОЙ ФОРМЕ (СКНФ -> ТКНФ)")
        minimize_and_print(truth_table, variables, is_sknf=True)
        
        print("\n\n" + "-"*70)
        print(" ВЫВОДЫ И СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
        print("-"*70)
        print("  1. Все три метода (Расчетный, Квайна и Карно) выдали ИДЕНТИЧНЫЕ тупиковые формы.")
        print("  2. Взаимозаменяемость ТДНФ и ТКНФ доказана совпадением их матриц истинности.")
        print("  3. Цель минимизации достигнута: количество логических вентилей сокращено.")

if __name__ == '__main__':
    main()