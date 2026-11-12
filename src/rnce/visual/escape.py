"""str é conteúdo e sempre escapa. Só Html passa direto, e só o renderizador
cria Html. Dessa forma não tem como eu esquecer o escape em algum canto."""
import html
from typing import Iterable


class Html(str):
    __slots__ = ()


def escapar(valor) -> Html:
    if isinstance(valor, Html):
        return valor
    return Html(html.escape(str(valor), quote=True))


def juntar(partes: Iterable, separador: str = "") -> Html:
    return Html(separador.join(escapar(p) for p in partes))


def so_se_http(endereco: str) -> str:
    e = endereco.strip()
    if not e.lower().startswith(("https://", "http://")):
        raise ValueError(f"endereço não permitido: {endereco!r}")
    return e
