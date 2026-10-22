import numpy as np

# Array com os valores de entrada (neurônios)
# Para cada posição é um neuronio, [0,0] = 2 neuronios, [0,0,1] = 3 neuronios a quantidade de pesos é igual a quantidade de neuronios.
X = np.array([[0,0], [0,1], [1,0], [1,1]])
# Array dos pesos (importância dos neurônios)
pesos = [0.5, 0.5]
# Array com as classes respectivas a entrada
Y = np.array([0,0,0,1])
soma = 0
qtdEntradas = 0
tx_aprendizagem = 0.3
epocas = 10
# for i in range(epocas):
for entrada in X:
    i = 0
    for xi in entrada:
        soma += xi * pesos[i]
        i = i+1
    # Função de ativação
    if(soma >= 3): 
        yp = 1
    else:
        yp = 0

    if yp == Y[qtdEntradas]:
        print("Acertou!")    
    else:
        print("Errou!")
        for i in range(2):
            pesos[i] = pesos[i] + (yp-Y[qtdEntradas]) * tx_aprendizagem * xi

    soma = 0