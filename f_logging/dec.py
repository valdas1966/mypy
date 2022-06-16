import logging


def log_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def log_info(func):
    def inner(*args, **kwargs):
        logging.info(f'BEGIN, {func.__module__}.{func.__name__}')
        for val in args:
            logging.info(f'ARG, {type(val)}, {val.__str__()[:100]}')
        for key, val in kwargs.items():
            logging.info(f'ARG, {type(val)}, {key}={val.__str__()[:100]}')
        x = func(*args, **kwargs)
        logging.info(f'END, {func.__module__}.{func.__name__}')
        return x
    return inner


def log_info_without_self(func):
    def inner(*args, **kwargs):
        logging.info(f'BEGIN, {func.__module__}.{func.__name__}')
        for i, val in enumerate(args):
            if i == 0:
                continue
            logging.info(f'ARG, {type(val)}, {val.__str__()[:100]}')
        for key, val in kwargs.items():
            logging.info(f'ARG, {type(val)}, {key}={val.__str__()[:100]}')
        func(*args, **kwargs)
        logging.info(f'END, {func.__module__}.{func.__name__}')
    return inner
