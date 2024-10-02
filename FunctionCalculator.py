import numpy as np
import matplotlib.pyplot as plt
import re
import cmath
import os

# Funciones que ya tienes para evaluar la función compleja y generar colores
def separateString(func: str):
    return func.split('=')[1]

def calculateValue(func: str, value: complex):
    """Calcula el valor de la función compleja para un valor dado."""
    variable = re.search(r'f\((\w)\)', func).group(1)
    sprt_func = separateString(func)
    sprt_func = re.sub(r'(\d)(\w)', r'\1*\2', sprt_func)  # Añadir multiplicación implícita
    sprt_func = sprt_func.replace('^', '**')  # Reemplazar ^ con **
    
    # Reemplazar la variable con el valor numérico
    repl_func = sprt_func.replace(variable, f'({value})')
    try:
        result = eval(repl_func, {"__builtins__": None}, {"cmath": cmath, "abs": abs})
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")

    if abs(result.real) < 1e-7:  # Si la parte real es muy pequeña, ajustarla a cero
        result = complex(0, result.imag)

    return result, cmath.phase(result)

def getColor(func: str, value: complex):
    """Genera el color basado en la fase del número complejo calculado."""
    _, phase_angle = calculateValue(func, value)
    
    # Ajustar el ángulo a [0, 2π]
    if phase_angle < 0:
        phase_angle += 2 * cmath.pi

    # Convertir el ángulo en un valor de color RGB
    if 2 * cmath.pi / 3 > phase_angle >= 0:
        r = 255 - int(765 * phase_angle / (2 * cmath.pi))
    elif 4 * cmath.pi / 3 > phase_angle >= 2 * cmath.pi / 3:
        r = 0
    else:
        r = 255 - int(765 * (2 * cmath.pi - phase_angle) / (2 * cmath.pi))

    if 2 * cmath.pi / 3 > phase_angle >= 0:
        g = 255 - int(765 * (phase_angle - 2 * cmath.pi / 3) / (2 * cmath.pi))
    elif 4 * cmath.pi / 3 > phase_angle >= 2 * cmath.pi / 3:
        g = 255 - int(765 * (2 * cmath.pi - phase_angle - 2 * cmath.pi / 3) / (2 * cmath.pi))
    else:
        g = 0

    if 2 * cmath.pi / 3 > phase_angle >= 0:
        b = 0
    elif 4 * cmath.pi / 3 > phase_angle >= 2 * cmath.pi / 3:
        b = 255 - int(765 * (phase_angle - 4 * cmath.pi / 3) / (2 * cmath.pi))
    else:
        b = 255 - int(765 * (2 * cmath.pi - phase_angle - 4 * cmath.pi / 3) / (2 * cmath.pi))

    return (r / 255, g / 255, b / 255)  # Normalizamos a valores entre 0 y 1 para matplotlib

# Función para graficar usando matplotlib
def plot_complex_function(func: str, re_min=-2, re_max=2, im_min=-2, im_max=2, resolution=500):
    """Grafica una función compleja en el plano usando colores."""
    re = np.linspace(re_min, re_max, resolution)
    im = np.linspace(im_min, im_max, resolution)
    Re, Im = np.meshgrid(re, im)
    
    # Malla de números complejos
    Z = Re + 1j * Im
    
    # Crear una matriz para almacenar los colores
    colors = np.zeros((resolution, resolution, 3))
    
    # Evaluar la función y calcular el color para cada punto
    for i in range(resolution):
        for j in range(resolution):
            colors[i, j] = getColor(func, Z[i, j])
            os.system("cls")
            print("cargando: " + str(j) + "/" + str(resolution))
            print("cargando: " + str(i) + "/" + str(resolution))
    
    # Mostrar el gráfico con matplotlib
    plt.imshow(colors, extent=(re_min, re_max, im_min, im_max))
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.title(f'Gráfico de la función compleja: {func}')
    plt.show()

if __name__ == '__main__':
    # Prueba de la función
    func_str = "f(x)=x"
    plot_complex_function(func_str, re_min=-2, re_max=2, im_min=-2, im_max=2, resolution=100)
