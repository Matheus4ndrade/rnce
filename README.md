# RNCE

Onde eu publico o que escrevo. Cada obra é um arquivo `.rnce`; o gerador lê
esses arquivos e monta o site estático.

Python 3.11+, sem dependência nenhuma.

```
python fazer.py              gera em dist/
python fazer.py servir       sobe em http://localhost:8000
python fazer.py conferir     só valida os .rnce
PYTHONPATH=src python -m unittest discover -s tests
```

Os endereços são de pasta (`/entre-portas/1/`), então abrir o `index.html` do
disco não funciona direito. Use o `servir`.

## Publicar

Arquivo novo em `conteudo/obras/` — o nome vira o endereço
(`entre-portas.rnce` → `/entre-portas/`). Roda o `servir`, confere, push.
O workflow gera e publica.

Capítulo novo no folhetim é mais um `*tit*` no mesmo arquivo. Quando a obra
acaba, troca `tipo: episodico` por `tipo: concluido` e ela muda de seção.

## Formato

```
---
titulo: Nome da obra
tipo: episodico        (ou concluido)
genero: Comédia · Mistério
ano: 2026
aviso: trau, ling      (sexo, viol, drog, trau, suic, ling, terr)
ordem: 1               (opcional)
sinopse: primeiro parágrafo
sinopse: segundo parágrafo
---

*tit* Capítulo Um *tit*        cada um vira uma página
*sub* 1999 *sub*
texto normal                   parágrafo, separado por linha em branco
***                            quebra de cena
*nome* DANILO (rindo)          a fala é o parágrafo seguinte
*acao* Sacada de uma casa.
```

Fechar a marca no fim da linha é opcional. Marca que não existe para o build
dizendo arquivo e linha.

Texto do site e `url`: `conteudo/site.toml`.

## Pastas

```
conteudo/     site.toml e as obras
src/rnce/     dominio, analise, visual, paginas, construcao
tema/         templates, css, js, fontes
tests/
docs/         notas
```

## Deploy

Settings → Pages → Source: GitHub Actions, e preencher `url` no `site.toml`
com `https://USUARIO.github.io/REPOSITORIO`. O resto está em
`.github/workflows/publicar.yml`.

## Falta fazer

- [ ] Editor local com os botões da marcação, pra não escrever `*tit*` na mão
- [ ] Rever os textos da home e das seções
- [ ] Dois Navegantes, episódio 2
