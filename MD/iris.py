# Dataset Iris
# Utilizado para demonstrar, passo a passo como um algoritmo de Machine Learning pode aprender padrões e classificar flores de 3 especies

# Importando biblioteca
import pandas as pd # Dataframe
import matplotlib.pyplot as plt # Criar gráficos
from sklearn.datasets import load_iris # Dataset nativo
from sklearn.tree import DecisionTreeClassifier # Arvore de Decisão
from sklearn.tree import plot_tree # Desenha a arvore de decisão

# Métricas utilizadas para avaliar o modelo
from sklearn.metrics import accuracy_score
from sklearn.metrics import  confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

#2 Carregamento do dataset iris
iris = load_iris()
print('\n')
print('='*70)

#3 Conhencendo o dataset
#Quantidade de registros
print("\n Quantidade de registros existentes: ")
print(len(iris.data))

#Nome das caracteristicas
print('\nCaracteristicas utilizadas para analisar cada flor: ')
for caracteristicas in iris.feature_names:
    print("-", caracteristicas)

#Nomes das Especies
print("\nEspecies Existentes:")
for especie in iris.target_names:
    print("-", especie)

print("\nMedidas da primeira flor: ")
print("Comprimento da sépala: ", iris.data[0][0], "cm")
print("Largura da sépala: ", iris.data[0][1], "cm")
print("Comprimento da pétala: ", iris.data[0][2], "cm")
print("Largura da pétala: ", iris.data[0][3], "cm")

#Código da especie
codigo_especie = iris.target[0]
print("\nCodigo da Espécie: ", codigo_especie)

#Traduzindo o código para o nome da especie
print("\nNome da Especie: ", iris.target_names[codigo_especie])

#Transformando dados em tabela
print("\n")
print("="*70)
print("Transformando os dados em tabela")

#Criar um Dataframe usando os dados do dataset
dados = pd.DataFrame(
    iris.data, 
    columns=[
        "Comprimento_sepala",
        "Largura_sepala",
        "Comprimento_petala",
        "Largura_petala"
        ]
)

#Adicionar a coluna com o código da espécie
dados["Codigo_Especie"] = iris.target
#Criar uma nova coluna traduzindo o código para o nome da especie
dados["Nome_Especie"]=dados["Codigo_Especie"].map({
    0:"Setosa",
    1:"Versicolor",
    2:"Virginica"
})

#Mostrar os primeiros registros
print("\nPrimeiras 10 flores do dataset:\n")
print(dados.head(10))

#Tamanho do dataset
print("\n")
print("="*70)
print("Tamanho do Dataset")
print("="*70)

print("\nQuantidade de linhas:", dados.shape[0])
print("\nQuantidade de colunas:", dados.shape[1])

#Quantidade de flores
print("\n")
print("="*70)
print("Quantidade de flores por especie")
print("="*70)

quantidade_especie = dados["Nome_Especie"].value_counts()
print("\nQuantidade de flores por especie são: \n", quantidade_especie)

#Gráfico - Quantidade de flores
quantidade_especie.plot(kind="bar")
plt.title("Quantidade de flores por espécie")
plt.xlabel("Espécie")
plt.ylabel("Quantidade")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Média das medidas por especie
print("\n")
print("="*70)
print("Medida das médias por especie")
print("="*70)

medias = dados.groupby("Nome_Especie")[
    [
        "Comprimento_sepala",
        "Largura_sepala",
        "Comprimento_petala",
        "Largura_petala"
    ]
].mean()

print("\n")
print(medias)

#Visualização dos Dados

print("\n")
print("="*70)
print("Visualização dos Dados")
print("="*70)

print("\nMostrar gráfico se existem grupos diferentes por especie")

#Percorrer cada especie
for especie in dados["Nome_Especie"].unique():

    #Filtrar apenas registros da especie
    dados_especie = dados[
        dados["Nome_Especie"] == especie
    ]

    #Adicionar os pontos do gráfico
    plt.scatter(
        dados_especie["Comprimento_petala"],
        dados_especie["Largura_petala"],
        label=especie
    )

    #Configuração dos gráfico
    plt.title("Relação entre comprimento e largura da petala")
    plt.xlabel("Comprimento da petala (cm)")
    plt.ylabel("Largura da petala (cm)")
    plt.legend()
    plt.grid()
    plt.show()

    print("\n")
    print("="*70)
    print("Quantidade de flores por especie")
    print("="*70)

    #X contem as caracteristicas utilizadas pelo algoritmo para realizar o aprendizado.

    x = dados[
        [
            "Comprimento_sepala",
            "Largura_sepala",
            "Comprimento_petala",
            "Largura_petala"    
        ]
    ]

#Y contem a resposta correta retornando a especie da flor
y = dados["Codigo_Especie"]
print("\nX representa os dados utilizado como ENTRADA")

print(
    "Comprimento_sepala",
    "Largura_sepala",
    "Comprimento_petala",
    "Largura_petala"  
)

print("\nY representa a resposta que queremos prever")
print("\n Y=especie da flor")

# Separando treinamento e teste

print("\n")
print("="*70)
print("Separação para treinamento e teste")
print("="*70)

# Iremos utilizar 70% dos dados para treinamento e 30% para testes
from sklearn.model_selection import train_test_split
x_treino, x_teste, y_treino, y_teste = train_test_split(
    x,
    y,
    test_size = 0.30,
    random_state=42,
    stratify=y
)
print("\nTotal de flores:", len(dados))

print("\nFlores utilizadas no treinamento:", len(x_treino))

print("\nFlores utilizadas no teste", len(x_teste))

#Criar a arvore de decisão
print("\n")
print("="*70)
print("Separação para treinamento e teste")
print("="*70)

#Criar o modelo de árvore de decisão. max_depth=3 limita a árvore em 3 níveis. Isso irá facilitar a visualização e interpretação.

modelo = DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)

print("\nModelo criado:")