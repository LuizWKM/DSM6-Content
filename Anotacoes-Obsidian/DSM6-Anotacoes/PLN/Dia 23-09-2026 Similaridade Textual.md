-> Permite identificar o quão próximos dois fragmentos de textos são baseados em sua estrutura (sintaxe) e/ou significado (semântica).

Exemplo: Os gatos comem os ratos; Os gatos comem os insetos.

-> Análise de acordo com as palavras em comuns indicaria um alto nível de semelhança entre as duas frases

-> A análise de acordo com o significado das palavras indicaria que as palavras "INSETOS" e "RATOS" não possuem alto índice de similaridade.

-> Tipos de métricas

### - Métrica baseada em termos
1 - Medida de Jaccard
-> Ela trabalha comparando o conjunto de termos obtidos após a tokenização. A ordem em que os termos aparecem não importa.
Ex: { Os gatos comem os ratos
    {Os gatos comem insetos
Passos a serem realizados:
1 - Definir os 2 fragmentos de texto
2 - Aplicar a tokenização sobre os 2 fragmentos de texto e armazenar o resultado em 2 arrays.
Tokens 1 = \[ 'Os', 'gatos', 'comem', 'os', 'ratos' ];
Tokens 2 = \[ 'Os', 'gatos', 'comem', 'os', 'insetos' ];

3 - Aplicar o operador de intersecção ( ∩ ) entre os termos dos 2 arrays.
tokens 1 ∩ tokens 2 = 4

4 - Aplicar o operador de união ( U ) entre os termos dos 2 arrays.

tokens 1 U tokens 2 = 6

5 - Realizar a divisão entre intersecção por união.

Jaccard = tokens 1 ∩ tokens 2 / tokens 1 U tokens 2

Jaccard = 4 / 6

Jaccard ~= 0,67 ou 67%

\* Exercício de fixação: A empresa Platz verificou que em seu banco de dados muitos nomes da cidade eram escritores de diferentes maneiras para a mesma cidade. Por exemplo: 
-> cidade: São Paulo
variações: SP; Sp; S. Paulo; São Paulo; São P.

Pensando nisso, responda os itens abaixo:
a) Compare as variações de 2 em 2 e de acordo com a métrica de Jaccard, calcule a intersecção, a união e o índice de Jaccard.
R: 

SP ∩ Sp = 0, SP U Sp = 2, Jaccard = 0 / 2 = 0
SP ∩ S. Paulo = 0; SP U S. Paulo = 3; Jaccard = 0 / 3 = 0
SP ∩ São Paulo = 0; SP U São Paulo = 3; Jaccard = 0 / 3 = 0
SP ∩ São P. = 0; SP U São P. = 3; Jaccard = 0 / 3 = 0

Sp ∩ S. Paulo = 0; Sp U S. Paulo = 3; Jaccard = 0 / 3 = 0
Sp ∩ São Paulo = 0; SP U São Paulo = 3; Jaccard = 0 / 3 = 0
Sp ∩ São P. = 0; SP U São P. = 3; Jaccard = 0 / 3 = 0

S. Paulo ∩ São Paulo = 1; S. Paulo U São Paulo = 3; Jaccard = 1 / 3 = 0,33 33%
S. Paulo ∩ São P. = 0; S. Paulo U São P. = 4; Jaccard = 0  / 4 = 0

São Paulo ∩ São P. = 1; São Paulo U São P. = 3; Jaccard = 1 / 3 = 0,33 33%

São Paulo ∩ São Paulo = 2; São Paulo U São Paulo = 2; Jaccard = 2 / 2 = 1 100%


b) Considerando o funcionamento dessa métrica, essa seria uma técnica eficiente para a tarefa proposta?
R: Não, mesmo tendo uma palavra que tem 100% de semelhança, não vai conseguir assimilar o restante das palavras corretamente, sendo que a maior pontuação é 33% e o restante 0%. Não consegue verificar abreviações corretamente.

2 - Medida de Levenshtein
-> Compara sequência de caracteres verificando a menor quantidade de operações válidas para transformar a primeira string na segunda string. Essa comparação é realizada por meio de uma matriz, na qual a primeira string será posicionada nas linhas e a segunda nas colunas. 
-> São operações válidas nas colunas: \[ Inserção (+1)
								Remoção (+1)
								Substituição (+1)]
-> Exemplo :
Comparar as palavras "dedo" e "dengo".

|     |     | d   | e   | n   | g   | o   |
| --- | --- | --- | --- | --- | --- | --- |
|     | 0   | 1   | 2   | 3   | 4   | 5   |
| d   | 1   | 0   | 1   | 2   | 3   | 4   |
| e   | 2   | 1   | 0   | 1   | 2   | 3   |
| d   | 3   |     |     |     |     |     |
| o   | 4   |     |     |     |     |     |
-> Para transformar:

| d   | e   | d   | o   |
| --- | --- | --- | --- |

| d   | e   | n   | g   | o   |
| --- | --- | --- | --- | --- |
0              0          1          1           1
			troca      troca     adiciona

\- Para montar  a matriz, siga as etapas:
1 - Posicione as palavras ( palavra 1 nas linhas e palavra 2 nas colunas)
2 - Numere as linhas e colunas iniciando com 'O' antes da primeira letra e criando a sequência de 1 até o tamanho das palavras.
3 - Para cada espaço em branco, analise o menor valor entre esquerda, diagonal e em cima. Esse valor será utilizado como base para saber quantas operações foram realizadas até ali. Em seguida, compare os caracteres se forem iguais some + 0 na quantidade mínima de operações. Caso sejam diferentes some + 1.
4 - Ao final do preenchimento da matriz você encontrara na última posição, o valor da quantidade de operações necessárias para transformar a palavra 1 em palavra 2.