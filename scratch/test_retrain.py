import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocessing import clean_dataset, encode_features
from src.config import RANDOM_STATE

DATA_RAW = ROOT / "data" / "raw" / "dataset_crediticio_chile-1-1.csv"
raw_df = pd.read_csv(DATA_RAW)

# Limpiar dataset usando la lógica del proyecto
cleaned_df = clean_dataset(raw_df)

# Caso 1: Ratio Original (Anual)
print("=== CASO 1: Ratio Original (Anual) ===")
X, y = encode_features(cleaned_df)

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

clf = GradientBoostingClassifier(random_state=RANDOM_STATE, n_estimators=100, max_depth=3)
clf.fit(x_train_scaled, y_train)
y_pred = clf.predict(x_test_scaled)
print(f"F1 score en Test: {f1_score(y_test, y_pred):.4f}")

# Caso 2: Ratio Recalculado (Mensual)
print("\n=== CASO 2: Ratio Recalculado (Mensual) ===")
cleaned_df_m = cleaned_df.copy()
cleaned_df_m["Ratio_Saldo_Ingreso"] = cleaned_df_m["Saldo_Total_CLP"] / cleaned_df_m["Ingreso_CLP"]

X_m, y_m = encode_features(cleaned_df_m)

x_train_m, x_test_m, y_train_m, y_test_m = train_test_split(
    X_m, y_m, test_size=0.2, random_state=RANDOM_STATE, stratify=y_m
)

scaler_m = StandardScaler()
x_train_scaled_m = scaler_m.fit_transform(x_train_m)
x_test_scaled_m = scaler_m.transform(x_test_m)

clf_m = GradientBoostingClassifier(random_state=RANDOM_STATE, n_estimators=100, max_depth=3)
clf_m.fit(x_train_scaled_m, y_train_m)
y_pred_m = clf_m.predict(x_test_scaled_m)
print(f"F1 score en Test: {f1_score(y_test_m, y_pred_m):.4f}")

# Evaluar Perfiles
print("\n=== Evaluar Perfiles ===")
referencia = {
    "Sexo": "M", "Tipo_Empleo": "IND", "Tiene_Vehiculo": 0.0, "Edad": 39.0, "Ciudad_Chile": "SANTIAGO",
    "Tiene_Tarjeta": 0.0, "Saldo_Tarjeta_CLP": 0.0, "Peor_Calificacion_36M": 0.0,
    "Reportes_Central_36M": 30.0, "Reportes_Central_12M": 12.0,
    "Promedio_Saldo_CLP": 2449474.41, "Maximo_Saldo_CLP": 4250000.0
}

# Perfil A
pa = referencia.copy()
pa.update({"Num_Entidades_Deuda": 1.0, "Peor_Calificacion_12M": 0.0, "Ingreso_CLP": 2500000.0, "Saldo_Total_CLP": 250000.0, "Variacion_Endeudamiento": 0.0})

# Perfil B
pb = referencia.copy()
pb.update({"Num_Entidades_Deuda": 6.0, "Peor_Calificacion_12M": 2.0, "Ingreso_CLP": 800000.0, "Saldo_Total_CLP": 4000000.0, "Variacion_Endeudamiento": 0.45})

# Perfil C
pc = referencia.copy()
pc.update({"Num_Entidades_Deuda": 3.0, "Peor_Calificacion_12M": 1.0, "Ingreso_CLP": 1200000.0, "Saldo_Total_CLP": 1500000.0, "Variacion_Endeudamiento": 0.15})

# Función para vectorizar un registro como en transform_single_record
def vectorize(record, feature_names, scaler_obj):
    frame = pd.DataFrame([record])
    # Como ya está limpio, hacemos codificación one-hot alineada
    frame_concat = pd.concat([frame, pd.DataFrame({"RiesgoAlto": [0]})], axis=1)
    encoded, _ = encode_features(frame_concat)
    aligned = pd.DataFrame(columns=feature_names, index=[0]).fillna(0.0)
    for column in encoded.columns:
        if column in aligned.columns:
            aligned[column] = encoded[column].values
    return pd.DataFrame(scaler_obj.transform(aligned), columns=feature_names)

feature_names = list(X.columns)

# Evaluamos Caso 1: API original (ratio mensual en modelo anual)
print("\n--- CASO 1: API original (modelo anual, ratio mensual) ---")
for name, p in [("Perfil A", pa), ("Perfil B", pb), ("Perfil C", pc)]:
    p_copy = p.copy()
    p_copy["Ratio_Saldo_Ingreso"] = p_copy["Saldo_Total_CLP"] / p_copy["Ingreso_CLP"]
    vec = vectorize(p_copy, feature_names, scaler)
    prob = clf.predict_proba(vec)[0][1]
    print(f"{name}: Ratio = {p_copy['Ratio_Saldo_Ingreso']:.4f}, Prob = {prob*100:.2f}%")

# Evaluamos Caso 1 corregido: API corregida (ratio anual en modelo anual)
print("\n--- CASO 1 CORREGIDO: Modelo anual, ratio corregido (anual) ---")
for name, p in [("Perfil A", pa), ("Perfil B", pb), ("Perfil C", pc)]:
    p_copy = p.copy()
    p_copy["Ratio_Saldo_Ingreso"] = p_copy["Saldo_Total_CLP"] / (p_copy["Ingreso_CLP"] * 12)
    vec = vectorize(p_copy, feature_names, scaler)
    prob = clf.predict_proba(vec)[0][1]
    print(f"{name}: Ratio = {p_copy['Ratio_Saldo_Ingreso']:.4f}, Prob = {prob*100:.2f}%")

# Evaluamos Caso 2: Modelo re-entrenado con ratio mensual, pasamos ratio mensual
print("\n--- CASO 2: Modelo re-entrenado con ratio mensual, ratio mensual ---")
for name, p in [("Perfil A", pa), ("Perfil B", pb), ("Perfil C", pc)]:
    p_copy = p.copy()
    p_copy["Ratio_Saldo_Ingreso"] = p_copy["Saldo_Total_CLP"] / p_copy["Ingreso_CLP"]
    vec = vectorize(p_copy, feature_names, scaler_m)
    prob = clf_m.predict_proba(vec)[0][1]
    print(f"{name}: Ratio = {p_copy['Ratio_Saldo_Ingreso']:.4f}, Prob = {prob*100:.2f}%")
