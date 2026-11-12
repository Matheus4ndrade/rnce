(function () {
  "use strict";

  var pagina = document.querySelector("article[data-obra]");
  if (!pagina) return;

  var prefs = window.RNCE.preferencias;
  var guardar = window.RNCE.guardar;
  var capitulo = parseInt(pagina.dataset.capitulo, 10);
  var chaveDaPosicao = "pos-" + pagina.dataset.obra;

  var texto = document.getElementById("texto");
  var ajustes = document.getElementById("ajustes");
  var botaoAjustes = document.getElementById("baj");
  var menu = document.getElementById("capmenu");
  var botaoMenu = document.getElementById("bcap");
  var barra = document.getElementById("prog");
  var aviso = document.getElementById("aviso");

  function todos(seletor, dentro) {
    return Array.prototype.slice.call((dentro || document).querySelectorAll(seletor));
  }

  function marcarOpcoes() {
    todos(".opt[data-k]", ajustes).forEach(function (botao) {
      var chave = botao.dataset.k;
      var ligado = chave === "foco"
        ? prefs.valores.foco
        : String(prefs.valores[chave]) === botao.dataset.v;
      botao.setAttribute("aria-pressed", String(ligado));
    });
    document.getElementById("tamv").textContent =
      Math.round((prefs.valores.tam / 1.2) * 100) + "%";
    texto.classList.toggle("foco", prefs.valores.foco);
  }

  function fecharAjustes() {
    ajustes.hidden = true;
    botaoAjustes.setAttribute("aria-expanded", "false");
  }

  function fecharMenu() {
    menu.classList.remove("aberto");
    botaoMenu.setAttribute("aria-expanded", "false");
  }

  botaoAjustes.addEventListener("click", function (evento) {
    evento.stopPropagation();
    var abrir = ajustes.hidden;
    ajustes.hidden = !abrir;
    botaoAjustes.setAttribute("aria-expanded", String(abrir));
    fecharMenu();
  });

  botaoMenu.addEventListener("click", function (evento) {
    evento.stopPropagation();
    var aberto = menu.classList.toggle("aberto");
    botaoMenu.setAttribute("aria-expanded", String(aberto));
    fecharAjustes();
  });

  ajustes.addEventListener("click", function (evento) {
    var botao = evento.target.closest("button");
    if (!botao) return;
    var tamanho = prefs.valores.tam;

    if (botao.dataset.k === "foco") prefs.mudar("foco", !prefs.valores.foco);
    else if (botao.dataset.k) prefs.mudar(botao.dataset.k, botao.dataset.v);
    else if (botao.dataset.a === "maior") prefs.mudar("tam", Math.min(2, Math.round((tamanho + 0.08) * 100) / 100));
    else if (botao.dataset.a === "menor") prefs.mudar("tam", Math.max(0.9, Math.round((tamanho - 0.08) * 100) / 100));
    else if (botao.dataset.a === "topo") window.scrollTo({ top: 0, behavior: "smooth" });
    else if (botao.dataset.a === "esquecer") {
      guardar.gravar(chaveDaPosicao, "");
      avisar("Posição esquecida.");
    }
    marcarOpcoes();
    aoRolar();
  });

  document.addEventListener("click", function (evento) {
    if (!ajustes.hidden && !ajustes.contains(evento.target)) fecharAjustes();
    if (menu.classList.contains("aberto") && !menu.contains(evento.target)) fecharMenu();
  });

  var relogioDoAviso;

  function avisar(mensagem, botoes) {
    clearTimeout(relogioDoAviso);
    aviso.textContent = "";
    var frase = document.createElement("span");
    frase.textContent = mensagem;
    aviso.appendChild(frase);
    (botoes || []).forEach(function (b) {
      var botao = document.createElement("button");
      botao.textContent = b.texto;
      if (b.discreto) botao.className = "sec";
      botao.addEventListener("click", function () {
        aviso.hidden = true;
        if (b.acao) b.acao();
      });
      aviso.appendChild(botao);
    });
    aviso.hidden = false;
    if (!botoes) relogioDoAviso = setTimeout(function () { aviso.hidden = true; }, 2200);
  }

  function alturaRolavel() {
    return document.documentElement.scrollHeight - window.innerHeight;
  }

  function semAnimacao(acao) {
    var raiz = document.documentElement;
    raiz.style.scrollBehavior = "auto";
    acao();
    setTimeout(function () { raiz.style.scrollBehavior = ""; }, 50);
  }

  function destacarParagrafoDoMeio() {
    var meio = window.innerHeight * 0.42;
    var escolhido = null;
    var menorDistancia = Infinity;
    todos("p", texto).forEach(function (p) {
      var caixa = p.getBoundingClientRect();
      if (caixa.bottom < 0 || caixa.top > window.innerHeight) return;
      var distancia = Math.abs((caixa.top + caixa.bottom) / 2 - meio);
      if (distancia < menorDistancia) {
        menorDistancia = distancia;
        escolhido = p;
      }
    });
    todos("p.atual", texto).forEach(function (p) {
      if (p !== escolhido) p.classList.remove("atual");
    });
    if (escolhido) escolhido.classList.add("atual");
  }

  function aoRolar() {
    var maximo = alturaRolavel();
    var fracao = maximo > 0 ? Math.min(1, window.scrollY / maximo) : 0;
    barra.style.width = fracao * 100 + "%";
    if (prefs.valores.foco) destacarParagrafoDoMeio();
    if (window.scrollY > 200) {
      guardar.gravar(chaveDaPosicao, JSON.stringify({
        c: capitulo,
        p: Math.round(fracao * 10000) / 10000
      }));
    }
  }

  // sem isso o scroll dispara o cálculo umas 60x por segundo
  var esperando = false;
  window.addEventListener("scroll", function () {
    if (esperando) return;
    esperando = true;
    requestAnimationFrame(function () {
      esperando = false;
      aoRolar();
    });
  }, { passive: true });

  function oferecerContinuar() {
    var guardado;
    try {
      guardado = JSON.parse(guardar.ler(chaveDaPosicao, ""));
    } catch (erro) {
      return;
    }
    if (!guardado || guardado.c !== capitulo) return;
    var fracao = Number(guardado.p);
    if (!(fracao > 0.02 && fracao < 0.985)) return;

    avisar("Você parou em " + Math.round(fracao * 100) + "% deste capítulo.", [
      { texto: "continuar", acao: function () {
          semAnimacao(function () { window.scrollTo(0, alturaRolavel() * fracao); });
        } },
      { texto: "do início", discreto: true }
    ]);
  }

  function observarQuebras() {
    var quebras = todos(".quebra");
    if (!("IntersectionObserver" in window)) {
      quebras.forEach(function (q) { q.classList.add("visivel"); });
      return;
    }
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("visivel");
        observador.unobserve(entrada.target);
      });
    }, { threshold: 0.4 });
    quebras.forEach(function (q) { observador.observe(q); });
  }

  document.addEventListener("keydown", function (evento) {
    if (evento.key === "Escape") {
      fecharAjustes();
      fecharMenu();
      return;
    }
    if (evento.ctrlKey || evento.metaKey || evento.altKey) return;
    if (evento.target.closest("input, textarea, button")) return;
    var destino = null;
    if (evento.key === "ArrowRight") destino = document.querySelector('a[rel="next"]');
    if (evento.key === "ArrowLeft") destino = document.querySelector('a[rel="prev"]');
    if (destino) window.location.href = destino.href;
  });

  marcarOpcoes();
  observarQuebras();
  aoRolar();
  oferecerContinuar();

  var atual = menu.querySelector('a[aria-current="page"]');
  if (atual && window.innerWidth > 900) {
    var lista = atual.closest("ol");
    lista.scrollTop = atual.offsetTop - lista.offsetTop - 20;
  }
})();
