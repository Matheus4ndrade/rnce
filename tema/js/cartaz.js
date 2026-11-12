/* Ajusta cada linha do título à largura do cartaz. */
(function () {
  "use strict";

  var titulo = document.querySelector(".poster h1");
  if (!titulo) return;

  function ajustar() {
    var largura = titulo.clientWidth;
    if (!largura) return;
    Array.prototype.forEach.call(titulo.querySelectorAll("span"), function (linha, i) {
      var recuo = i % 2 ? 0.13 : 0; // linha par entra um pouco, fica menos quadrado
      linha.style.fontSize = "100px";
      linha.style.marginLeft = "0";
      var medida = linha.getBoundingClientRect().width || 1;
      var tamanho = (100 * largura * (1 - recuo) * 0.97) / medida;
      linha.style.fontSize = Math.max(30, Math.min(176, tamanho)) + "px";
      linha.style.marginLeft = recuo * largura + "px";
    });
  }

  ajustar();
  window.addEventListener("resize", ajustar);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajustar);
})();
