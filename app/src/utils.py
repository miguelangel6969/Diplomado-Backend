from flask import request


def convert_input_to(class_):
    def wrap(f):
        def dec(*args):
            obj = class_(**request.get_json())
            return f(obj)

        wrap.__name__ = f.__name__
        dec.__name__ = f.__name__
        return dec

    return wrap