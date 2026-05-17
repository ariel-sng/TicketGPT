from functools import wraps
import time

def measure_latency(func):
    '''
        Decorator que recibe una función con sus correspondientes parámetros y devuelve dos datos: 
        el resultado de la función original y la latencia en completarse
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        
        elapsed_time = (end - start)*1000  # guardamos el valor en una variable en ms
        
        return result, elapsed_time
    return wrapper