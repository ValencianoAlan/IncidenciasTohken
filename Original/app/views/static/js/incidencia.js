document.addEventListener("DOMContentLoaded", function () {
    const motivoAusencia = document.getElementById("motivo_ausencia");
    const horaFields = document.querySelectorAll(".hora-fields");

    motivoAusencia.addEventListener("change", function () {
      const motivo = this.value;

      // Motivos que ocultan los campos de hora
      const motivosOcultar = [
        "goce_sueldo",
        "sin_goce_sueldo",
        "vacaciones",
        "olvido_gafete",
        "tiempo_x_tiempo",
      ];

      if (motivosOcultar.includes(motivo)) {
        horaFields.forEach((field) => {
          field.style.display = "none";
        });
      } else if (motivo === "motivos_trabajo") {
        horaFields.forEach((field) => {
          field.style.display = "block";
        });
      }
    });

    // Ejecutar el cambio al cargar la página para establecer el estado inicial
    motivoAusencia.dispatchEvent(new Event("change"));
  });
