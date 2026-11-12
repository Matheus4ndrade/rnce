from pathlib import Path
from string import Template

from .escape import Html, escapar


class Modelos:
    """Moldes de tema/templates. $nome é onde entra valor."""

    def __init__(self, pasta: Path):
        self._pasta = pasta
        self._cache: dict[str, Template] = {}

    def renderizar(self, modelo_nome: str, /, **valores: object) -> Html:
        modelo = self._cache.get(modelo_nome)
        if modelo is None:
            modelo = Template((self._pasta / f"{modelo_nome}.html").read_text(encoding="utf-8"))
            self._cache[modelo_nome] = modelo
        return Html(modelo.substitute({k: escapar(v) for k, v in valores.items()}))
