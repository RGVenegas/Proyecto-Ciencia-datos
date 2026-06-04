"""Esquemas Pydantic para validación de entrada/salida de la API."""
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ClienteInput(BaseModel):
    """Perfil completo (24 features). Uso técnico / integraciones."""

    Sexo: Literal["F", "M"]
    Tipo_Empleo: str = Field(..., min_length=1, max_length=40)
    Tiene_Vehiculo: Literal[0, 1]
    Edad: int = Field(..., ge=18, le=100)
    Ciudad_Chile: str = Field(..., min_length=2, max_length=40)
    Num_Entidades_Deuda: int = Field(..., ge=0, le=20)
    Tiene_Tarjeta: Literal[0, 1]
    Saldo_Tarjeta_CLP: float = Field(..., ge=0)
    Saldo_Total_CLP: float = Field(..., ge=0)
    Variacion_Endeudamiento: float
    Peor_Calificacion_36M: float | None = None
    Peor_Calificacion_12M: float | None = None
    Reportes_Central_36M: int = Field(..., ge=0)
    Reportes_Central_12M: int = Field(..., ge=0)
    Promedio_Saldo_CLP: float = Field(..., ge=0)
    Maximo_Saldo_CLP: float = Field(..., ge=0)
    Ingreso_CLP: float = Field(..., gt=0)
    Ratio_Saldo_Ingreso: float = Field(..., ge=0)

    @field_validator("Tipo_Empleo", "Ciudad_Chile")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not cleaned:
            raise ValueError("El campo no puede estar vacío.")
        return cleaned

    @model_validator(mode="after")
    def normalizar_ratio(self) -> "ClienteInput":
        esperado = round(self.Saldo_Total_CLP / self.Ingreso_CLP, 4) if self.Ingreso_CLP > 0 else 0.0
        object.__setattr__(self, "Ratio_Saldo_Ingreso", esperado)
        return self


class EvaluacionCrediticiaInput(BaseModel):
    """Variables predictivas con aporte real al modelo (sin campos demográficos irrelevantes)."""

    Num_Entidades_Deuda: int = Field(..., ge=0, le=20)
    Peor_Calificacion_12M: float = Field(
        default=-1,
        description="-1 sin historial; 0 normal; valores positivos indican deterioro",
    )
    Ingreso_CLP: float = Field(..., gt=0)
    Saldo_Total_CLP: float = Field(..., ge=0)
    Variacion_Endeudamiento: float = Field(default=0)

    def to_cliente_completo(self, referencia: dict[str, Any] | None = None) -> ClienteInput:
        ref = referencia or {}
        ingreso = self.Ingreso_CLP
        saldo = self.Saldo_Total_CLP
        ratio = round(saldo / ingreso, 4) if ingreso > 0 else 0.0

        return ClienteInput(
            Sexo=ref.get("Sexo", "F"),
            Tipo_Empleo=ref.get("Tipo_Empleo", "DEP"),
            Tiene_Vehiculo=ref.get("Tiene_Vehiculo", 0),
            Edad=int(ref.get("Edad", 41)),
            Ciudad_Chile=ref.get("Ciudad_Chile", "SANTIAGO"),
            Num_Entidades_Deuda=self.Num_Entidades_Deuda,
            Tiene_Tarjeta=ref.get("Tiene_Tarjeta", 0),
            Saldo_Tarjeta_CLP=float(ref.get("Saldo_Tarjeta_CLP", 0)),
            Saldo_Total_CLP=saldo,
            Variacion_Endeudamiento=self.Variacion_Endeudamiento,
            Peor_Calificacion_36M=float(ref.get("Peor_Calificacion_36M", -1)),
            Peor_Calificacion_12M=self.Peor_Calificacion_12M,
            Reportes_Central_36M=int(ref.get("Reportes_Central_36M", 0)),
            Reportes_Central_12M=int(ref.get("Reportes_Central_12M", 0)),
            Promedio_Saldo_CLP=float(ref.get("Promedio_Saldo_CLP", saldo)),
            Maximo_Saldo_CLP=float(ref.get("Maximo_Saldo_CLP", saldo)),
            Ingreso_CLP=ingreso,
            Ratio_Saldo_Ingreso=ratio,
        )

    def variables_utilizadas(self) -> dict[str, float | int]:
        ratio = round(self.Saldo_Total_CLP / self.Ingreso_CLP, 4)
        return {
            "Num_Entidades_Deuda": self.Num_Entidades_Deuda,
            "Peor_Calificacion_12M": self.Peor_Calificacion_12M,
            "Ingreso_CLP": self.Ingreso_CLP,
            "Saldo_Total_CLP": self.Saldo_Total_CLP,
            "Ratio_Saldo_Ingreso": ratio,
            "Variacion_Endeudamiento": self.Variacion_Endeudamiento,
        }


class PredictionResponse(BaseModel):
    riesgo_alto: int
    probabilidad_riesgo_alto: float
    etiqueta: str
    recomendacion: str
    nivel_riesgo: str
    modelo: str
    latencia_ms: float
    variables_clave: list[dict]
    variables_evaluadas: dict[str, Any] | None = None


class HealthResponse(BaseModel):
    status: str
    modelo_cargado: bool
    modelo: str | None = None


class ErrorResponse(BaseModel):
    detail: str
