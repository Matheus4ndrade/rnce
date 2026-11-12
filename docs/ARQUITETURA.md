# Notas

Anotações pra quando eu voltar nisso daqui a seis meses.

## Fluxo

`conteudo/obras/*.rnce` → `RepositorioDeObras` lê os arquivos → `AnalisadorRnce`
transforma em `Obra` (ou estoura `ErroDeConteudo` com arquivo e linha) → as
classes de `paginas/` montam o HTML → `SaidaEmDisco` escreve `dist/`.
`ConstrutorDoSite` chama tudo na ordem.

`dominio/` não importa nada do projeto. `analise/` e `visual/` importam
`dominio`. `paginas/` importa `visual`. `construcao/` importa todo mundo.
Se eu inverter isso em algum momento, é sinal de que coloquei coisa no lugar
errado.

## Por que assim

**Uma página por capítulo.** A primeira versão era um HTML só, com as obras
embutidas e rota por hash. Funcionava, mas cada obra nova engordava o arquivo
inteiro e o texto completo aparecia no fonte da página. Agora cada capítulo é
um `index.html` e a capa da obra não carrega texto nenhum.

**Nó em vez de string.** O analisador devolve `Fala`, `Acao`, `Nome`... e o
renderizador tem um método por tipo. Pra criar marca nova: classe em
`dominio/modelos.py`, tratador no analisador, `_visitar_*` no renderizador.

**`Html` é um tipo.** `str` sempre escapa, só `Html` passa direto, e só o
renderizador cria `Html`. Assim eu não esqueço escape — o caminho preguiçoso
já é o certo.

## Segurança

Site estático, então não tem servidor, banco, login nem formulário. O que
sobra é texto virar HTML:

- escape por tipo (acima);
- validação antes de publicar (nome de arquivo, tamanho, caractere de
  controle, marca que não existe) — o build para em vez de publicar torto;
- link do `site.toml` só passa se for http(s), externo leva
  `rel="noopener noreferrer"`;
- CSP em toda página; script, estilo e fonte só do próprio site;
- nada de CDN, biblioteca de terceiro ou rastreador;
- no navegador os avisos são montados com `textContent`, e o que vem do
  `localStorage` eu valido contra lista antes de usar;
- `test_seguranca.py` constrói o site a partir de uma obra cheia de `<script>`
  e confere que nada virou HTML.

O Pages não deixa mandar cabeçalho HTTP, então a CSP vai em `<meta>`. Pega
script e estilo injetado, mas `frame-ancestors` só funciona como cabeçalho —
ia precisar de domínio próprio atrás de proxy.
