from IPython.core.magic import register_cell_magic
from IPython.display import HTML, display, Markdown
import argparse
import shlex
import os

from .checker import run_code, check_result


@register_cell_magic
def run(line, cell):
    # Пытаемся понять где живет runner для запуска кода и хранения проверок
    if os.getenv('PYRUNNER'):
        pyrunner_default_host = os.getenv('PYRUNNER')
    else:
        pyrunner_default_host = 'http://localhost:8000'

    # Парсим неделю и номер задачи
    args_list = shlex.split(line)
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', type=str, required=True)
    parser.add_argument('--task', type=str, required=True)
    parser.add_argument('--plot', action=argparse.BooleanOptionalAction)
    parser.add_argument('--pyrunner', type=str, required=False, default=pyrunner_default_host)

    args = parser.parse_args(args_list)
    print(args, end='\n')

    # Запускаем код
    runner_result = run_code(code=cell, host=args.pyrunner)

    # Выкидываем ошибку клиенту
    if runner_result.get('stderr') != '':
        return HTML(f"""
        <div style="
            background-color:#f8d7da;
            color:#721c24;
            border:1px solid #f5c6cb;
            border-radius:8px;
            padding:12px 16px;
            font-family:Arial;
            font-size:16px;
            font-weight:bold;">
            ❌ Ошибка: {runner_result.get('stderr')}
        </div>
        """)
    else:
        # Делаем проверки рехультата
        checker_result = check_result(
            code=cell,
            stdout=runner_result.get('stdout'),
            module=args.module,
            task=args.task,
            host=args.pyrunner # Отсюда заберем yaml проверок
        )

        # Выводим stdout
        # Если указан plot, то дополнительно строим график
        if args.plot:
            exec(cell)
        else:
            display(Markdown(f'```\n{runner_result.get('stdout')}\n```'))

        # Если не прошли прверку, то сообщение об ошибке
        if checker_result is not True:
            return HTML(f"""
            <div style="
                background-color:#f8d7da;
                color:#721c24;
                border:1px solid #f5c6cb;
                border-radius:8px;
                padding:12px 16px;
                font-family:Arial;
                font-size:16px;
                font-weight:bold;">
                ❌ Ошибка: {checker_result}
            </div>
            """)
        # Иначе успех
        else:
            return HTML("""
        <div style="
            background-color:#d4edda;
            color:#155724;
            border:1px solid #c3e6cb;
            border-radius:8px;
            padding:12px 16px;
            font-family:Arial;
            font-size:16px;
            font-weight:bold;">
            ✅ Проверка пройдена успешно!
        </div>
        """)
