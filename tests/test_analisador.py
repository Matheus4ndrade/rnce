import unittest

from rnce.analise import AnalisadorRnce
from rnce.dominio import Acao, Aviso, ErroDeConteudo, Fala, Nome, Paragrafo, Quebra, Subtitulo, Tipo

TEXTO = """---
titulo: Uma Peça
tipo: concluido
genero: Drama
ano: 2025
aviso: trau, ling
sinopse: primeiro
sinopse: segundo
---

*tit* Parte I *tit*

*sub* 1999

*acao* Uma sala.

*nome* Danilo (rindo)

Oi.
Tudo bem?

Narração comum.

***

*tit* Parte II
"""


class AnalisadorTest(unittest.TestCase):
    def setUp(self):
        self.obra = AnalisadorRnce().analisar(TEXTO, "uma-peca")

    def test_cabecalho(self):
        o = self.obra
        self.assertEqual(o.titulo, "Uma Peça")
        self.assertIs(o.tipo, Tipo.VOLUME)
        self.assertEqual(o.avisos, (Aviso.TRAUMA, Aviso.LINGUAGEM))
        self.assertEqual(o.sinopse, ("primeiro", "segundo"))

    def test_capitulos_e_nos(self):
        self.assertEqual([c.titulo for c in self.obra.capitulos], ["Parte I", "Parte II"])
        tipos = [type(n) for n in self.obra.capitulo(1).nos]
        self.assertEqual(tipos, [Subtitulo, Acao, Nome, Fala, Paragrafo, Quebra])
        self.assertEqual(self.obra.capitulo(1).subtitulo, "1999")

    def test_fala_e_so_o_paragrafo_depois_do_nome(self):
        nos = self.obra.capitulo(1).nos
        self.assertEqual(nos[3], Fala("Oi.\nTudo bem?"))
        self.assertEqual(nos[4], Paragrafo("Narração comum."))

    def test_marca_desconhecida_avisa_a_linha(self):
        with self.assertRaises(ErroDeConteudo) as erro:
            AnalisadorRnce().analisar("*tit* A\n\n*acoa* errei a marca\n", "x")
        self.assertIn("x.rnce:3", str(erro.exception))

    def test_recusa_slug_torto_tipo_invalido_e_obra_vazia(self):
        a = AnalisadorRnce()
        for texto, slug in (
            ("*tit* A\n\ntexto", "Com Espaço"),
            ("*tit* A\n\ntexto", "../fora"),
            ("*tit* A\n\ntexto", "folhetim"),
            ("---\ntipo: outro\n---\n*tit* A\n\ntexto", "ok"),
            ("---\naviso: xyz\n---\n*tit* A\n\ntexto", "ok"),
            ("", "ok"),
            ("texto com \x00 nulo", "ok"),
        ):
            with self.subTest(slug=slug, texto=texto[:20]):
                with self.assertRaises(ErroDeConteudo):
                    a.analisar(texto, slug)


if __name__ == "__main__":
    unittest.main()
