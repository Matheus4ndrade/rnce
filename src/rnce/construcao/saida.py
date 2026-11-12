import shutil
from pathlib import Path


class SaidaEmDisco:
    def __init__(self, pasta: Path):
        self.pasta = pasta
        self.arquivos = 0

    def limpar(self) -> None:
        if self.pasta.exists():
            shutil.rmtree(self.pasta)
        self.pasta.mkdir(parents=True)

    def escrever(self, caminho: str, conteudo: str) -> None:
        destino = (self.pasta / caminho).resolve()
        if not destino.is_relative_to(self.pasta.resolve()):
            raise ValueError(f"caminho fora da saída: {caminho}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(conteudo, encoding="utf-8", newline="\n")
        self.arquivos += 1

    def copiar_pasta(self, origem: Path, caminho: str) -> None:
        shutil.copytree(origem, self.pasta / caminho, dirs_exist_ok=True)
