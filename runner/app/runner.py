import subprocess
import asyncio
from tempfile import TemporaryDirectory
import os

from models import RunPythonResponse


MAX_STDOUT_SIZE = os.getenv('RUNNER__MAX_STDOUT_SIZE', 1000)
MAX_STDERR_SIZE = os.getenv('RUNNER__MAX_STDERR_SIZE', 1000)
TIMEOUT = os.getenv('RUNNER__TIMEOUT', 30)

run_lock = asyncio.Lock()


async def run_code(code):

    async with run_lock:
        # создаём временную директорию для файлов студента
        home_dir = os.path.join("home", "student")
        os.makedirs(home_dir, exist_ok=True)

        with TemporaryDirectory(dir=home_dir) as tmpdir:
            code_file = os.path.join(tmpdir, "main.py")

            # сохраняем код в main.py
            with open(code_file, "w") as f:
                f.write(code)

            command = f"python3 {code_file}"
            try:
                proc = subprocess.run(
                    f"(cd {tmpdir} && chown -R student {tmpdir} && ln -s ../../../datasets datasets"
                    f"&& su -m student -c \'{command}\')"
                    f"> >(head -c {MAX_STDOUT_SIZE}) "
                    f"2> >(head -c {MAX_STDERR_SIZE} >&2)",
                    capture_output=True,
                    timeout=TIMEOUT,
                    shell=True,
                    executable="/bin/bash",
                    env={"MPLCONFIGDIR": tmpdir}
                )
                stdout = proc.stdout.decode("utf-8", errors="ignore")
                stderr = proc.stderr.decode("utf-8", errors="ignore")
                return_code = proc.returncode

                return RunPythonResponse(
                    stdout=stdout,
                    stderr=stderr,
                    return_code=return_code,
                    timeout=False
                    )

            except subprocess.TimeoutExpired:
                return RunPythonResponse(
                    stdout="",
                    stderr="Execution timed out",
                    return_code=None,
                    timeout=True
                    )

            finally:
                # убиваем все процессы студента (безопасная очистка окружения)
                subprocess.call("killall -s 9 -u student", shell=True)
