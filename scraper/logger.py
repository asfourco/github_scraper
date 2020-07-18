import logging
import functools


class Log(object):
    def __init__(self, name="Decorator Log"):
        log_format = "%(asctime)s - %(name)s - [%(levelname)s]: %(message)s"

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler("logs/github_api.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(fh)

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(
                    f"function_name:{fn.__name__} || args:{args} || kwargs:{kwargs}"
                )
                result = fn(*args, **kwargs)
                self.logger.debug(f"Result => {result}")
            except Exception as e:
                self.logger.error(f"Exception {e}")
                raise e
            else:
                return result

        return wrapper
