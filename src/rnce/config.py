import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .dominio import Tipo
from .visual.escape import so_se_http


@dataclass(frozen=True)
class Secao:
    tipo: Tipo
    nome: str
    rotulo: str
    texto: str
    vazio: str


@dataclass(frozen=True)
class Inicio:
    rotulo: str
    titulo: str
    paragrafos: tuple[str, ...]


@dataclass(frozen=True)
class Config:
    nome: str
    descricao: str
    autor: str
    instagram: str
    ano: str
    url: str
    inicio: Inicio
    secoes: dict[Tipo, Secao]

    @property
    def caminho_base(self) -> str:
        """`/rnce` em usuario.github.io/rnce; vazio se o site está na raiz."""
        return urlparse(self.url).path.rstrip("/") if self.url else ""


def carregar(arquivo: Path) -> Config:
    dados = tomllib.loads(arquivo.read_text(encoding="utf-8"))
    site, inicio = dados["site"], dados["inicio"]

    secoes = {}
    for tipo in Tipo:
        s = dados["secoes"][tipo.value]
        secoes[tipo] = Secao(tipo, s["nome"], s["rotulo"], s["texto"], s["vazio"])

    url = site.get("url", "").strip()
    if url:
        so_se_http(url)

    return Config(
        nome=site["nome"],
        descricao=site["descricao"],
        autor=site["autor"],
        instagram=so_se_http(site["instagram"]),
        ano=str(site["ano"]),
        url=url,
        inicio=Inicio(inicio["rotulo"], inicio["titulo"], tuple(inicio["paragrafos"])),
        secoes=secoes,
    )
