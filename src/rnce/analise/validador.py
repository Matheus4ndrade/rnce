import re

from ..dominio import ErroDeConteudo, Obra

TAMANHO_MAXIMO = 3 * 1024 * 1024
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUGS_RESERVADOS = frozenset({"folhetim", "volume", "tema", "assets", "404", "index"})
_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class ValidadorDeObra:
    """Melhor parar o build do que publicar obra quebrada."""

    def validar_texto(self, texto: str, arquivo: str) -> None:
        if len(texto.encode("utf-8")) > TAMANHO_MAXIMO:
            raise ErroDeConteudo(arquivo, "arquivo grande demais (máximo 3 MB)")
        achou = _CONTROLE.search(texto)
        if achou:
            linha = texto[: achou.start()].count("\n") + 1
            raise ErroDeConteudo(arquivo, "caractere de controle invisível no texto", linha)

    def validar_obra(self, obra: Obra, arquivo: str) -> None:
        if not SLUG.match(obra.slug):
            raise ErroDeConteudo(
                arquivo,
                "o nome do arquivo vira o endereço: use só letras minúsculas, "
                "números e hífen (ex.: entre-portas.rnce)",
            )
        if obra.slug in SLUGS_RESERVADOS:
            raise ErroDeConteudo(arquivo, f"`{obra.slug}` é um nome reservado do site")
        if not obra.titulo.strip():
            raise ErroDeConteudo(arquivo, "falta o campo `titulo:` no cabeçalho")
        if not obra.capitulos:
            raise ErroDeConteudo(arquivo, "a obra não tem nenhum texto")
        if all(not c.nos for c in obra.capitulos):
            raise ErroDeConteudo(arquivo, "os capítulos estão vazios")
