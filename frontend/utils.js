const FEATURE_LABELS = {
  Num_Entidades_Deuda: "Instituciones con deuda",
  Peor_Calificacion_12M: "Peor calificación 12M",
  Ratio_Saldo_Ingreso: "Ratio deuda / ingreso",
  Saldo_Total_CLP: "Deuda total",
  Variacion_Endeudamiento: "Variación de deuda",
  Ingreso_CLP: "Ingreso mensual",
};

const STORAGE_KEY = "creditvision_result";
const RING_LENGTH = 326.7;

function formatApiError(detail) {
  if (!detail) return "Error al calcular. Revise los datos.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") return item;
        const field = (item.loc || []).filter((part) => part !== "body").join(".");
        return field ? `${field}: ${item.msg}` : item.msg;
      })
      .join(" · ");
  }
  return String(detail);
}

function formatCLP(value) {
  return new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    maximumFractionDigits: 0,
  }).format(value);
}

function formatEvalValue(key, value) {
  if (key.includes("CLP") && typeof value === "number") return formatCLP(value);
  if (key === "Peor_Calificacion_12M") {
    const map = { "-1": "Sin historial", 0: "Normal", 1: "Atrasos leves", 2: "Morosidad relevante" };
    return map[value] ?? value;
  }
  if (key === "Variacion_Endeudamiento" && typeof value === "number") {
    return `${(value * 100).toFixed(1)}%`;
  }
  if (key === "Ratio_Saldo_Ingreso" && typeof value === "number") {
    return value.toFixed(2);
  }
  return value;
}

function renderResultPage(data) {
  const pct = data.probabilidad_riesgo_alto * 100;
  const ringFill = document.getElementById("ring-fill");
  const nivel = (data.nivel_riesgo || "").toLowerCase();

  document.getElementById("score-pct").textContent = `${pct.toFixed(1)}%`;
  ringFill.style.strokeDashoffset = String(RING_LENGTH - (RING_LENGTH * Math.min(pct, 100)) / 100);
  ringFill.style.stroke =
    nivel === "bajo" ? "#059669" : nivel === "moderado" ? "#d97706" : "#dc2626";

  const badge = document.getElementById("verdict-badge");
  badge.textContent = data.nivel_riesgo || "—";
  badge.className = `verdict-badge ${nivel}`;

  document.getElementById("verdict-title").textContent = data.etiqueta;
  document.getElementById("verdict-text").textContent = data.recomendacion || "";
  document.getElementById("metric-label").textContent = data.etiqueta;
  document.getElementById("metric-model").textContent = data.modelo;
  document.getElementById("metric-latency").textContent = `${data.latencia_ms} ms`;

  const featuresList = document.getElementById("features");
  featuresList.innerHTML = "";
  (data.variables_clave || []).forEach((item) => {
    const li = document.createElement("li");
    const label = FEATURE_LABELS[item.feature] || item.feature;
    li.innerHTML = `<span>${label}</span><span>${(item.importance * 100).toFixed(1)}%</span>`;
    featuresList.appendChild(li);
  });

  const evaluadosList = document.getElementById("evaluados");
  evaluadosList.innerHTML = "";
  Object.entries(data.variables_evaluadas || {}).forEach(([key, value]) => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${FEATURE_LABELS[key] || key}</span><span>${formatEvalValue(key, value)}</span>`;
    evaluadosList.appendChild(li);
  });
}
