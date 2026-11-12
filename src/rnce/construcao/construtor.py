from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from xml.sax.saxutils import escape as escapar_xml

from .. import config as leitor_de_config
from ..dominio import Tipo
from ..paginas import (
    Contexto, Pagina, PaginaDeCapitulo, PaginaDeObra, PaginaDeSecao,
    PaginaInicial, PaginaNaoEncontrada,
)
from ..visual import Modelos, tatreez
from .repositorio import RepositorioDeObras
from .saida import SaidaEmDisco


@dataclass(frozen=True)
class Resultado:
    obras: int
    paginas: int
    pasta: Path


class ConstrutorDoSite:
    def __init__(self, raiz: Path, saida: Path | None = None):
        self._conteudo = raiz / "conteudo"
        self._tema = raiz / "tema"
        self._saida = SaidaEmDisco(saida or raiz / "dist")

    def construir(self) -> Resultado:
        contexto = Contexto(
            config=leitor_de_config.carregar(self._conteudo / "site.toml"),
            obras=RepositorioDeObras(self._conteudo / "obras").todas(),
            modelos=Modelos(self._tema / "templates"),
        )
        # renderiza tudo antes de apagar o dist antigo, senão um erro no meio
        # me deixa sem site nenhum
        paginas = [(p.arquivo, p.renderizar()) for p in self._paginas(contexto)]

        self._saida.limpar()
        for arquivo, html in paginas:
            self._saida.escrever(arquivo, html)
        self._copiar_tema()
        self._arquivos_do_servidor(contexto, [a for a, _ in paginas])
        return Resultado(len(contexto.obras), len(paginas), self._saida.pasta)

    @staticmethod
    def _paginas(ctx: Contexto) -> Iterator[Pagina]:
        yield PaginaInicial(ctx)
        yield PaginaNaoEncontrada(ctx)
        for tipo in Tipo:
            yield PaginaDeSecao(ctx, tipo)
        for obra in ctx.obras:
            yield PaginaDeObra(ctx, obra)
            for capitulo in obra.capitulos:
                yield PaginaDeCapitulo(ctx, obra, capitulo)

    def _copiar_tema(self) -> None:
        for pasta in ("css", "js", "fontes"):
            self._saida.copiar_pasta(self._tema / pasta, f"tema/{pasta}")
        self._saida.escrever("tema/css/tatreez.css", tatreez.css())
        self._saida.escrever(
            "tema/favicon.svg", (self._tema / "favicon.svg").read_text(encoding="utf-8")
        )

    def _arquivos_do_servidor(self, ctx: Contexto, arquivos: list[str]) -> None:
        self._saida.escrever(".nojekyll", "")
        url = ctx.config.url.rstrip("/")
        if not url:
            return
        enderecos = sorted(
            a.removesuffix("index.html") for a in arquivos if a.endswith("index.html")
        )
        linhas = "".join(f"  <url><loc>{escapar_xml(f'{url}/{e}')}</loc></url>\n" for e in enderecos)
        self._saida.escrever(
            "sitemap.xml",
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{linhas}</urlset>\n",
        )
        self._saida.escrever("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {url}/sitemap.xml\n")
