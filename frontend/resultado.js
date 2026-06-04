const sinDatos = document.getElementById("resultado-sin-datos");
const contenido = document.getElementById("resultado-contenido");
const estadoApi = document.getElementById("estado-api");

async function init() {
  const raw = sessionStorage.getItem(STORAGE_KEY);

  if (!raw) {
    sinDatos.classList.remove("hidden");
    return;
  }

  try {
    const data = JSON.parse(raw);
    renderResultPage(data);
    contenido.classList.remove("hidden");
    estadoApi.textContent = `Evaluación · ${data.modelo}`;
    estadoApi.style.background = "rgba(16, 185, 129, 0.18)";
  } catch {
    sinDatos.classList.remove("hidden");
    contenido.classList.add("hidden");
  }
}

init();
