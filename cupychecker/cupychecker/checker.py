import requests

from .task_loader import load
from .helpers import TestHelper


def check_result(code: str, stdout: str, module: int, task: int):
    task_config = load(module=module, task=task)
    _test = TestHelper(code=code, stdout=stdout)

    for check in task_config.get('checks'):
        if 'message' in check:
            message = check['message']
        else:
            message = None

        if check['type'] == 'var':
            result = _test.var(
                var_name=check['expected']['var'],
                expected_value=check['expected']['value'],
                msg=message
            )

        if check['type'] == "call":
            if 'args' in check['expected']:
                expected_args = check['expected']['args']
            else:
                expected_args = None
            result = _test.call(
                func_name=check['expected']['func'],
                expected_args=expected_args,
                msg=message
            )

        elif check['type'] == "output":
            if 'include' in check['expected']:
                include = check['expected']['include']
            else:
                include = None
            result = _test.output(
                expected_output=check['expected']['stdout'],
                include=include,
                msg=message
            )

        elif check['type'] == "contains":
            result = _test.contains(
                expected_code=check['expected']['code'],
                msg=message
            )

        if result is not True:
            return result

    return True


def run_code(code, host='http://localhost:8000/run'):
    response = requests.post(
        host,
        json={
            'code': f'{code}'
        }
    )
    response.raise_for_status()

    return response.json()


def check(code: str, module: int, task: int, host='http://localhost:8000/run'):
    runner_result = run_code(code=code, host=host)
    return check_result(
        code,
        runner_result.get('stdout'),
        module=module,
        task=task
    )
