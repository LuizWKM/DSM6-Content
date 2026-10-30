import nltk
import pandas

textos = pandas.read_excel("avaliacoes.xlsx")
textos1 = []

texto1 ="O produto possui excelente qualidade, chegou rapidamente e atendeu completamente às minhas expectativas. Gostei muito da compra e recomendo este produto para outras pessoas."

texto2 = "O produto possui péssima qualidade, apresentou problemas logo após a compra e não atendeu às minhas expectativas. Fiquei muito decepcionado e não recomendo este produto."

palavras1 = nltk.word_tokenize(texto1.lower())
palavras2 = nltk.word_tokenize(texto2.lower())

for texto in textos["avaliacao"]:
    palavras = set(nltk.word_tokenize(texto.lower()))
    for palavra in palavras:
        textos1.append(palavra)


t1 = set(textos1)
p1 = set(palavras1)
p2 = set(palavras2)

interseccao_positiva = 0
interseccao_negativa = 0
p3 = []

# Referência positiva
for palavra1 in p1:
    for palavra2 in t1:
        if (palavra1 == palavra2):
            interseccao_positiva += 1

# Referência negativa
for palavra1 in p2:
    for palavra2 in t1:
        if (palavra1 == palavra2):
            interseccao_negativa += 1



uniao_positiva = (len(p1) + len(t1)) - interseccao_positiva
uniao_negativa = (len(p2) + len(t1)) - interseccao_negativa
print("Textos: ", len(t1))
print(uniao_positiva)
print(uniao_negativa)

jaccard_positivo = interseccao_positiva / uniao_positiva
jaccard_negativo = interseccao_negativa / uniao_negativa
print(f"{jaccard_positivo * 100 :.2f}%")
print(f"{jaccard_negativo * 100 :.2f}%")
# print(f"Jaccard: {jaccard:.2f}%")