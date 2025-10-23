import math
from Funciones_Matematicas.MathematicalFunction import MathematicalFunction


class PredefinedFunction(MathematicalFunction):
    """Funciones predefinidas comunes"""
    
    def __init__(self, func_type: str, amplitude: float = 1.0, period: float = 2.0):
        super().__init__(amplitude, period)
        self.func_type = func_type
        self.name = func_type
    
    def evaluate(self, t: float) -> float:
        """Evalúa funciones predefinidas"""
        omega = 2 * math.pi / self.period
        
        try:
            if self.func_type == "Seno":
                return self.amplitude * math.sin(omega * t)
            elif self.func_type == "Coseno":
                return self.amplitude * math.cos(omega * t)
            elif self.func_type == "Onda Cuadrada":
                return self.amplitude if math.sin(omega * t) >= 0 else -self.amplitude
            elif self.func_type == "Onda Triangular":
                # Función triangular usando formulación directa
                t_norm = (t % self.period) / self.period
                if t_norm < 0.25:
                    return self.amplitude * (4 * t_norm)
                elif t_norm < 0.75:
                    return self.amplitude * (2 - 4 * t_norm)
                else:
                    return self.amplitude * (4 * t_norm - 4)
            elif self.func_type == "Onda Diente de Sierra":
                t_norm = (t % self.period) / self.period
                return self.amplitude * (2 * t_norm - 1)
            elif self.func_type == "Pulso":
                t_norm = t % self.period
                return self.amplitude if t_norm < self.period * 0.1 else 0.0
            else:
                return 0.0
        except Exception as e:
            print(f"Error evaluando función {self.func_type}: {e}")
            return 0.0
