from dataclasses import dataclass, field
from enum import Enum


class Tipo(Enum):
    FOLHETIM = "folhetim"
    VOLUME = "volume"

    @classmethod
    def de_texto(cls, texto: str) -> "Tipo":
        t = texto.strip().lower()
        if t in ("episodico", "episódico", "folhetim"):
            return cls.FOLHETIM
        if t in ("concluido", "concluído", "volume", "fechado"):
            return cls.VOLUME
        raise ValueError(texto)


class Aviso(Enum):
    SEXO = "Nudez e Conteúdo Sexual"
    VIOLENCIA = "Violência e Conteúdo Gráfico"
    DROGAS = "Drogas, Armas e Atividades Ilegais"
    TRAUMA = "Temas Sensíveis / Traumas"
    SUICIDIO = "Suicídio e Autolesão"
    LINGUAGEM = "Linguagem Ofensiva"
    TERROR = "Terror e Tensão Psicológica"

    @classmethod
    def de_codigo(cls, codigo: str) -> "Aviso":
        return _CODIGOS_DE_AVISO[codigo.strip().lower()]


_CODIGOS_DE_AVISO = {
    "sexo": Aviso.SEXO,
    "viol": Aviso.VIOLENCIA,
    "drog": Aviso.DROGAS,
    "trau": Aviso.TRAUMA,
    "suic": Aviso.SUICIDIO,
    "ling": Aviso.LINGUAGEM,
    "terr": Aviso.TERROR,
}


class No:
    """Bloco do texto de um capítulo."""


@dataclass(frozen=True)
class Paragrafo(No):
    texto: str


@dataclass(frozen=True)
class Fala(No):
    texto: str


@dataclass(frozen=True)
class Nome(No):
    texto: str


@dataclass(frozen=True)
class Acao(No):
    texto: str


@dataclass(frozen=True)
class Subtitulo(No):
    texto: str


@dataclass(frozen=True)
class Quebra(No):
    pass


@dataclass(frozen=True)
class Capitulo:
    numero: int
    titulo: str
    nos: tuple[No, ...] = ()

    @property
    def subtitulo(self) -> str:
        """Só conta como subtítulo do capítulo se vier antes de qualquer texto."""
        if self.nos and isinstance(self.nos[0], Subtitulo):
            return self.nos[0].texto
        return ""


@dataclass(frozen=True)
class Obra:
    slug: str
    titulo: str
    tipo: Tipo
    genero: str = ""
    ano: str = ""
    avisos: tuple[Aviso, ...] = ()
    sinopse: tuple[str, ...] = ()
    ordem: float = 0
    capitulos: tuple[Capitulo, ...] = field(default_factory=tuple)

    def capitulo(self, numero: int) -> Capitulo:
        return self.capitulos[numero - 1]

    @property
    def rotulo_de_capitulos(self) -> str:
        n = len(self.capitulos)
        return f"{n} capítulo" if n == 1 else f"{n} capítulos"
