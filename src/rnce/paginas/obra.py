from ..dominio import Obra
from ..visual import Html, juntar
from ..visual.escape import escapar
from .base import Contexto, Pagina


def em_linhas(titulo: str, largura: int = 9) -> list[str]:
    linhas: list[str] = []
    for palavra in titulo.split():
        if linhas and len(linhas[-1]) + 1 + len(palavra) <= largura:
            linhas[-1] += " " + palavra
        else:
            linhas.append(palavra)
    return linhas


class PaginaDeObra(Pagina):
    scripts = ("cartaz", "continuar")
    tipo_og = "book"

    def __init__(self, contexto: Contexto, obra: Obra):
        super().__init__(contexto)
        self.obra = obra

    @property
    def partes(self):
        return (self.obra.slug,)

    @property
    def titulo(self):
        return self.obra.titulo

    @property
    def descricao(self):
        return self.obra.sinopse[0] if self.obra.sinopse else super().descricao

    @property
    def secao_ativa(self):
        return self.obra.tipo

    def corpo(self) -> Html:
        o = self.obra
        return self.ctx.modelos.renderizar(
            "obra",
            slug=o.slug,
            secao=self.ctx.config.secoes[o.tipo].nome,
            capitulos_rotulo=o.rotulo_de_capitulos,
            titulo=o.titulo,
            titulo_em_linhas=juntar(
                Html(f'<span aria-hidden="true">{escapar(l)}</span>') for l in em_linhas(o.titulo)
            ),
            genero=o.genero or "—",
            ano=o.ano or "—",
            sinopse=juntar((Html(f"            <p>{escapar(p)}</p>") for p in o.sinopse), "\n"),
            avisos=self._avisos(),
            primeiro=self.link(o.slug, "1"),
            capitulos=juntar((self._linha_do_sumario(c) for c in o.capitulos), "\n"),
            outras=self._outras(),
        )

    def _avisos(self) -> Html:
        if not self.obra.avisos:
            return Html("")
        etiquetas = juntar(
            Html(f'<span class="tag av">{escapar(a.value)}</span>') for a in self.obra.avisos
        )
        return Html(
            '          <div class="aviso-box">\n'
            '            <p class="rot">aviso de conteúdo</p>\n'
            f'            <div class="tags">{etiquetas}</div>\n'
            "          </div>"
        )

    def _linha_do_sumario(self, capitulo) -> Html:
        sub = f"<small>{escapar(capitulo.subtitulo)}</small>" if capitulo.subtitulo else ""
        return Html(
            f'          <li><a href="{escapar(self.link(self.obra.slug, str(capitulo.numero)))}">'
            f'<span class="n">{capitulo.numero:02d}</span>'
            f"<span>{escapar(capitulo.titulo or self.obra.titulo)}{sub}</span></a></li>"
        )

    def _outras(self) -> Html:
        outras = [o for o in self.ctx.obras if o is not self.obra]
        if not outras:
            return Html("")
        cartoes = []
        for o in outras:
            genero = f'<span class="tag">{escapar(o.genero)}</span>' if o.genero else ""
            sinopse = f"<p>{escapar(o.sinopse[0])}</p>" if o.sinopse else ""
            cartoes.append(Html(
                f'          <a class="out" href="{escapar(self.link(o.slug))}">'
                f'<span class="rot">{escapar(self.ctx.config.secoes[o.tipo].nome)}</span>'
                f"<h3>{escapar(o.titulo)}</h3>{genero}{sinopse}"
                '<span class="ir">ler →</span></a>'
            ))
        return Html(
            '\n      <section class="outras">\n'
            '        <p class="rot">ler outra história</p>\n'
            '        <div class="oc">\n' + "\n".join(cartoes) + "\n        </div>\n      </section>"
        )
