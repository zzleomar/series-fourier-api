import math
import re
from Funciones_Matematicas.MathematicalFunction import MathematicalFunction
class CustomFunction(MathematicalFunction):
    """Función personalizada definida por el usuario"""
    
    def __init__(self, expression: str, amplitude: float = 1.0, period: float = 2.0):
        super().__init__(amplitude, period)
        self.expression = expression
        self.name = f"Custom: {expression}"
        self.compiled_expr = self._compile_expression(expression)
    
    def _compile_expression(self, expr: str):
        """Compila la expresión matemática para evaluación segura"""
        # Reemplazar funciones matemáticas comunes
        expr = expr.replace('^', '**')  # Exponenciación
        expr = re.sub(r'\bsin\b', 'math.sin', expr)
        expr = re.sub(r'\bcos\b', 'math.cos', expr)
        expr = re.sub(r'\btan\b', 'math.tan', expr)
        expr = re.sub(r'\bexp\b', 'math.exp', expr)
        expr = re.sub(r'\blog\b', 'math.log', expr)
        expr = re.sub(r'\babs\b', 'abs', expr)
        expr = re.sub(r'\bsqrt\b', 'math.sqrt', expr)
        expr = re.sub(r'\bpi\b', 'math.pi', expr)
        expr = re.sub(r'\be\b', 'math.e', expr)
        
        return expr
    
    def evaluate(self, t: float) -> float:
        """Evalúa la función personalizada"""
        try:
            # Crear un namespace seguro para la evaluación
            namespace = {
                't': t,
                'math': math,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'log': math.log,
                'sqrt': math.sqrt,
                'abs': abs,
                'pi': math.pi,
                'e': math.e,
                'A': self.amplitude,
                'T': self.period
            }

            result = eval(self.compiled_expr, {"__builtins__": {}}, namespace)
            if result is None:
                raise ValueError("La expresión retorna None. Asegúrate de que la expresión devuelva un valor numérico.")
            return float(result)
        except SyntaxError as e:
            raise ValueError(f"Error de sintaxis en la expresión: '{self.expression}'. Verifica que esté bien escrita.")
        except NameError as e:
            variable = str(e).split("'")[1] if "'" in str(e) else "desconocida"
            raise ValueError(f"Variable o función '{variable}' no reconocida. Usa: t, A, T, sin, cos, tan, exp, log, sqrt, abs, pi, e")
        except ZeroDivisionError:
            raise ValueError(f"División por cero en la expresión para t={t}")
        except TypeError as e:
            raise ValueError(f"Error de tipo en la expresión: {str(e)}. Verifica que todas las operaciones sean válidas.")
        except ValueError as e:
            raise ValueError(f"Error al evaluar la expresión: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado al evaluar '{self.expression}': {str(e)}")
