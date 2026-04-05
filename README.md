Análisis Exploratorio de Datos: Riesgo Crediticio en Chile

Este repositorio contiene un proyecto de Análisis Exploratorio de Datos (EDA) orientado a identificar los determinantes del riesgo crediticio y la probabilidad de morosidad en clientes de una institución financiera.

A través de técnicas de preprocesamiento de datos y visualización estadística, el objetivo principal es evaluar el poder predictivo de distintas variables (demográficas y financieras) para aislar aquellas con mayor relevancia analítica en la detección temprana del riesgo de default.


--- Estructura del Repositorio ---

El proyecto está organizado de la siguiente manera:

proyecto sermana 3.ipynb: Archivo principal (Jupyter Notebook) que documenta el flujo de trabajo completo, dividido en tres etapas:

Preprocesamiento y Limpieza de Datos: Tratamiento de valores nulos e imputación estadística, preservando la integridad de la distribución original.

Análisis Exploratorio (EDA): Generación de estadística descriptiva y evaluación de la distribución de clases (identificación de desbalance).

Visualización de Datos: Construcción de gráficos univariados, bivariados y matrices de correlación para la interpretación de relaciones y multicolinealidad.

data/: Directorio que contiene el set de datos original (dataset_crediticio_chile-1-1.csv) utilizado como fuente primaria para el análisis.


--- Resumen Ejecutivo de Hallazgos ---

El análisis exploratorio permitió extraer las siguientes conclusiones clave para el negocio y el futuro modelamiento predictivo:

Desbalance de Clases: Se constató que aproximadamente el 75% de los clientes presenta un comportamiento de pago favorable (bajo riesgo). Este desbalance natural en el dataset requerirá la implementación de técnicas de remuestreo (balanceo) o el uso de métricas de evaluación específicas en futuras fases de machine learning.

Bajo Poder Predictivo de Variables Demográficas: El análisis bivariado demostró que características como la edad, el sexo, la posesión de un vehículo o los ingresos atípicos (outliers superiores) no presentan diferencias estadísticas significativas entre los grupos de riesgo, descartándolas como predictores aislados de morosidad.

Alta Relevancia del Comportamiento Financiero: Las variables históricas, específicamente el nivel de endeudamiento (cantidad de entidades con deuda) y la presencia de reportes negativos en centrales de riesgo durante los últimos 12 meses, demostraron ser los indicadores más robustos y con mayor poder explicativo para identificar el alto riesgo crediticio.


--- Instrucciones de Ejecución y Revisión ---

Para la evaluación de este proyecto, existen dos alternativas:

Revisión en Entorno Web (Recomendada)
El código, los gráficos generados y el análisis escrito pueden ser visualizados directamente haciendo clic en el archivo "proyecto sermana 3.ipynb" dentro de este repositorio web de GitHub, sin necesidad de configuraciones adicionales.

Ejecución Local (Reproducibilidad)
Para replicar el entorno y ejecutar el código fuente de manera local en su equipo, siga estos pasos:

Paso 1: Clonar este repositorio mediante la terminal usando el enlace web de este GitHub.

Paso 2: Instalación de dependencias requeridas. Asegúrese de tener Python instalado junto con las siguientes librerías de análisis de datos:

pandas

numpy

matplotlib

seaborn
(Puede instalarlas rápidamente ejecutando en su terminal el comando: pip install pandas numpy matplotlib seaborn).

Paso 3: Abrir el archivo "proyecto sermana 3.ipynb" utilizando Jupyter Notebook, JupyterLab o Visual Studio Code.

Paso 4: Ejecutar las celdas de forma secuencial desde el inicio para reproducir todo el análisis y los gráficos.