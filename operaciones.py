import math

SAFE_GLOBALS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'ln': math.log,
    'log': math.log,
    'exp': math.exp,
    'e': math.e,
    'pi': math.pi,
    'sqrt': math.sqrt,
    'pow': pow,
}

def evaluar_expresion(expr):
    try:
        resultado = eval(expr, {'__builtins__': None}, SAFE_GLOBALS)
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)
        return str(resultado)
    except Exception as e:
        return f"ERROR: {e}"
