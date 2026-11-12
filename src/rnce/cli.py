import argparse
import functools
import http.server
import sys
from pathlib import Path

from .construcao import ConstrutorDoSite, RepositorioDeObras
from .dominio import ErroDeConteudo

RAIZ = Path(__file__).resolve().parents[2]


def _construir(args) -> int:
    r = ConstrutorDoSite(RAIZ).construir()
    print(f"ok: {r.obras} obra(s), {r.paginas} página(s) em {r.pasta.relative_to(RAIZ)}/")
    return 0


def _conferir(args) -> int:
    for o in RepositorioDeObras(RAIZ / "conteudo" / "obras").todas():
        print(f"ok: {o.slug}: {o.titulo} ({o.rotulo_de_capitulos}, {o.tipo.value})")
    return 0


def _servir(args) -> int:
    r = ConstrutorDoSite(RAIZ).construir()
    tratador = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(r.pasta))
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.porta), tratador) as servidor:
        print(f"http://localhost:{args.porta}  (Ctrl+C para parar)")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print()
    return 0


def principal(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rnce", description="Gerador do site RNCE.")
    comandos = parser.add_subparsers(dest="comando", required=True)
    comandos.add_parser("construir", help="gera o site em dist/").set_defaults(acao=_construir)
    comandos.add_parser("conferir", help="valida os arquivos .rnce").set_defaults(acao=_conferir)
    servir = comandos.add_parser("servir", help="gera e serve em localhost")
    servir.add_argument("--porta", type=int, default=8000)
    servir.set_defaults(acao=_servir)

    args = parser.parse_args(argv)
    try:
        return args.acao(args)
    except ErroDeConteudo as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
