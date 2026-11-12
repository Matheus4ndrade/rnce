from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..config import Config
from ..dominio import Obra, Tipo
from ..visual import Html, Modelos, juntar, tatreez
from ..visual.escape import escapar


@dataclass(frozen=True)
class Contexto:
    config: Config
    obras: tuple[Obra, ...]
    modelos: Modelos

    def obras_de(self, tipo: Tipo) -> tuple[Obra, ...]:
        return tuple(o for o in self.obras if o.tipo is tipo)


class Pagina(ABC):
    """Moldura comum (topo, menu, rodapé). Cada página define corpo() e endereço."""

    scripts: tuple[str, ...] = ()
    tipo_og = "website"

    def __init__(self, contexto: Contexto):
        self.ctx = contexto

    @property
    @abstractmethod
    def partes(self) -> tuple[str, ...]:
        """Pastas do endereço: ("entre-portas", "2") -> /entre-portas/2/."""

    @property
    @abstractmethod
    def titulo(self) -> str: ...

    @abstractmethod
    def corpo(self) -> Html: ...

    @property
    def descricao(self) -> str:
        return self.ctx.config.descricao

    @property
    def secao_ativa(self) -> Tipo | None:
        return None

    @property
    def arquivo(self) -> str:
        return "/".join((*self.partes, "index.html"))

    @property
    def raiz(self) -> str:
        return "../" * len(self.partes)

    def link(self, *partes) -> str:
        return self.raiz + "".join(f"{p}/" for p in partes) or "./"

    def renderizar(self) -> str:
        cfg = self.ctx.config
        titulo = cfg.nome if not self.titulo else f"{self.titulo} — {cfg.nome}"
        return self.ctx.modelos.renderizar(
            "base",
            titulo=titulo,
            descricao=self.descricao,
            tipo_og=self.tipo_og,
            raiz=self.raiz,
            inicio=self.link(),
            nome_do_site=cfg.nome,
            traco_do_logo=tatreez.caminho_do_traco_cufico(),
            menu=self._menu(),
            corpo=self.corpo(),
            ano=cfg.ano,
            instagram=cfg.instagram,
            autor=cfg.autor,
            scripts=juntar(
                Html(f'  <script src="{escapar(self.raiz)}tema/js/{escapar(s)}.js" defer></script>\n')
                for s in self.scripts
            ),
        )

    def _menu(self) -> Html:
        itens = []
        for tipo, secao in self.ctx.config.secoes.items():
            ativo = ' class="on" aria-current="page"' if tipo is self.secao_ativa else ""
            itens.append(Html(
                f'        <a href="{escapar(self.link(tipo.value))}"{ativo}>{escapar(secao.nome)}</a>'
            ))
        return juntar(itens, "\n")
