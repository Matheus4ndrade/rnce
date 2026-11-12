import re

_CABECALHO = re.compile(r"\A---\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)
_CAMPO = re.compile(r"^(\w+)\s*:\s*(.*)$")


def separar(texto: str) -> tuple[dict[str, list[str]], str, int]:
    """(campos, corpo, linhas do cabeçalho).

    Cada campo é uma lista porque `sinopse:` pode repetir.
    """
    achou = _CABECALHO.match(texto)
    if not achou:
        return {}, texto, 0
    campos: dict[str, list[str]] = {}
    for linha in achou.group(1).split("\n"):
        campo = _CAMPO.match(linha)
        if not campo:
            continue
        nome = campo.group(1).lower()
        valor = campo.group(2).strip()
        if len(valor) >= 2 and valor[0] == valor[-1] == '"':
            valor = valor[1:-1]
        campos.setdefault(nome, []).append(valor)
    return campos, texto[achou.end():], texto[: achou.end()].count("\n")
