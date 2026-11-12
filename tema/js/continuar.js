(function () {
  "use strict";

  var link = document.getElementById("continuar");
  if (!link) return;

  var guardado;
  try {
    guardado = JSON.parse(window.RNCE.guardar.ler("pos-" + link.dataset.obra, ""));
  } catch (erro) {
    return;
  }
  var capitulo = guardado && parseInt(guardado.c, 10);
  if (!capitulo || capitulo < 1) return;

  link.href = link.href.replace(/1\/$/, capitulo + "/");
  link.textContent = "continuar do capítulo " + capitulo;
  link.hidden = false;
})();
