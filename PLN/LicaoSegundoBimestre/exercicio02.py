import nltk
import string
import pandas as pd
import numpy as np

def levenshtein(seq1, seq2):
    #criar uma matriz
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x,size_y))

    #atribuir valor aos números das colunas (0,n-1)
    for x in range(size_x):
        matrix[x,0] = x
    
     #atribuir valor aos números das linhas (0,n-1)
    for y in range(size_y):
        matrix[0,y] = y

    #calcular a distância
    for x in range(1, size_x):
        for y in range(1, size_y):
            #se os caracteres sao iguais, nao aumenta a distancia
            if(seq1[x-1] == seq2[y-1]):
                matrix[x,y] = matrix[x-1,y-1]
            
            #se sao diferentes, aumenta a distancia em 1
            else:
                matrix[x,y] = min(matrix[x-1,y]+1,matrix[x-1,y-1]+1,matrix[x,y-1]+1)

    #imprime a matriz de calculo de distancia
    #list(seq1) convert string em uma lista de caracteres

    return (matrix[size_x-1,size_y-1])

textos = pd.read_excel("avaliacoes.xlsx")
resultados = []
cont = 0

texto1="O produto possui excelente qualidade, chegou rapidamente e atendeu completamente às minhas expectativas. Gostei muito da compra e recomendo este produto para outras pessoas."
texto2 = "O produto possui péssima qualidade, apresentou problemas logo após a compra e não atendeu às minhas expectativas. Fiquei muito decepcionado e não recomendo este produto."

texto1_limpo = "".join([c for c in texto1.lower() if c not in string.punctuation])
texto2_limpo = "".join([c for c in texto2.lower() if c not in string.punctuation])

palavras1 = nltk.word_tokenize(texto1.lower())
palavras2 = nltk.word_tokenize(texto2.lower())

palavras1 = [palavra for palavra in palavras1 if palavra not in string.punctuation]
palavras2 = [palavra for palavra in palavras2 if palavra not in string.punctuation]


p1 = set(palavras1)
p2 = set(palavras2)
interseccao_positiva = 0
interseccao_negativa = 0
lev_pos = 0
lev_neg = 0
classe_jaccard = ""
classe_lev = ""

for texto in textos["avaliacao"]:
    cont += 1    

    texto_str = str(texto)

    texto_avaliacao_limpo = "".join([c for c in texto_str.lower() if c not in string.punctuation])

    palavras = set(nltk.word_tokenize(texto.lower()))
    palavras = [palavra for palavra in palavras if palavra not in string.punctuation]
    lev_pos = levenshtein(texto_avaliacao_limpo, texto1_limpo)
    lev_neg = levenshtein(texto_avaliacao_limpo, texto2_limpo)


    for palavra1 in palavras:
        for palavra2 in p1:
            if (palavra1 == palavra2):
                interseccao_positiva += 1

        for palavra3 in p2:
            if (palavra1 == palavra3):
                interseccao_negativa += 1

    uniao = (len(p1) + len(palavras)) - interseccao_positiva
    jaccard_positivo = interseccao_positiva / uniao
    interseccao_positiva = 0

    uniao = (len(p2) + len(palavras)) - interseccao_negativa
    jaccard_negativo = interseccao_negativa / uniao
    interseccao_negativa = 0

    if jaccard_positivo > jaccard_negativo:
        classe_jaccard = "Positiva"
    else:
        classe_jaccard = "Negativa"

    if lev_pos < lev_neg:
        classe_lev = "Positiva"
    else:
        classe_lev = "Negativa"

    resultados.append(
        {
            "ID": cont,
            "Avaliação": texto,
            "Jaccard Pos.": round(jaccard_positivo, 2),
            "Jaccard Neg.": round(jaccard_negativo, 2),
            "Class. Jaccard": classe_jaccard,
            "Lev. Pos.": lev_pos,
            "Lev. Neg.": lev_neg,
            "Class. Lev.": classe_lev,
        }
    )
    
    lev_pos = 0
    lev_neg = 0


df_final = pd.DataFrame(resultados)
print(df_final)
df_final.to_excel("resultado_classificacao.xlsx", index=False)