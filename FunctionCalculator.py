import re
import cmath


def separateString(func:str):
    return func.split('=')[1]

def calculateValue(func:str, value:float):
    variable = re.search(r'f\((\w)\)', func).group(1)
    sprt_func = separateString(func)
    sprt_func = re.sub(r'(\d)(\w)', r'\1*\2', sprt_func)
    sprt_func = sprt_func.replace('^', '**')
    repl_func = sprt_func.replace(variable, '('+str(value)+')')
    print(repl_func)
    result = eval(repl_func, {"__builtins__": None}, {"cmath": cmath})

    if abs(result.real) < 1e-7:  # Ajusta este umbral según sea necesario
        result = complex(0, result.imag)  # Poner la parte real a cero

    return result, cmath.phase(result)

def getColor(func:str, value:float):
    
    abs_ang = calculateValue(func, value)[1]

    if calculateValue(func, value)[1] < 0:
        abs_ang = cmath.pi + abs(abs_ang)

    r = 255 - (765 * abs_ang / (2 * cmath.pi))
    g = 0
    b = 0

    color = (r, g, b)

if __name__ == '__main__':
    print(calculateValue("f(x)=-1 + -(-.5)^(1/2)", 0))