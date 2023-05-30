from flask import request

#convertie los datos de entrada en una instancia de una clase específica
def convert_input_to(class_):
    def wrap(f):
        def dec(*args):
            obj = class_(**request.get_json())
            return f(obj)

        wrap.__name__ = f.__name__
        dec.__name__ = f.__name__
        return dec

    return wrap