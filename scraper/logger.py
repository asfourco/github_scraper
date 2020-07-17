import logging
import functools


class LogDecorator(object):
    def __init__(self, name="Decorator Log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        channel = logging.StreamHandler()
        channel.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - [%(levelname)s]: %(message)s"
        )
        channel.setFormatter(formatter)
        self.logger.addHandler(channel)

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
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

        return decorated
