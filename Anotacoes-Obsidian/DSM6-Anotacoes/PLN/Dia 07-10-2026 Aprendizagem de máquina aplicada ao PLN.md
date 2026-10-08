\- Redes Neurais Artificiais (RNA)
	\- O modelo matemático simplificado foi proposto por Mc Cullock e Pitts conforme definido abaixo:

A operação de uma rede neural artificial pode ser resumida por:
1) Sinais são apresentados a entrada.
2) Cada sinal está associado a um peso(grau de relevância para com a saída)
3) É feita a soma ponderada dos sinais com seus respectivos pesos.
4) O resultado da soma ponderada será apresentado a função de ativação e de acordo com a comparação produz-se o resultado da saída.

Para as RNAs com feedback, o fluxo de informação passa da "entrada" para a "saída" e fornece para a rede como "ajuste" o resultado entre saída correta e saída obtida . nesse caso o obrigando o fluxo de informação a retornar da saída para entrada.

Exercício para fixação 

-Tarefa : Brincar no parque
\- Atributos: {- Está sol? (x1)
		   - Está quente? (x2)}
\- Modelo simplificado da rede:

\- Classes { - 0: Não irá brincar
		- 1: Irá brincar}
\- Base de dados:

| x1  | x2  | classe (y) -> Classe real Yr = 0 |
| --- | --- | -------------------------------- |
| 0   | 0   | 0                                |
| 0   | 1   | 0                                |
| 1   | 0   | 0                                |
| 1   | 1   | 1                                |

\- Taxa de aprendizagem (n) = 0,5

### \* Atualização dos pesos
\- Se Yp (classe predita) for igual a Yr(classe real) então não há necessidade de atualizar o peso da rede.
\- Se Yp ≠ Yr então realize a atualização dos pesos:
Wnovo = Wi + n \* (Yr - Yp) \* Xi
em que:
Wi: peso atual do atributo
n: taxa de aprendizagem da rede
Yr: classe real
Yp: classe predita
Xi: valor do atributo

\-> A taxa de aprendizagem indica a velocidade em que a rede irá convergir. Normalmente é um valor entre 0 e 1.

### \#Etapa de treinamento 
\- Selecionar uma amostra:

| X1  | X2  | Classe0 |
| --- | --- | ------- |
| 0   | 0   | 0       |
\- Aplicar X1 = 0 e X2 = 0 no modelo da rede:

0 X1 W1 = 1   Soma - F(x) -> 
0 X2 W2 = 2
\- Calcular a soma ponderada:

E(Soma) = (X1 * W1) + (X2 * W2)
\= (0 * 1) + (0 * 2)
\= 0 + 0 = 0

F(x) = {1, soma >= 3
	   0, soma < 3}

\-> Aplicar o resultado da soma na F(x):
	soma = 0 -> Yp = 0
\-> Compar Yp com Yr:
Yp = 0 } são iguais
 Yr = 0}


| X1  | X2  | Classe |
| --- | --- | ------ |
| 0   | 1   | 0      |


E = (x1 * w1) + (x2 * w2)
\= (0 * 1) + (1 * 2) = 
\= 0 + 2 = 2

F(x)= se resultado(2) < 3 == 0
Soma = 2 -> Yp = 0
-> Comparar Yp com Yr:
Yp = 0 
são iguais
Yr = 0 

| X1  | X2  | Classe |
| --- | --- | ------ |
| 1   | 0   | 0      |


E = (x1 * w1) + (x2 * w2)
\= (1 * 1) + (1 *0) = 
\= 1 + 0 = 1

F(x)= Se resultado(1) < 3 == 0
Soma = 1 -> Yp = 0
-> Comparar Yp com Yr:
Yp = 0 
são iguais
Yr = 0 

| X1  | X2  | Classe |
| --- | --- | ------ |
| 1   | 1   | 1      |


E = (x1 * w1) + (x2 * w2)
\= (1 * 1) + (1 * 2) = 
\= 1 + 2 = 3

F(x)= se resultado(3) < 3 == 0, se resultado(3) maior ou igual a 3 == 1
Soma = 3 -> Yp = 1
-> Comparar Yp com Yr:
Yp = 1
são iguais
Yr = 1

