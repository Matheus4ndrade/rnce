/* Preferências de leitura. Carrega no <head> para o tema não piscar. */
(function () {
  "use strict";

  var FONTES = {
    serif: '"Spectral", Georgia, serif',
    sans: 'system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    mono: "ui-monospace, Menlo, Consolas, monospace",
    kufi: '"Reem Kufi", "Spectral", sans-serif',
    cal: '"Aref Ruqaa", "Spectral", serif'
  };
  var LARGURAS = { e: "30rem", m: "36rem", l: "46rem" };
  var ESPACOS = { c: "1.5", m: "1.75", s: "2.05" };
  var TEMAS = ["escuro", "claro", "sepia"];

  var guardar = {
    ler: function (chave, padrao) {
      try {
        var valor = localStorage.getItem("rnce-" + chave);
        return valor === null ? padrao : valor;
      } catch (erro) {
        return padrao;
      }
    },
    gravar: function (chave, valor) {
      try { localStorage.setItem("rnce-" + chave, valor); } catch (erro) { /* modo privado */ }
    }
  };

  function daLista(valor, lista, padrao) {
    return Object.prototype.hasOwnProperty.call(lista, valor) ? valor : padrao;
  }

  var tamanho = parseFloat(guardar.ler("tam", "1.2"));
  var valores = {
    tam: tamanho >= 0.9 && tamanho <= 2 ? tamanho : 1.2,
    fonte: daLista(guardar.ler("fonte", "serif"), FONTES, "serif"),
    tema: TEMAS.indexOf(guardar.ler("tema", "escuro")) >= 0 ? guardar.ler("tema", "escuro") : "escuro",
    larg: daLista(guardar.ler("larg", "m"), LARGURAS, "m"),
    esp: daLista(guardar.ler("esp", "m"), ESPACOS, "m"),
    foco: guardar.ler("foco", "0") === "1"
  };

  function aplicar() {
    var raiz = document.documentElement;
    raiz.setAttribute("data-tema", valores.tema);
    raiz.style.setProperty("--tam", valores.tam + "rem");
    raiz.style.setProperty("--leitura", FONTES[valores.fonte]);
    raiz.style.setProperty("--medida", LARGURAS[valores.larg]);
    raiz.style.setProperty("--lh", ESPACOS[valores.esp]);
  }

  function mudar(chave, valor) {
    valores[chave] = valor;
    guardar.gravar(chave, chave === "foco" ? (valor ? "1" : "0") : valor);
    aplicar();
  }

  document.documentElement.classList.add("js");
  aplicar();

  window.RNCE = { preferencias: { valores: valores, mudar: mudar }, guardar: guardar };
})();
