import logging
from f_utils import u_inspect


global count
count = 0


def log_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def log_info(func):
    return log_template(func, is_class=False)


def log_info_class(func):
    return log_template(func, is_class=True)


def log_template(func, is_class=False):
    def inner(*args, **kwargs):
        # return func(*args, **kwargs)
        global count
        try:
            tabs = '\t' * count
            logging.info(f'{tabs}BEGIN, {func.__module__}.{func.__name__}')
            logging.info(f'{tabs}DESC, {u_inspect.get_desc(func)}')
            count += 1
            tabs = '\t' * count
            for i, val in enumerate(args):
                if is_class and not i:
                    continue
                logging.info(f'{tabs}ARG, {details_val(val)}')
            for key, val in kwargs.items():
                logging.info(f'{tabs}KWARG, {details_val(val, key)}')
            return func(*args, **kwargs)
        except Exception as e:
            logging.info(f'{tabs}EXCEPTION, {e}')
            raise Exception(e)
        finally:
            count -= 1
            tabs = '\t' * count
            logging.info(f'{tabs}END, {func.__module__}.{func.__name__}')
    return inner


def log_row(msg):
    global count
    tabs = '\t' * count
    logging.info(f'{tabs}MSG, {msg[:100]}')


def details_val(val, key=None):
    str_type = type(val)
    str_length = str()
    try:
        str_length = f'[{len(val)}]'
    except Exception as e:
        pass
    str_key = f'{key}=' if key else str()
    str_val = val.__str__().replace('\n', '')[:100]
    return f'{str_type}, {str_length}, {str_key}{str_val}'