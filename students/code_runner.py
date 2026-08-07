import tempfile
import subprocess
import sys
import os
import json
from typing import List, Tuple, Dict


def run_user_code(user_code: str, inputs: List[Tuple[str, str]], timeout: int = 5) -> Dict[str, str]:
    """
    Запускает код пользователя в отдельном процессе Python с таймаутом.

    inputs: список кортежей (varname, raw_value_string). raw_value_string будет eval()'т в дочернем процессе.

    Возвращает словарь: { 'output': str, 'error': str }

    Примечание: это упрощённый шаг по изоляции — запуск в subprocess уменьшает риск для основного
    Django-процесса, но для продакшна рекомендуется запускать выполнение в надёжной песочнице
    (контейнер, nsjail, отдельный сервис с лимитами CPU/памяти и сетевыми ограничениями).
    """
    # Создаём временный файл-скрипт, который присвоит входные переменные, выполнит код и
    # напечатает результат (или stderr).
    fd, path = tempfile.mkstemp(suffix='.py', prefix='usercode_')
    os.close(fd)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('# Auto-generated wrapper to run user code\n')
            f.write('import sys, json\n')
            # присвоение переменных (eval в дочернем процессе)
            for varname, raw_value in inputs:
                # сохраняем значение как литерал строкой, потом eval в дочернем процессе
                # экранируем тройные кавычки
                safe_val = raw_value.replace('\"\"\"', '\"\"\\\"')
                f.write(f"{varname} = eval('''{safe_val}''')\n")

            f.write('\n# User code starts here\n')
            f.write(user_code)
            f.write('\n')
            f.write('\n# If there is a callable `solve`, call it and print the result\n')
            f.write('try:\n')
            f.write('    if "solve" in globals() and callable(globals()["solve"]):\n')
            # build args list in the same order as inputs
            arg_names = [var for var, _ in inputs]
            if arg_names:
                f.write('        result = globals()["solve"](' + ','.join(arg_names) + ')\n')
            else:
                f.write('        result = globals()["solve"]()\n')
            f.write('        # print result to stdout\n')
            f.write('        print(result)\n')
            f.write('except Exception as e:\n')
            f.write('    # propagate exception info to stderr\n')
            f.write('    import traceback\n')
            f.write('    traceback.print_exc(file=sys.stderr)\n')

        # Запускаем скрипт отдельным процессом
        completed = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = completed.stdout or ""
        error = completed.stderr or ""

        return {"output": output, "error": error}

    except subprocess.TimeoutExpired as e:
        return {"output": "", "error": f"TimeoutExpired: execution exceeded {timeout} seconds"}
    except Exception as e:
        return {"output": "", "error": f"{type(e).__name__}: {e}"}
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
