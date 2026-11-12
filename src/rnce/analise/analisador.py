import re
from typing import Callable

from ..dominio import (
    Acao, Aviso, Capitulo, ErroDeConteudo, Fala, No, Nome, Obra, Paragrafo,
    Quebra, Subtitulo, Tipo,
)
from . import frontmatter
from .validador import ValidadorDeObra

_MARCA = re.compile(
    r"^\*(?P<marca>[a-z]+)\*[ \t]*(?P<texto>.*?)"
    r"(?:[ \t]*\*(?:tit|sub|acao|nome|ti|su)\*)?\s*$",
    re.IGNORECASE | re.DOTALL,
)
_QUEBRA = re.compile(r"^\*{3,}$")
_MARCAS_CONHECIDAS = ("tit", "sub", "acao", "nome")


class _Rascunho:
    def __init__(self, titulo: str):
        self.titulo = titulo
        self.nos: list[No] = []


class AnalisadorRnce:
    """Lê um .rnce e devolve a Obra. Bloco = trecho entre linhas em branco."""

    def __init__(self, validador: ValidadorDeObra | None = None):
        self._validador = validador or ValidadorDeObra()
        self._tratadores: dict[str, Callable[[str, "_Estado"], None]] = {
            "tit": self._titulo,
            "sub": self._subtitulo,
            "acao": self._acao,
            "nome": self._nome,
        }

    def analisar(self, texto: str, slug: str, arquivo: str | None = None) -> Obra:
        arquivo = arquivo or f"{slug}.rnce"
        self._validador.validar_texto(texto, arquivo)
        texto = texto.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿ \t\n")

        campos, corpo, linhas_do_cabecalho = frontmatter.separar(texto)
        estado = _Estado(arquivo)
        for numero_da_linha, bloco in self._blocos(corpo, linhas_do_cabecalho):
            estado.linha = numero_da_linha
            self._tratar_bloco(bloco, estado)

        obra = self._montar_obra(slug, campos, estado, arquivo)
        self._validador.validar_obra(obra, arquivo)
        return obra

    @staticmethod
    def _blocos(corpo: str, deslocamento: int):
        atual: list[str] = []
        inicio = 0
        for i, linha in enumerate(corpo.split("\n")):
            if linha.strip():
                if not atual:
                    inicio = i
                atual.append(linha.rstrip())
            elif atual:
                yield inicio + deslocamento + 1, "\n".join(atual).strip()
                atual = []
        if atual:
            yield inicio + deslocamento + 1, "\n".join(atual).strip()

    def _tratar_bloco(self, bloco: str, estado: "_Estado") -> None:
        if _QUEBRA.match(bloco):
            estado.adicionar(Quebra())
            return
        marca = _MARCA.match(bloco)
        if marca:
            nome = marca.group("marca").lower()
            if nome not in _MARCAS_CONHECIDAS:
                raise ErroDeConteudo(
                    estado.arquivo,
                    f"marca desconhecida *{nome}*. As marcas são: "
                    + ", ".join(f"*{m}*" for m in _MARCAS_CONHECIDAS),
                    estado.linha,
                )
            texto = re.sub(r"\s*\n\s*", " ", marca.group("texto")).strip()
            self._tratadores[nome](texto, estado)
            return
        if estado.depois_de_nome:
            estado.adicionar(Fala(bloco))
        else:
            estado.adicionar(Paragrafo(bloco))

    def _titulo(self, texto: str, estado: "_Estado") -> None:
        estado.novo_capitulo(texto)

    def _subtitulo(self, texto: str, estado: "_Estado") -> None:
        estado.adicionar(Subtitulo(texto))

    def _acao(self, texto: str, estado: "_Estado") -> None:
        estado.adicionar(Acao(texto))

    def _nome(self, texto: str, estado: "_Estado") -> None:
        estado.adicionar(Nome(texto))

    def _montar_obra(self, slug, campos, estado: "_Estado", arquivo: str) -> Obra:
        def um(nome: str, padrao: str = "") -> str:
            valores = campos.get(nome)
            return valores[0] if valores else padrao

        try:
            tipo = Tipo.de_texto(um("tipo", "episodico"))
        except ValueError:
            raise ErroDeConteudo(
                arquivo, "tipo deve ser `episodico` ou `concluido`"
            ) from None

        avisos: list[Aviso] = []
        for codigo in re.split(r"[,;]", um("aviso")):
            if not codigo.strip():
                continue
            try:
                avisos.append(Aviso.de_codigo(codigo))
            except KeyError:
                raise ErroDeConteudo(
                    arquivo, f"aviso desconhecido: {codigo.strip()!r}"
                ) from None

        try:
            ordem = float(um("ordem", "0") or 0)
        except ValueError:
            raise ErroDeConteudo(arquivo, "`ordem` deve ser um número") from None

        capitulos = tuple(
            Capitulo(numero=i, titulo=r.titulo, nos=tuple(r.nos))
            for i, r in enumerate(estado.rascunhos, start=1)
        )
        return Obra(
            slug=slug,
            titulo=um("titulo", slug),
            tipo=tipo,
            genero=um("genero"),
            ano=um("ano"),
            avisos=tuple(avisos),
            sinopse=tuple(s for s in campos.get("sinopse", []) if s),
            ordem=ordem,
            capitulos=capitulos,
        )


class _Estado:
    def __init__(self, arquivo: str):
        self.arquivo = arquivo
        self.linha = 0
        self.rascunhos: list[_Rascunho] = []
        self._ultimo: No | None = None

    @property
    def depois_de_nome(self) -> bool:
        return isinstance(self._ultimo, Nome)

    def novo_capitulo(self, titulo: str) -> None:
        self.rascunhos.append(_Rascunho(titulo))
        self._ultimo = None

    def adicionar(self, no: No) -> None:
        if not self.rascunhos:
            self.rascunhos.append(_Rascunho(""))
        self.rascunhos[-1].nos.append(no)
        self._ultimo = no
