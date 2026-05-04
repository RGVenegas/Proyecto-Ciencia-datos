# Predicción de Riesgo Crediticio mediante Machine Learning

Este repositorio contiene el desarrollo de un sistema de alerta temprana basado en Machine Learning para evaluar el riesgo crediticio de clientes en el sector financiero chileno. El proyecto abarca desde la limpieza y transformación de datos (EDA) hasta el entrenamiento, evaluación, selección de algoritmos predictivos y su posterior exportación a un entorno simulado de producción.

## ⚙️ Características del Proyecto

* **Metodología:** CRISP-DM adaptada para un entorno de investigación y desarrollo.
* **Preprocesamiento de Datos:** Imputación inteligente de valores nulos, One-Hot Encoding para variables categóricas y estandarización matemática (StandardScaler).
* **Modelado Predictivo:** Se evaluaron 5 arquitecturas de clasificación (Árboles de Decisión, Random Forest, Gradient Boosting, Support Vector Machine y Regresión Logística).
* **Selección Final:** Tras comparar los cinco algoritmos en el conjunto de prueba, se exporta el modelo con **mayor F1-Score** (criterio definido en el notebook). En la práctica suele predominar la **Regresión Logística** por interpretabilidad y generalización; el escalado se ajusta solo con datos de entrenamiento para evitar fuga de información hacia el test.

## 📂 Estructura del Repositorio

* `/data/raw/`: Contiene el conjunto de datos original e histórico.
* `/data/processed/`: Contiene el dataset final 100% numérico, codificado y escalado, listo para el consumo del modelo.
* `/models/`: Contiene el modelo predictivo exportado como `modelo_final.pkl` (mejor F1 en test según el notebook), listo para integrarse en producción mediante APIs.
* `/notebooks/`: Directorio principal que aloja el archivo `proyecto semana 3 predictivo.ipynb` con todo el flujo analítico documentado.
* `/src/`: Scripts de ejecución en Python plano (ej. `probar_modelo.py` para testear la carga de `modelo_final.pkl`).

## 🚀 Instrucciones de Revisión y Ejecución

### Opción 1: Revisión Web (Recomendada)
Puede visualizar el código, los gráficos de métricas (Matrices de Confusión, Feature Importance) y el análisis analítico directamente haciendo clic en el archivo `notebooks/proyecto semana 3 predictivo.ipynb` en este repositorio de GitHub.

### Opción 2: Ejecución Local Completa

**Paso 1:** Clonar el repositorio en su terminal local:
`git clone https://github.com/RGVenegas/Proyecto-Ciencia-datos.git`

**Paso 2:** Instalar las dependencias de ciencia de datos requeridas (requiere entorno Python):
`pip install pandas numpy matplotlib seaborn scikit-learn joblib`

**Paso 3:** Ejecución del Flujo de Datos (Notebook)
Abrir el archivo `notebooks/proyecto semana 3 predictivo.ipynb` (utilizando Jupyter Notebook o la extensión de Jupyter en VS Code) y ejecutar todas las celdas de forma secuencial de principio a fin. Eso actualiza `data/processed/dataset_crediticio_procesado.csv` y genera `models/modelo_final.pkl` (el clasificador con mejor F1 en test). Gracias al uso de rutas relativas integradas con la librería `os`, el código funcionará independientemente del sistema operativo o carpeta de origen.

**Paso 4:** Prueba del Modelo en "Producción"
Para comprobar que el modelo ha sido exportado correctamente y está listo para recibir nuevos clientes, ejecute el script de prueba desde la raíz del proyecto en su terminal:
`python src/probar_modelo.py` (carga `models/modelo_final.pkl`).

## 👥 Integrantes

* Rodrigo Venegas
* Diego Carmona
* Vicente Bustamante