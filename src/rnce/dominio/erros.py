class ErroDeConteudo(Exception):
    def __init__(self, arquivo: str, mensagem: str, linha: int | None = None):
        onde = f"{arquivo}:{linha}" if linha else arquivo
        super().__init__(f"{onde}: {mensagem}")
        self.arquivo = arquivo
        self.linha = linha
