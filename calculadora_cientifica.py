import tkinter as tk
from tkinter import messagebox
import math

SAFE_GLOBALS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'ln': math.log,       # natural log
    'log': math.log,
    'exp': math.exp,      # e^x
    'e': math.e,
    'pi': math.pi,
    'sqrt': math.sqrt,
    'pow': pow,
}

class ScientificCalculator(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title('Calculadora Científica')
        self.resizable(False, False)
        self.expression = ''
        self.create_widgets()

    def create_widgets(self):
        # Entry / display
        self.display_var = tk.StringVar()
        display = tk.Entry(self, textvariable=self.display_var, font=('Consolas', 20), bd=4, relief='ridge', justify='right', width=26)
        display.grid(row=0, column=0, columnspan=6, padx=8, pady=8)

        btns = [
            ('7',1,0),('8',1,1),('9',1,2),('/',1,3),('pi',1,4),('C',1,5),
            ('4',2,0),('5',2,1),('6',2,2),'*',2,3,('e',2,4),('⌫',2,5),
        ]
        # We'll build buttons programmatically below for clarity

        buttons = [
            ('7',1,0),('8',1,1),('9',1,2),('/',1,3),('pi',1,4),('C',1,5),
            ('4',2,0),('5',2,1),('6',2,2),('*',2,3),('e',2,4),('⌫',2,5),
            ('1',3,0),('2',3,1),('3',3,2),('-',3,3),('(',3,4),(')',3,5),
            ('0',4,0),('.',4,1),('±',4,2),('+',4,3),('^',4,4),('=',4,5),

            ('sin',5,0),('cos',5,1),('tan',5,2),('ln',5,3),('exp',5,4),('1/x',5,5),
            ('asin',6,0),('acos',6,1),('atan',6,2),('x^(1/y)',6,3),('x^y',6,4),('sqrt',6,5),
        ]

        for (text,r,c) in buttons:
            action = lambda t=text: self.on_button(t)
            tk.Button(self, text=text, width=7, height=2, command=action).grid(row=r, column=c, padx=3, pady=3)

        # Note: some special buttons handled inside on_button

    def on_button(self, char):
        if char == 'C':
            self.expression = ''
            self.display_var.set(self.expression)
            return
        if char == '⌫':
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
            return
        if char == '=':
            self.calculate()
            return
        if char == '±':
            # toggle sign of last number if possible
            self.toggle_sign()
            return
        if char == '1/x':
            # wrap current expression with reciprocal
            if self.expression.strip() == '':
                return
            self.expression = f'(1/({self.expression}))'
            self.display_var.set(self.expression)
            return
        if char == 'x^y':
            # insert power operator
            self.expression += '**'
            self.display_var.set(self.expression)
            return
        if char == '^':
            # caret visual: map to ** for python
            self.expression += '**'
            self.display_var.set(self.expression)
            return
        if char == 'x^(1/y)':
            # insert pattern for x^(1/y) -> user should type the y and close )
            # we'll insert **(1/  and user must complete with y and )
            self.expression += '**(1/'
            self.display_var.set(self.expression)
            return

        # functions and constants: append with parentheses if function
        functions = {'sin','cos','tan','asin','acos','atan','ln','exp','sqrt'}
        constants = {'pi','e'}
        operators = {'+','-','*','/','(',')','.'}

        if char in functions:
            # ln maps to ln( -> which we'll evaluate using 'ln' from SAFE_GLOBALS
            self.expression += f'{char}('
            self.display_var.set(self.expression)
            return
        if char in constants or char.isdigit() or char in operators:
            self.expression += char
            self.display_var.set(self.expression)
            return

        # fallback
        self.expression += char
        self.display_var.set(self.expression)

    def toggle_sign(self):
        # Try to find last number and toggle sign
        expr = self.expression
        if not expr:
            return
        # split by operators to find last token
        import re
        tokens = re.split(r'([+\-*/()])', expr)
        if not tokens:
            return
        # find last non-empty token
        for i in range(len(tokens)-1, -1, -1):
            if tokens[i].strip() != '':
                last = tokens[i]
                idx = i
                break
        else:
            return
        try:
            if last.startswith('(-') and last.endswith(')'):
                new = last[2:-1]
            else:
                new = f'(-{last})'
            tokens[idx] = new
            self.expression = ''.join(tokens)
            self.display_var.set(self.expression)
        except Exception:
            pass

    def calculate(self):
        expr = self.expression
        if not expr.strip():
            return
        try:
            # Evaluate safely: allow only names in SAFE_GLOBALS
            result = eval(expr, {'_builtins_': None}, SAFE_GLOBALS)
            # Format result: if integer-like, show as int
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.display_var.set(self.expression)
        except Exception as e:
            messagebox.showerror('Error', f'Entrada inválida: {e}')

if _name_ == '_main_':
    app = ScientificCalculator()
    app.mainloop()