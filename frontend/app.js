const form = document.getElementById("form-cliente");
const estadoApi = document.getElementById("estado-api");
const formError = document.getElementById("form-error");
const btnCalcular = document.getElementById("btn-calcular");
const ingresoInput = document.getElementById("ingreso");
const deudaInput = document.getElementById("deuda");
const ratioInput = document.getElementById("ratio");

function updateRatio() {
  const ingreso = Number(ingresoInput.value);
  const deuda = Number(deudaInput.value);
  if (ingreso > 0) {
    ratioInput.value = (deuda / ingreso).toFixed(2);
  }
}

ingresoInput.addEventListener("input", updateRatio);
deudaInput.addEventListener("input", updateRatio);
updateRatio();

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    if (data.status === "ok") {
      estadoApi.textContent = `En línea · ${data.modelo}`;
      estadoApi.style.background = "rgba(16, 185, 129, 0.18)";
    } else {
      estadoApi.textContent = "Sin modelo entrenado";
      estadoApi.style.background = "rgba(239, 68, 68, 0.18)";
    }
  } catch {
    estadoApi.textContent = "API no disponible";
    estadoApi.style.background = "rgba(239, 68, 68, 0.18)";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.classList.add("hidden");
  btnCalcular.disabled = true;
  btnCalcular.textContent = "Calculando...";

  const raw = Object.fromEntries(new FormData(form).entries());
  const payload = {
    Num_Entidades_Deuda: Number(raw.Num_Entidades_Deuda),
    Peor_Calificacion_12M: Number(raw.Peor_Calificacion_12M),
    Ingreso_CLP: Number(raw.Ingreso_CLP),
    Saldo_Total_CLP: Number(raw.Saldo_Total_CLP),
    Variacion_Endeudamiento: Number(raw.Variacion_Endeudamiento || 0),
  };

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      const msg = formatApiError(data.detail);
      formError.textContent =
        response.status === 422
          ? `Datos inválidos: ${msg}. Si persiste, reinicie la API con: uvicorn src.api.main:app --reload`
          : msg;
      formError.classList.remove("hidden");
      return;
    }

    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    window.location.assign("/resultado");
    return;
  } catch {
    formError.textContent = "No se pudo conectar con la API. Verifique que el servidor esté activo.";
    formError.classList.remove("hidden");
  } finally {
    btnCalcular.disabled = false;
    btnCalcular.textContent = "Calcular riesgo crediticio";
  }
});

checkHealth();
