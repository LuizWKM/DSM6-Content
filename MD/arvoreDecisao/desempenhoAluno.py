import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix

#1. Carregar e conhecer a base
df = pd.read_csv("arvoreDecisao\desempenho_estudantes.csv")

print('\nPrimeiros registro: ')
print(df.head(5))
print('\nTamanho da base: ', df.shape)
print('Valores ausentes:')
print(df.isnull().sum())

#2. Selecionar as variaveis uteis para a mineracao
variaveis = ["horas_estudo_semana", "frequencia_percentual", "atividades_entregues", "media_exercicios", "participacao_aulas", "acessos_plataforma_semana", "faltas_mes"]
x = df[variaveis].copy()
y = df["situacao_final"]

# Entradas(X) => Hora, Frequencia, Atividades, Media, Participacao, Acesso e Faltas
# Algoritmo => Arvore de decisao
# Respostas(Y) => Desempenho_satisfatorio ou Precisa_atencao

#3. Separar os dados para treinamento e o teste
X_treino, X_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.25, random_state=42, stratify=y)

#180 Registros
# 25% para teste = 45 registros
# 75% para aprendizagem = 135 registros
# Modelo: Aprender padroes
# Treinamento = Aprender ocm exemplos anteriores
# Teste = verificar se o aprendizado funciona em exemplos reservados

#4. Pre-processar usando apenas informacoes do treinamento
medianas = X_treino.median()
X_treino = X_treino.fillna(medianas)
X_teste = X_teste.fillna(medianas)

#5. Criar e treinar a Árvore de decisão

modelo = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=42)
modelo.fit(X_treino, y_treino)

#6. Fazer previsões e avaliar o modelo
previsoes = modelo.predict(X_teste)
acuracia = accuracy_score(y_teste, previsoes)
matriz = confusion_matrix(
    y_teste, previsoes,
    labels = ["Precisa de Atenção", "Desempenho_satisfatorio"]
)

print(f"\nAcurácia do modelo: {acuracia*100:.2f}%")
print("\nMatriz de confusão: ")
print(matriz)

#7 Descobrir quais variaveis mais influenciaram as decisoes
importancias = pd.Series(modelo.feature_importances_, index=variaveis)
print("\nImportância das variáveis: ")
print(importancias.sort_values(ascending=False).round(3))

#8 Visualizar o padrão aprendido
plt.figure(figsize=(18,8))
plot_tree(modelo, feature_names=variaveis,class_names=modelo.classes_,filled=True, rounded=True, fontsize=9)
plt.title("Arvore de Decisão - Classificação do Desempenho ")
plt.tight_layout()
plt.show()

#9. Usar o modelo em um novo caso
novo_aluno = pd.DataFrame([{
    "horas_estudo_semana": 2.0, "frequencia_percentual": 65.0,
    "atividades_entregues": 4, "media_exercicios": 4.0,
    "participacao_aulas": 2, "acessos_plataforma_semana": 3,
    "faltas_mes": 6
}])

print("\nClassificação do novo aluno", modelo.predict(novo_aluno)[0])