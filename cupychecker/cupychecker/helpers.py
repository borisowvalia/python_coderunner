import ast


class TestHelper():
    def __init__(self, code: str, stdout: str):
        self.code = code
        self.stdout = stdout

    def var(self, var_name: str, expected_value, msg=None):
        """
        Проверяет, что в переданном Python-коде переменной `var_name` присвоено ожидаемое значение `expected_value`.

        Функция парсит код с помощью модуля `ast`, ищет все присваивания переменной
        `var_name` и проверяет соответствие последнего присвоенного значения ожидаемому.
        Пробелы удаляются перед сравнением.

        Args:
            code (str):
                Строка с Python-кодом, который будет анализироваться.
            var_name (str):
                Имя переменной, значение которой нужно проверить.
            expected_value (any):
                Ожидаемое значение переменной. Может быть числом, строкой, списком и т.д.
                Для строк пробелы игнорируются при сравнении.
            msg (str, optional):
                Сообщение об ошибке, которое будет возвращено, если значение переменной
                не соответствует ожидаемому. Если None (по умолчанию), формируется
                стандартное сообщение.

        Returns:
            bool | str | SyntaxError:
                * True — если переменной присвоено ожидаемое значение.
                * str — сообщение об ошибке, если переменная не объявлена или
                  её значение не соответствует ожидаемому.
                * SyntaxError — если переданный код содержит синтаксическую ошибку.

        Examples:
            >>> var("x = 10", "x", 10)
            True

            >>> var("x = 1\\nx = 2", "x", 1)
            'Переменной `x` было переписвоено значение 2, ожидалось 1'

            >>> var("y = 'hello'", "z", "hello")
            'Переменная `z` не объявлена'

            >>> var("x = pd.DataFrame([1,2,3])", "x", "pd.DataFrame([1,2,3])")
            True
        """

        try:
            tree = ast.parse(self.code)
        except SyntaxError as err:
            return err

        assignments = {}

        # Парсим переменную
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == var_name:
                        try:
                            assignments[var_name] = ast.literal_eval(node.value)   
                            if isinstance(assignments[var_name], str):
                                assignments[var_name] = assignments[var_name].replace(" ", "")
                        except Exception:
                            assignments[var_name] = ast.unparse(node.value).replace(" ", "")

        # print(assignments.get(var_name, None))

        # Готовим expected
        if isinstance(expected_value, str):
            strip_expected_value = expected_value.replace(" ", "")
        else:
            strip_expected_value = expected_value

        if var_name not in assignments:
            return f"Переменная `{var_name}` не объявлена"
        if assignments[var_name] != strip_expected_value:
            return msg or f"Переменной `{var_name}` было переписвоено значение {assignments[var_name]}, ожидалось {expected_value}"
        else:
            return True

    def call(self, func_name: str, expected_args=None, msg=None):
        """
        Проверяет, что в переданном коде есть вызов указанной функции
        с ожидаемыми позиционными и/или именованными аргументами.

        Функция разбирает Python-код с помощью модуля `ast`, ищет последний вызов функции,
        сравнивает фактические аргументы вызова с ожидаемыми и возвращает
        результат проверки.

        Args:
            code (str):
                Строка с Python-кодом, который будет анализироваться.
            func_name (str):
                Имя функции, вызов которой нужно проверить.
            expected_args (list | None, optional):
                Список ожидаемых аргументов. Может содержать:
                    * строковые литералы или выражения для позиционных аргументов,
                    * кортежи вида (имя_аргумента, значение) для именованных аргументов,
                    * числа и другие литералы.
                Пробелы внутри строк удаляются автоматически.
                Если None (по умолчанию), то проверяется только сам факт вызова функции.
            msg (str | None, optional):
                Сообщение об ошибке, которое будет возвращено в случае
                несоответствия. Если None (по умолчанию), формируется стандартное сообщение.

        Returns:
            bool | str | SyntaxError:
                * True — если функция вызвана с ожидаемыми аргументами
                  (или если `expected_args` не переданы и вызов найден).
                * str — сообщение об ошибке (если функция не найдена или аргументы не совпадают).
                * SyntaxError — если переданный код содержит синтаксическую ошибку.

        Examples:
            >>> call("print(123, sep='\\t')", "print", [123, ("sep", "\\t")])
            True

            >>> call("print(123)", "print", [123, ("sep", "\\t")])
            'Функция `print` вызвана с аргументами [123], ожидаются [123, ("sep", "\\t")]'

            >>> call("x = 1", "print")
            'Не найден вызов функции `print`'

            >>> call("print(123, end=var)", "print", [("end", "var")])
            True
        """

        try:
            tree = ast.parse(self.code)
        except SyntaxError as err:
            return err

        assignments = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                else:
                    name = None

                if name == func_name:
                    assignments[func_name] = node

        if func_name not in assignments:
            return msg or f"Не найден вызов функции `{func_name}`" 
        elif func_name in assignments and expected_args is None:
            return True
        elif func_name in assignments and expected_args is not None:
            call_kwargs = []
            call_args = []
            node = assignments[func_name]

            # Позиционные аргументы
            for arg in node.args:
                try:
                    value = ast.literal_eval(arg)  # пробуем как литерал
                    if not (isinstance(value, int) or isinstance(value, float)):
                        value = value.replace(" ", "")
                except Exception:
                    value = ast.unparse(arg).replace(" ", "")  # иначе оставляем как код
                call_kwargs.append(value)
            # Именованные аргументы
            for kw in node.keywords:
                try:
                    value = ast.literal_eval(kw.value)
                    if not (isinstance(value, int) or isinstance(value, float)):
                        value = value.replace(" ", "")
                except Exception:
                    value = ast.unparse(kw.value).replace(" ", "")
                call_kwargs.append((kw.arg, value))

            # Готовим expected
            strip_expected_args = []
            for arg in expected_args:
                if isinstance(arg, str):
                    strip_expected_args.append(arg.replace(" ", ""))
                elif isinstance(arg, list):
                    if isinstance(arg[1], str):
                        strip_expected_args.append((arg[0], arg[1].replace(" ", "")))
                    else:
                        strip_expected_args.append((arg[0], arg[1]))
                else:
                    strip_expected_args.append(arg)

            # print(call_args + call_kwargs)
            # print(strip_expected_args)

            if set(strip_expected_args).issubset(set(call_args + call_kwargs)):
                return True
            else:
                return msg or f"Функция `{func_name}` вызвана с аргументами {call_args + call_kwargs}, ожидаются {expected_args}"

    def output(self, expected_output: str, include=None, msg=None):
        """
        Проверяет, что строковый вывод функции соответствует ожидаемому.
        Предназначено для проверки вывода после print().

        Args:
            actual_output (str): Строка, полученная после print().
            expected_output (str): Ожидаемый вывод в виде строки.
            include (bool, optional): Условие на строгое соотвествие вывода или частичное включение
            msg (str, optional): Сообщение об ошибке, если вывод отличается.

        Returns:
            bool | str: True, если вывод совпадает; иначе сообщение об ошибке.
        """
        actual_str = "\n".join([line.strip() for line in self.stdout.splitlines() if line.strip()])
        expected_str = "\n".join([line.strip() for line in expected_output.splitlines() if line.strip()])

        if actual_str == expected_str and include is None:
            return True
        elif expected_str in actual_str and include is True:
            return True
        else:
            return msg or f"Фактический вывод: {actual_str}, ожидается: {expected_str}"

    def contains(self, expected_code: str, msg: str = None):
        """
        Проверяет, что в коде студента есть определённая подстрока
        """
        actual_str = "\n".join([line.strip() for line in self.code.splitlines() if line.strip()]).replace(" ", "").replace("\"", "'")
        expected_str = "\n".join([line.strip() for line in expected_code.splitlines() if line.strip()]).replace(" ", "").replace("\"", "'")

        if expected_str not in actual_str:
            return msg or f"Ожидается {expected_code}"

        return True
