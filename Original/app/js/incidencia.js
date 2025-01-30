// INCIDENCIAS.HTML - HABILITAR Y DESHABILITAR CAMPOS
document
  .getElementById("motivo_ausencia")
  .addEventListener("change", function () {
    const motivo = this.value;
    const numDias = document.getElementById("num_dias");
    const fechaInicio = document.getElementById("fecha_inicio");
    const fechaFin = document.getElementById("fecha_fin");
    const horaEntrada = document.getElementById("hora_entrada");
    const horaSalida = document.getElementById("hora_salida");
    const tiempo_x_tiempo = document.getElementById("tiempo_x_tiempo_fields");

    // Habilitar/Deshabilitar horas de entrada y salida
    if (
      [
        "goce_sueldo",
        "sin_goce_sueldo",
        "vacaciones",
        "olvido_gafete",
      ].includes(motivo)
    ) {
      numDias.disabled = false;
      fechaInicio.disabled = false;
      fechaFin.disabled = false;
      horaEntrada.disabled = true;
      horaSalida.disabled = true;
    } else if (["tiempo_x_tiempo"].includes(motivo)) {
      numDias.disabled = true;
      fechaInicio.disabled = true;
      fechaFin.disabled = true;
      horaEntrada.disabled = true;
      horaSalida.disabled = true;
    } else if (
      ["entrada_tarde", "salida_antes", "motivos_trabajo"].includes(motivo)
    ) {
      numDias.disabled = false;
      fechaInicio.disabled = false;
      fechaFin.disabled = false;
      horaEntrada.disabled = false;
      horaSalida.disabled = false;
    }

    // Mostrar/ocultar sección Tiempo x Tiempo
    if (motivo === "tiempo_x_tiempo") {
      tiempo_x_tiempo.style.display = "block";
    } else {
      tiempo_x_tiempo.style.display = "none";
    }
  });
