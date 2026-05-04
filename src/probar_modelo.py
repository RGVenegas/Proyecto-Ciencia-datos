import joblib
import os

# 1. Python averigua automáticamente dónde está guardado este script (la carpeta src)
directorio_script = os.path.dirname(os.path.abspath(__file__))

# 2. Desde esa carpeta 'src', retrocede un nivel ('..') y entra a 'models'
ruta_modelo = os.path.join(directorio_script, '../models/modelo_final.pkl')

# 3. Descongelamos el modelo
modelo_banco = joblib.load(ruta_modelo)

print("Modelo cargado exitosamente.\n")
print(f"Tipo de algoritmo: {modelo_banco}")
if hasattr(modelo_banco, 'coef_') and modelo_banco.coef_ is not None:
    print("\nPrimeros 5 coeficientes guardados en el archivo:")
    print(modelo_banco.coef_.ravel()[:5])
elif hasattr(modelo_banco, 'feature_importances_'):
    print("\nPrimeras 5 importancias de variables:")
    print(modelo_banco.feature_importances_[:5])
else:
    print("\nEste estimador no expone coef_ ni feature_importances_ en texto breve.")
