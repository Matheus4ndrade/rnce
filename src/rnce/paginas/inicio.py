import re

from ..visual import Html, juntar
from ..visual.escape import escapar
from .base import Pagina

_DESTAQUE = re.compile(r"\*([^*\n]+)\*")


def com_destaques(texto: str) -> Html:
    return Html(_DESTAQUE.sub(r"<em>\1</em>", escapar(texto)))


def contar_obras(n: int) -> str:
    return f"{n} obra" if n == 1 else f"{n} obras"


class PaginaInicial(Pagina):
    partes = ()
    titulo = ""

    def corpo(self) -> Html:
        inicio = self.ctx.config.inicio
        secoes = juntar(
            self.ctx.modelos.renderizar(
                "inicio_secao",
                link=self.link(tipo.value),
                rotulo=secao.rotulo,
                nome=secao.nome,
                texto=secao.texto,
                quantas=contar_obras(len(self.ctx.obras_de(tipo))),
            )
            for tipo, secao in self.ctx.config.secoes.items()
        )
        return self.ctx.modelos.renderizar(
            "inicio",
            rotulo=inicio.rotulo,
            titulo=inicio.titulo,
            paragrafos=juntar(
                (Html(f"        <p>{com_destaques(p)}</p>") for p in inicio.paragrafos), "\n"
            ),
            secoes=secoes,
        )
