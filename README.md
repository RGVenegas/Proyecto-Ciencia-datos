# Predicción de Riesgo Crediticio mediante Machine Learning

Este repositorio contiene el desarrollo de un sistema de alerta temprana basado en Machine Learning para evaluar el riesgo crediticio de clientes en el sector financiero chileno. El proyecto abarca desde la limpieza y transformación de datos (EDA) hasta el entrenamiento, evaluación y selección de algoritmos predictivos.

## ⚙️ Características del Proyecto

* **Metodología:** CRISP-DM adaptada para un entorno de investigación y desarrollo.
* **Preprocesamiento de Datos:** Imputación inteligente de valores nulos, One-Hot Encoding para variables categóricas y estandarización matemática (StandardScaler).
* **Modelado Predictivo:** Se evaluaron 5 arquitecturas de clasificación (Árboles de Decisión, Random Forest, Gradient Boosting, Support Vector Machine y Regresión Logística).
* **Selección Final:** El modelo implementado es la **Regresión Logística**, seleccionada estratégicamente por su alta interpretabilidad probabilística, su excelente capacidad de generalización (F1-Score superior al 96%) y para mitigar el sobreajuste (Data Leakage) detectado en modelos de ensamble.

## 📂 Estructura del Repositorio

* `/data/raw/`: Contiene el conjunto de datos original e histórico.
* `/data/processed/`: Contiene el dataset final 100% numérico, codificado y escalado, listo para el consumo del modelo.
* `/notebooks/`: Directorio principal que aloja el archivo `proyecto semana 3 predictivo.ipynb` con todo el flujo de código documentado.

## 🚀 Instrucciones de Revisión y Ejecución

### Opción 1: Revisión Web (Recomendada)
Puede visualizar el código, los gráficos de métricas (Matrices de Confusión, Feature Importance) y el análisis analítico directamente haciendo clic en el archivo `notebooks/proyecto semana 3 predictivo.ipynb` en este repositorio de GitHub.

### Opción 2: Ejecución Local

**Paso 1:** Clonar el repositorio en su terminal local:
```bash
git clone [https://github.com/RGVenegas/Proyecto-Ciencia-datos.git](https://github.com/RGVenegas/Proyecto-Ciencia-datos.git)

**Paso 2:** Instalar las dependencias de ciencia de datos requeridas (requiere entorno Python):

pip install pandas numpy matplotlib seaborn scikit-learn

**Paso 3:** Abrir el archivo proyecto semana 3 predictivo.ipynb (utilizando Jupyter Notebook o la extensión de Jupyter en VS Code) y ejecutar todas las celdas de forma secuencial de principio a fin. Gracias al uso de rutas relativas, el código funcionará independientemente del sistema operativo.
```


👥 Integrantes

Rodrigo Venegas

Diego Carmona

Vicente Bustamante