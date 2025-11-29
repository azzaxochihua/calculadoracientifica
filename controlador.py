import re
from operaciones import evaluar_expresion

class Controlador:
    def __init__(self):
        self.expression = ""

    def agregar(self, char):
        self.expression += char
        return self.expression

    def borrar(self):
        self.expression = ""
        return self.expression

    def retroceso(self):
        self.expression = self.expression[:-1]
        return self.expression

    def calcular(self):
        self.expression = evaluar_expresion(self.expression)
        return self.expression

    def toggle_sign(self):
        expr = self.expression
        if not expr:
            return expr

        tokens = re.split(r'([+\-*/()])', expr)
        for i in range(len(tokens)-1, -1, -1):
            if tokens[i].strip() != '':
                last = tokens[i]
                idx = i
                break
        else:
            return expr

        if last.startswith('(-') and last.endswith(')'):
            tokens[idx] = last[2:-1]
        else:
            tokens[idx] = f'(-{last})'

        self.expression = ''.join(tokens)
        return self.expression
