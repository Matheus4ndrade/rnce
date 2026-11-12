from ..dominio import Capitulo, Obra, Tipo
from ..visual import Html, RenderizadorDeNos, juntar
from ..visual.escape import escapar
from ..visual.separadores import Filigrana, desenhar
from .base import Contexto, Pagina

_RECUO = " " * 12


class PaginaDeCapitulo(Pagina):
    scripts = ("leitura",)
    tipo_og = "article"

    def __init__(self, contexto: Contexto, obra: Obra, capitulo: Capitulo):
        super().__init__(contexto)
        self.obra = obra
        self.capitulo = capitulo

    @property
    def partes(self):
        return (self.obra.slug, str(self.capitulo.numero))

    @property
    def titulo(self):
        if self.capitulo.titulo:
            return f"{self.capitulo.titulo} · {self.obra.titulo}"
        return self.obra.titulo

    @property
    def descricao(self):
        return self.obra.sinopse[0] if self.obra.sinopse else super().descricao

    @property
    def secao_ativa(self):
        return self.obra.tipo

    def corpo(self) -> Html:
        o, c = self.obra, self.capitulo
        titulo = Html(f'            <h1 class="tit">{escapar(c.titulo)}</h1>') if c.titulo else Html("")
        return self.ctx.modelos.renderizar(
            "capitulo",
            slug=o.slug,
            numero=c.numero,
            link_secao=self.link(o.tipo.value),
            secao=self.ctx.config.secoes[o.tipo].nome,
            link_obra=self.link(o.slug),
            obra=o.titulo,
            posicao=f"{c.numero} de {len(o.capitulos)}",
            ajustes=self.ctx.modelos.renderizar("ajustes"),
            titulo=titulo,
            texto=RenderizadorDeNos().capitulo(c),
            rodape=self._rodape(),
            menu=juntar((self._item_do_menu(x) for x in o.capitulos), "\n"),
        )

    def _link_do_capitulo(self, numero: int) -> str:
        return self.link(self.obra.slug, str(numero))

    def _rodape(self) -> Html:
        o, c = self.obra, self.capitulo
        partes: list[Html] = [desenhar(Filigrana(), grande=True)]
        navegacao = []
        if c.numero > 1:
            anterior = o.capitulo(c.numero - 1)
            navegacao.append(Html(
                f'<a class="ant" rel="prev" href="{escapar(self._link_do_capitulo(anterior.numero))}">'
                f"<span>←</span> {escapar(anterior.titulo or 'anterior')}</a>"
            ))
        if c.numero < len(o.capitulos):
            proximo = o.capitulo(c.numero + 1)
            navegacao.append(Html(
                f'<a class="prox" rel="next" href="{escapar(self._link_do_capitulo(proximo.numero))}">'
                f"próximo capítulo <span>→</span> {escapar(proximo.titulo)}</a>"
            ))
        else:
            fim = (
                "fim do capítulo · o próximo ainda não saiu"
                if o.tipo is Tipo.FOLHETIM else "fim"
            )
            partes.append(Html(f'<p class="fim-obra">{fim}</p>'))
        if navegacao:
            partes.append(Html('<nav class="passos" aria-label="Capítulo anterior e próximo">'
                               + "".join(navegacao) + "</nav>"))
        return Html(_RECUO + juntar(partes, "\n" + _RECUO))

    def _item_do_menu(self, capitulo: Capitulo) -> Html:
        atual = ' class="on" aria-current="page"' if capitulo is self.capitulo else ""
        sub = f"<small>{escapar(capitulo.subtitulo)}</small>" if capitulo.subtitulo else ""
        return Html(
            f'              <li><a href="{escapar(self._link_do_capitulo(capitulo.numero))}"{atual}>'
            f'<span class="n">{capitulo.numero:02d}</span>'
            f"<span>{escapar(capitulo.titulo or self.obra.titulo)}{sub}</span></a></li>"
        )
