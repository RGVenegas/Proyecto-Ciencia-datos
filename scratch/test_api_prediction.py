import urllib.request
import json

url = "http://127.0.0.1:8000/predict"
headers = {"Content-Type": "application/json"}

perfiles = {
    "Perfil A (Riesgo Bajo)": {
        "Num_Entidades_Deuda": 1,
        "Peor_Calificacion_12M": 0.0,
        "Ingreso_CLP": 2500000.0,
        "Saldo_Total_CLP": 250000.0,
        "Variacion_Endeudamiento": 0.0
    },
    "Perfil B (Riesgo Alto)": {
        "Num_Entidades_Deuda": 6,
        "Peor_Calificacion_12M": 2.0,
        "Ingreso_CLP": 800000.0,
        "Saldo_Total_CLP": 4000000.0,
        "Variacion_Endeudamiento": 0.45
    },
    "Perfil C (Riesgo Moderado)": {
        "Num_Entidades_Deuda": 3,
        "Peor_Calificacion_12M": 1.0,
        "Ingreso_CLP": 1200000.0,
        "Saldo_Total_CLP": 1500000.0,
        "Variacion_Endeudamiento": 0.15
    }
}

for name, payload in perfiles.items():
    print(f"\n=== {name} ===")
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as res:
            response_data = json.loads(res.read().decode("utf-8"))
            print(f"Probabilidad de Riesgo Alto: {response_data['probabilidad_riesgo_alto']*100:.2f}%")
            print(f"Nivel de Riesgo Clasificado: {response_data['nivel_riesgo']}")
            print(f"Recomendación: {response_data['recomendacion']}")
            print(f"Latencia: {response_data['latencia_ms']} ms")
    except Exception as e:
        print("Error al realizar la petición:", e)
