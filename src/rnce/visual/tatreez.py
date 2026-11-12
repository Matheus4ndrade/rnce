"""Tatreez em SVG, vira data: url no CSS. Nenhuma imagem no repo."""
from urllib.parse import quote

VERMELHO, VERDE, BRANCO = "#d42a3c", "#1f9a57", "#ecebe4"


def _ponto_cruz(celulas: list[tuple[int, int, str]], largura: int, altura: int, lado: int) -> str:
    quadros = "".join(
        f'<rect x="{x * lado}" y="{y * lado}" width="{lado}" height="{lado}" fill="{cor}"/>'
        for x, y, cor in celulas
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura * lado}" '
        f'height="{altura * lado}" shape-rendering="crispEdges">{quadros}</svg>'
    )
    return f'url("data:image/svg+xml;utf8,{quote(svg)}")'


def _faixa_do_titulo() -> str:
    celulas = []
    for i in range(9):
        for j in range(9):
            d = abs(i - 4) + abs(j - 4)
            cor = {4: VERMELHO, 2: VERDE, 0: BRANCO}.get(d)
            if cor:
                celulas.append((i, j, cor))
    celulas += [(11, 4, BRANCO), (11, 3, VERDE), (11, 5, VERDE), (10, 4, VERDE), (12, 4, VERDE)]
    return _ponto_cruz(celulas, 13, 9, 3)


def caminho_do_traco_cufico() -> str:
    caminho = "M0 9"
    for i in range(20):
        caminho += f" h5 v{4 if i % 2 else -4}"
    return caminho


def css() -> str:
    return (
        "/* Gerado por rnce/visual/tatreez.py. */\n"
        ":root{\n"
        f"  --tz-band:{_faixa_do_titulo()};\n"
        "}\n"
    )
