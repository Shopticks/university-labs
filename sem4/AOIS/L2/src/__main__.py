from itertools import product as iproduct


def tokenize(expr: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] =[]

    expr = (expr
            .replace(' ', '')
            .replace('·', '*')
            .replace('∙', '*')
            .replace('∧', '*')
            .replace('∨', '+')
            .replace('~', '!')
            .replace('¬', '!'))

    i = 0
    while i < len(expr):
        c = expr[i]


        if c == 'x' and i + 1 < len(expr) and expr[i + 1].isdigit():
            j = i + 1
            while j < len(expr) and expr[j].isdigit():
                j += 1
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
            raise SyntaxError(
                f"Неизвестный символ '{c}' в позиции {i}.\n"
                "Используйте x1..xN для переменных, ! для отрицания, "
                "+ для ИЛИ, * для И, () для группировки."
            )

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
        if self.peek() is not None:
            raise SyntaxError(f"Неожиданный токен '{self.peek()[1]}' в конце выражения")
        return node

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() and self.peek()[0] == 'OR':
            self.consume('OR')
            right = self.parse_term()
            left = ('OR', left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while True:
            tok = self.peek()
            if tok is None:
                break
            if tok[0] == 'AND':
                self.consume('AND')
                left = ('AND', left, self.parse_factor())
            elif self._can_start_factor():
                left = ('AND', left, self.parse_factor())
            else:
                break
        return left

    def parse_factor(self):
        if self.peek() and self.peek()[0] == 'NOT':
            self.consume('NOT')
            return ('NOT', self.parse_factor())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        if tok is None:
            raise SyntaxError("Неожиданный конец выражения")
        if tok[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expr()
            if self.peek() is None or self.peek()[0] != 'RPAREN':
                raise SyntaxError("Отсутствует закрывающая скобка ')'")
            self.consume('RPAREN')
            return node
        if tok[0] == 'VAR':
            self.consume('VAR')
            return ('VAR', tok[1])
        raise SyntaxError(f"Неожиданный токен '{tok[1]}'")


def parse_expression(expr: str):
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Пустое выражение")
    return Parser(tokens).parse()


def evaluate(node, assignment: dict[str, int]) -> int:
    kind = node[0]
    if kind == 'VAR':
        name = node[1]
        if name not in assignment:
            raise ValueError(f"Переменная '{name}' отсутствует в наборе")
        return assignment[name]
    if kind == 'NOT':
        return 1 - evaluate(node[1], assignment)
    if kind == 'AND':
        return evaluate(node[1], assignment) & evaluate(node[2], assignment)
    if kind == 'OR':
        return evaluate(node[1], assignment) | evaluate(node[2], assignment)
    raise ValueError(f"Неизвестный тип узла АСД: {kind}")


def collect_variables(node) -> set[str]:
    kind = node[0]
    if kind == 'VAR':
        return {node[1]}
    if kind == 'NOT':
        return collect_variables(node[1])
    if kind in ('AND', 'OR'):
        return collect_variables(node[1]) | collect_variables(node[2])
    return set()


def build_truth_table(node, variables: list[str]) -> list[tuple[tuple, int]]:
    table: list[tuple[tuple, int]] = []
    for values in iproduct([0, 1], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        result = evaluate(node, assignment)
        table.append((values, result))
    return table


def _fmt_conjunction(values, variables: list[str]) -> str:
    parts =[f'¬{v}' if val == 0 else v for v, val in zip(variables, values)]
    return '(' + ' ∧ '.join(parts) + ')'

def _fmt_disjunction(values, variables: list[str]) -> str:
    parts =[f'¬{v}' if val == 1 else v for v, val in zip(variables, values)]
    return '(' + ' ∨ '.join(parts) + ')'

def compute_sdnf(truth_table, variables: list[str]) -> tuple[list[int], list[str]]:
    minterms, terms = [],[]
    for values, result in truth_table:
        if result == 1:
            minterms.append(int(''.join(map(str, values)), 2))
            terms.append(_fmt_conjunction(values, variables))
    return minterms, terms

def compute_sknf(truth_table, variables: list[str]) -> tuple[list[int], list[str]]:
    maxterms, terms = [],[]
    for values, result in truth_table:
        if result == 0:
            maxterms.append(int(''.join(map(str, values)), 2))
            terms.append(_fmt_disjunction(values, variables))
    return maxterms, terms

def compute_index(truth_table) -> int:
    return int(''.join(str(r) for _, r in truth_table), 2)


def print_truth_table(truth_table, variables: list[str], index: int) -> None:
    col_w = max(len(v) for v in variables) + 2
    f_label = f'f{index}'
    
    header = '  №  | ' + ' | '.join(f'{v:^{col_w}}' for v in variables) + f' | {f_label:^{max(3, len(f_label))}} | Вес разряда'
    sep = '-' * len(header)
    print(sep)
    print(header)
    print(sep)
    
    num_rows = len(truth_table)
    
    for j, (values, result) in enumerate(truth_table):
        weight = 2 ** (num_rows - 1 - j)
        
        row = f' {j:>3} | '
        row += ' | '.join(f'{v:^{col_w}}' for v in values)
        row += f' | {result:^{max(3, len(f_label))}} | {weight:^11}'
        print(row)
    print(sep)


def print_results(
    expr_input: str,
    variables: list[str],
    truth_table,
    sdnf_terms: list[str],
    sknf_terms: list[str],
    minterms: list[int],
    maxterms: list[int],
    index: int
) -> None:
    func_name = f'F{index}'
    var_str = ', '.join(variables)

    print('\n' + '═' * 64)
    print(f'  Исходная функция : {expr_input}')
    print(f'  Переменные       : {var_str}  (n = {len(variables)})')
    print('═' * 64)

    print('\n[ Таблица истинности ]')
    print_truth_table(truth_table, variables, index)

    print(f'\n[ Индекс функции ]')
    print(f'  i = {index}  (двоичное: {index:0{2 ** len(variables)}b})')

    print(f'\n[ СДНФ — Совершенная Дизъюнктивная Нормальная Форма ]')
    if sdnf_terms:
        print(f'  СДНФ({var_str}) =')
        chunk = 4
        for i in range(0, len(sdnf_terms), chunk):
            prefix = '    = ' if i == 0 else '      '
            suffix = ' ∨' if i + chunk < len(sdnf_terms) else ''
            print(prefix + ' ∨ '.join(sdnf_terms[i:i + chunk]) + suffix)
    else:
        print(f'  СДНФ = 0  (функция тождественно ЛОЖНА)')

    print(f'\n[ СКНФ — Совершенная Конъюнктивная Нормальная Форма ]')
    if sknf_terms:
        print(f'  СКНФ({var_str}) =')
        chunk = 4
        for i in range(0, len(sknf_terms), chunk):
            prefix = '    = ' if i == 0 else '      '
            suffix = ' ∧' if i + chunk < len(sknf_terms) else ''
            print(prefix + ' ∧ '.join(sknf_terms[i:i + chunk]) + suffix)
    else:
        print(f'  СКНФ = 1  (функция тождественно ИСТИННА)')

    print(f'\n[ Числовая форма ]')
    v_part = 'V(' + ','.join(map(str, minterms)) + ')' if minterms else 'V(∅)'
    l_part = 'Λ(' + ','.join(map(str, maxterms)) + ')' if maxterms else 'Λ(∅)'
    print(f'  ({var_str}) = {v_part} = {l_part}')
    print()

    


HELP_TEXT = """
┌─────────────────────────────────────────────────────────────┐
│       Синтаксис ввода логической функции                    │
├─────────────────────────────────────────────────────────────┤
│  Переменные : x1, x2, x3 (или xN для любого N)              │
│  Отрицание  : !x1   или   !(выражение)                      │
│  И  (AND)   : *  или  &  или пробел (неявное И)             │
│  ИЛИ (OR)   : +                                             │
│  Скобки     : ( )                                           │
├─────────────────────────────────────────────────────────────┤
│  Примеры вариантов из лабораторной работы:                  │
│  Вар.02: !(!x1 + !x2) * !x1 * x3                            │
│  Вар.06: !(x1 + !x2) * !(!x1 * x3)      ← общее отрицание   │
│  Вар.10: !(!x1 + !x2) * !x2 * x3                            │
│  Вар.11: !( !x1 + x2 ) * !( x2 * !x3 )                      │
│  Вар.20: (x2 + x3) * !x1 * x3                               │
└─────────────────────────────────────────────────────────────┘
"""


def main() -> None:
    print('═' * 64)
    print('   Лабораторная работа №2')
    print('   Преобразование логических функций в СДНФ и СКНФ')
    print('═' * 64)
    print(HELP_TEXT)

    while True:
        try:
            raw = input('Введите функцию (или "exit" для выхода):\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nВыход.')
            break

        if not raw:
            continue
        if raw.lower() in ('exit', 'quit', 'выход', 'q'):
            print('Выход.')
            break

        try:
            ast = parse_expression(raw)
        except (SyntaxError, ValueError) as e:
            print(f'\n[Ошибка парсинга] {e}\n')
            continue

        vars_set = collect_variables(ast)
        if not vars_set:
            print('[Ошибка] Переменные не найдены.\n')
            continue

        variables = sorted(vars_set, key=lambda s: int(s[1:]))

        truth_table = build_truth_table(ast, variables)
        minterms, sdnf_terms = compute_sdnf(truth_table, variables)
        maxterms, sknf_terms = compute_sknf(truth_table, variables)
        index = compute_index(truth_table)

        print_results(
            expr_input=raw,
            variables=variables,
            truth_table=truth_table,
            sdnf_terms=sdnf_terms,
            sknf_terms=sknf_terms,
            minterms=minterms,
            maxterms=maxterms,
            index=index,
        )


if __name__ == '__main__':
    main()