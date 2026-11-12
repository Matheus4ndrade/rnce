from abc import ABC, abstractmethod

from .escape import Html


class Separador(ABC):
    @abstractmethod
    def tracos(self) -> str:
        """Conteúdo do <svg>, viewBox 0 0 320 30."""


class Filigrana(Separador):
    def tracos(self) -> str:
        return (
            '<path d="M8 15H128M192 15H312"/>'
            '<rect x="-8" y="-8" width="16" height="16" transform="translate(160 15)"/>'
            '<rect x="-8" y="-8" width="16" height="16" transform="translate(160 15) rotate(45)"/>'
            '<rect class="f" x="-2.5" y="-2.5" width="5" height="5" transform="translate(160 15) rotate(45)"/>'
            '<rect class="f" x="-3" y="-3" width="6" height="6" transform="translate(8 15) rotate(45)"/>'
            '<rect class="f" x="-3" y="-3" width="6" height="6" transform="translate(312 15) rotate(45)"/>'
        )


class Zigue(Separador):
    def tracos(self) -> str:
        d, x, sobe = "M20 24", 20, True
        while x < 300:
            d += f"h16v{-14 if sobe else 14}"
            sobe = not sobe
            x += 16
        return f'<path d="{d}"/><path class="v" d="M148 4h24"/>'


class Arcos(Separador):
    def tracos(self) -> str:
        arcos = "".join(
            f'<path d="M{62 + k * 30} 26v-9a8 8 0 0 1 16 0v9"/>' for k in range(7)
        )
        return (
            arcos
            + '<rect class="f" x="-2.5" y="-2.5" width="5" height="5" transform="translate(160 4) rotate(45)"/>'
            + '<path d="M20 26H300" class="v"/>'
        )


class Losangos(Separador):
    def tracos(self) -> str:
        partes = []
        for q in range(9):
            cx = 40 + q * 30
            r = 9 if q == 4 else 5
            cor = 'class="v" ' if q % 2 else ""
            partes.append(
                f'<rect {cor}x="{-r}" y="{-r}" width="{2 * r}" height="{2 * r}" '
                f'transform="translate({cx} 15) rotate(45)"/>'
            )
        return "".join(partes)


class EscolhedorDeSeparador:
    """Vai alternando entre os desenhos dentro do capítulo."""

    _VARIANTES = (Filigrana(), Zigue(), Arcos(), Losangos())

    def __init__(self) -> None:
        self._proximo = 0

    def proximo(self) -> Separador:
        s = self._VARIANTES[self._proximo % len(self._VARIANTES)]
        self._proximo += 1
        return s


def desenhar(separador: Separador, grande: bool = False) -> Html:
    classe = "quebra grande" if grande else "quebra"
    return Html(
        f'<div class="{classe}" role="separator">'
        f'<svg viewBox="0 0 320 30" aria-hidden="true">{separador.tracos()}</svg></div>'
    )
