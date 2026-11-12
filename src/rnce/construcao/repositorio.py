from pathlib import Path

from ..analise import AnalisadorRnce
from ..dominio import ErroDeConteudo, Obra

EXTENSOES = (".rnce", ".md")


class RepositorioDeObras:
    def __init__(self, pasta: Path, analisador: AnalisadorRnce | None = None):
        self._pasta = pasta
        self._analisador = analisador or AnalisadorRnce()

    def todas(self) -> tuple[Obra, ...]:
        arquivos = sorted(
            a for a in self._pasta.iterdir()
            if a.is_file() and a.suffix in EXTENSOES and not a.name.startswith((".", "_"))
        )
        obras: list[Obra] = []
        vistos: dict[str, str] = {}
        for arquivo in arquivos:
            slug = arquivo.stem
            if slug in vistos:
                raise ErroDeConteudo(arquivo.name, f"mesmo endereço que {vistos[slug]}")
            vistos[slug] = arquivo.name
            try:
                texto = arquivo.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                raise ErroDeConteudo(arquivo.name, "o arquivo precisa estar em UTF-8") from None
            obras.append(self._analisador.analisar(texto, slug, arquivo.name))
        return tuple(sorted(obras, key=lambda o: (o.ordem, o.slug)))
