from ..visual import Html
from .base import Pagina


class PaginaNaoEncontrada(Pagina):
    partes = ()
    titulo = "Página não encontrada"
    arquivo = "404.html"

    @property
    def raiz(self) -> str:
        # O Pages serve esse arquivo em qualquer endereço, então ../ não serve.
        return self.ctx.config.caminho_base + "/"

    def corpo(self) -> Html:
        return self.ctx.modelos.renderizar("nao_encontrada", inicio=self.raiz)
