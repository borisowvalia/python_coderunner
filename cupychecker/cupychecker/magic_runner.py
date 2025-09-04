from IPython.core.magic import register_cell_magic
from IPython.display import HTML, display, Markdown
import argparse
import shlex
import os

from .checker import run_code, check_result


@register_cell_magic
def run(line, cell):
    # Парсим неделю и номер задачи
    args_list = shlex.split(line)
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', type=int, required=True)
    parser.add_argument('--task', type=int, required=True)
    parser.add_argument('--plot', action=argparse.BooleanOptionalAction)

    if os.getenv('PYRUNNER'):
        pyrunner_default_host = os.getenv('PYRUNNER')
    else:
        pyrunner_default_host = 'http://localhost:8000/run'

    parser.add_argument('--pyrunner', type=str, required=False, default=pyrunner_default_host)
    args = parser.parse_args(args_list)
    print(args, end='\n')

    runner_result = run_code(code=cell, host=args.pyrunner)

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
        checker_result = check_result(
            code=cell,
            stdout=runner_result.get('stdout'),
            module=args.module,
            task=args.task
        )

        if args.plot:
            exec(cell)
        else:
            display(Markdown(f'```\n{runner_result.get('stdout')}\n```'))

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
