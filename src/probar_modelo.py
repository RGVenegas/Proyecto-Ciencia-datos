import joblib
import os

# 1. Python averigua automáticamente dónde está guardado este script (la carpeta src)
directorio_script = os.path.dirname(os.path.abspath(__file__))

# 2. Desde esa carpeta 'src', retrocede un nivel ('..') y entra a 'models'
ruta_modelo = os.path.join(directorio_script, '../models/modelo_regresion_logistica.pkl')

# 3. Descongelamos el modelo
modelo_banco = joblib.load(ruta_modelo)

print("¡Modelo cargado exitosamente!\n")
print(f"Tipo de algoritmo: {modelo_banco}")
print("\nPrimeros 5 coeficientes matemáticos guardados en el archivo:")
print(modelo_banco.coef_[0][:5])