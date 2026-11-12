from ..dominio import Acao, Capitulo, Fala, No, Nome, Paragrafo, Quebra, Subtitulo
from .escape import Html, escapar, juntar
from .separadores import EscolhedorDeSeparador, desenhar

_RECUO = " " * 12


class RenderizadorDeNos:
    """Desenha os nós de um capítulo. Um visitante por tipo de nó."""

    def __init__(self) -> None:
        self._separadores = EscolhedorDeSeparador()

    def capitulo(self, capitulo: Capitulo) -> Html:
        nos = (self.renderizar(no) for no in capitulo.nos)
        return Html(_RECUO + juntar(nos, "\n" + _RECUO))

    def renderizar(self, no: No) -> Html:
        metodo = getattr(self, f"_visitar_{type(no).__name__.lower()}", None)
        if metodo is None:
            raise TypeError(f"sem desenho para {type(no).__name__}")
        return metodo(no)

    def _visitar_paragrafo(self, no: Paragrafo) -> Html:
        return Html(f"<p>{self._com_quebras(no.texto)}</p>")

    def _visitar_fala(self, no: Fala) -> Html:
        return Html(f'<p class="fala">{self._com_quebras(no.texto)}</p>')

    def _visitar_nome(self, no: Nome) -> Html:
        return Html(f'<p class="nome">{escapar(no.texto)}</p>')

    def _visitar_acao(self, no: Acao) -> Html:
        return Html(f'<p class="acao">{escapar(no.texto)}</p>')

    def _visitar_subtitulo(self, no: Subtitulo) -> Html:
        return Html(f'<p class="sub">{escapar(no.texto)}</p>')

    def _visitar_quebra(self, no: Quebra) -> Html:
        return desenhar(self._separadores.proximo())

    @staticmethod
    def _com_quebras(texto: str) -> Html:
        return Html("<br>\n".join(escapar(linha) for linha in texto.split("\n")))
