import shutil
import tempfile
import unittest
from pathlib import Path

from rnce.construcao import ConstrutorDoSite
from rnce.visual.escape import Html, escapar, so_se_http

RAIZ = Path(__file__).resolve().parents[1]

MALICIOSA = """---
titulo: <script>alert(1)</script>
tipo: concluido
genero: "><img src=x onerror=alert(2)>
sinopse: </title><script>alert(3)</script>
---

*tit* <b onmouseover=alert(4)>Cap</b>

*nome* <svg onload=alert(5)>

Fala com <script>alert(6)</script> e "aspas" & e-comercial.

*acao* <iframe src="javascript:alert(7)"></iframe>
"""


class EscapeTest(unittest.TestCase):
    def test_texto_comum_e_escapado(self):
        self.assertEqual(escapar('<a href="x">&'), "&lt;a href=&quot;x&quot;&gt;&amp;")

    def test_html_nao_e_escapado_duas_vezes(self):
        self.assertEqual(escapar(Html("<p>ok</p>")), "<p>ok</p>")

    def test_links_so_http(self):
        self.assertEqual(so_se_http("https://exemplo.org"), "https://exemplo.org")
        for ruim in ("javascript:alert(1)", "data:text/html,x", "//exemplo.org", "ftp://x"):
            with self.assertRaises(ValueError):
                so_se_http(ruim)


class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(RAIZ / "tema", cls.tmp / "tema")
        (cls.tmp / "conteudo" / "obras").mkdir(parents=True)
        shutil.copy(RAIZ / "conteudo" / "site.toml", cls.tmp / "conteudo")
        (cls.tmp / "conteudo" / "obras" / "teste.rnce").write_text(MALICIOSA, encoding="utf-8")
        cls.resultado = ConstrutorDoSite(cls.tmp).construir()
        cls.paginas = {
            p.relative_to(cls.tmp / "dist").as_posix(): p.read_text(encoding="utf-8")
            for p in (cls.tmp / "dist").rglob("*.html")
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def test_gera_uma_pagina_por_capitulo(self):
        self.assertIn("teste/index.html", self.paginas)
        self.assertIn("teste/1/index.html", self.paginas)
        self.assertIn("404.html", self.paginas)

    def test_nenhuma_marca_do_texto_vira_html(self):
        for nome, html in self.paginas.items():
            with self.subTest(pagina=nome):
                for perigo in ("<script>alert", "<img src=x", "<svg onload", "<iframe", "<b onmouseover"):
                    self.assertNotIn(perigo, html)

    def test_o_texto_aparece_escapado(self):
        self.assertIn("&lt;script&gt;alert(6)&lt;/script&gt;", self.paginas["teste/1/index.html"])

    def test_sem_script_ou_estilo_embutido(self):
        for nome, html in self.paginas.items():
            with self.subTest(pagina=nome):
                self.assertNotIn("<style", html)
                self.assertNotIn(" style=", html)
                self.assertNotIn(" onclick=", html)
                self.assertEqual(html.count("<script"), html.count("<script src="))
                self.assertIn("Content-Security-Policy", html)

    def test_capa_nao_carrega_o_texto_da_obra(self):
        self.assertNotIn("e-comercial", self.paginas["teste/index.html"])


if __name__ == "__main__":
    unittest.main()
