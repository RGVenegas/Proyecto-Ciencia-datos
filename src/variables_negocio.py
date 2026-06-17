"""Descripciones de negocio para variables del scoring crediticio."""
from src.config import FEATURE_IMPORTANCE_THRESHOLD

VARIABLES_NEGOCIO = {
    "Num_Entidades_Deuda": {
        "titulo": "Instituciones con deuda activa",
        "descripcion": "Número de entidades financieras donde el cliente mantiene deuda vigente.",
        "fuente": "Buró / sistema core bancario",
    },
    "Peor_Calificacion_12M": {
        "titulo": "Peor calificación crediticia (12 meses)",
        "descripcion": "Peor comportamiento de pago registrado en los últimos 12 meses. -1 indica sin historial.",
        "fuente": "Central de riesgo",
    },
    "Ingreso_CLP": {
        "titulo": "Ingreso mensual líquido",
        "descripcion": "Ingreso mensual declarado o verificado, en pesos chilenos.",
        "fuente": "Liquidaciones / declaración del cliente",
    },
    "Saldo_Total_CLP": {
        "titulo": "Deuda total consolidada",
        "descripcion": "Suma de saldos de créditos, tarjetas y líneas activas.",
        "fuente": "Buró / consolidado de deuda",
    },
    "Ratio_Saldo_Ingreso": {
        "titulo": "Ratio deuda / ingreso",
        "descripcion": "Relación entre deuda total e ingreso mensual. Se calcula automáticamente.",
        "fuente": "Derivado (deuda total ÷ ingreso)",
    },
    "Variacion_Endeudamiento": {
        "titulo": "Variación reciente del endeudamiento",
        "descripcion": "Cambio porcentual reciente en el nivel de deuda (señal de alerta temprana).",
        "fuente": "Monitoreo de cartera / buró",
    },
}

VARIABLES_EXCLUIDAS_UI = [
    "Edad",
    "Sexo",
    "Ciudad_Chile",
    "Tipo_Empleo",
    "Tiene_Vehiculo",
    "Tiene_Tarjeta",
    "Saldo_Tarjeta_CLP",
    "Peor_Calificacion_36M",
    "Reportes_Central_36M",
    "Reportes_Central_12M",
    "Promedio_Saldo_CLP",
    "Maximo_Saldo_CLP",
    "ScoreRiesgo",
]

INTRO_SISTEMA = {
    "titulo": "Evaluación de riesgo del cliente",
    "proposito": (
        "Herramienta de apoyo a la venta en sucursal para identificar perfiles con "
        "riesgo alto antes de ofrecer productos de crédito."
    ),
    "datos_utilizados": (
        "Endeudamiento (deuda total, instituciones activas y variación reciente), "
        "central de riesgo (peor calificación 12 meses) y capacidad de pago "
        "(ingreso y relación deuda/ingreso)."
    ),
    "criterio_variables": (
        f"El formulario incluye únicamente antecedentes financieros con impacto en la "
        f"decisión (importancia ≥ {FEATURE_IMPORTANCE_THRESHOLD:.1%})."
    ),
    "exclusion_leakage": None,
}
