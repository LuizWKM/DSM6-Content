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
    print(pd.DataFrame(matrix[1:,1:], index=list(seq1),columns=list(seq2)))

    return (matrix[size_x-1,size_y-1])

print(levenshtein("medicina","medico"))
print(levenshtein("computador","computado"))