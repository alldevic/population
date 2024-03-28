"""
Тестовый декоратор для профайлинга
примонтировать папку
import dev_utils
после @route
@dev_utils.profile_to_txt()
"""

import os
import pstats
import sys
import uuid
from cProfile import Profile
from datetime import datetime
from functools import wraps


# print_args=[10]
def profile_to_txt(sort_args=['cumulative'], print_args=[], folder: str = './profiles'):
    """
    Оборачиваем вызов метода в cProfile, на выходе *.txt для человека
    Параметры:
    https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
    https://docs.python.org/3/library/profile.html#pstats.Stats.print_stats
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = Profile()
            result = None
            try:
                profiler.enable()
                result = func(*args, **kwargs)
                profiler.disable()
            finally:
                old_std_out = sys.stdout
                file_name = f'{datetime.now()}_{str(uuid.uuid4())[:10]}.txt'
                if not os.path.exists(folder):
                    os.makedirs(folder)
                sys.stdout = open(f'{folder}/{file_name}', 'w')
                stats = pstats.Stats(profiler)
                stats.strip_dirs().sort_stats(*sort_args).print_stats(*print_args)
                sys.stdout.flush()
                sys.stdout = old_std_out
            return result
        return wrapper

    return decorator


def profile_to_prof(folder: str = './profiles'):
    """
    Оборачиваем вызов метода в cProfile, на выходе *.prof для snakeviz
    или другой утилиты
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = Profile()
            result = None
            try:
                profiler.enable()
                result = func(*args, **kwargs)
                profiler.disable()
            finally:
                file_name = f'{datetime.now()}_{str(uuid.uuid4())[:10]}.prof'
                if not os.path.exists(folder):
                    os.makedirs(folder)
                profiler.dump_stats(f'{folder}/{file_name}')
            return result
        return wrapper

    return decorator
