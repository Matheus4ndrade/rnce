from ..dominio import Obra, Tipo
from ..visual import Html, juntar
from ..visual.escape import escapar
from .base import Contexto, Pagina


def etiquetas_da_obra(obra: Obra) -> Html:
    textos = [t for t in (obra.genero, obra.ano, obra.rotulo_de_capitulos) if t]
    return juntar(Html(f'<span class="tag">{escapar(t)}</span>') for t in textos)


class PaginaDeSecao(Pagina):
    def __init__(self, contexto: Contexto, tipo: Tipo):
        super().__init__(contexto)
        self.tipo = tipo
        self.secao = contexto.config.secoes[tipo]

    @property
    def partes(self):
        return (self.tipo.value,)

    @property
    def titulo(self):
        return self.secao.nome

    @property
    def descricao(self):
        return self.secao.texto

    @property
    def secao_ativa(self):
        return self.tipo

    def corpo(self) -> Html:
        obras = self.ctx.obras_de(self.tipo)
        if obras:
            itens = juntar(self._item(i, o) for i, o in enumerate(obras, start=1))
        else:
            itens = Html(f'      <p class="vazio">{escapar(self.secao.vazio)}</p>')
        return self.ctx.modelos.renderizar(
            "lista",
            nome=self.secao.nome,
            rotulo=self.secao.rotulo,
            texto=self.secao.texto,
            itens=itens,
        )

    def _item(self, numero: int, obra: Obra) -> Html:
        sinopse = Html(f"          <p>{escapar(obra.sinopse[0])}</p>") if obra.sinopse else Html("")
        return self.ctx.modelos.renderizar(
            "lista_item",
            link=self.link(obra.slug),
            numero=f"{numero:02d}",
            titulo=obra.titulo,
            etiquetas=etiquetas_da_obra(obra),
            sinopse=sinopse,
        )
