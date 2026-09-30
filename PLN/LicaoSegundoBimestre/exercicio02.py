import nltk
import pandas

textos = pandas.read_excel("avaliacoes.xlsx")
textos1 = []
for texto in textos["avaliacao"]:
    palavras = set(nltk.word_tokenize(texto.lower()))
    for palavra in palavras:

        textos1.append(palavra)

texto1="O produto possui excelente qualidade, chegou rapidamente e atendeu completamente às minhas expectativas. Gostei muito da compra e recomendo este produto para outras pessoas."

texto2 = "Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

palavras1 = nltk.word_tokenize(texto1.lower())
p1 = set(palavras1)


interseccao = 0
p3 = []
for palavra1 in p1:
    for palavra2 in textos1:
        if (palavra1 == palavra2):
            interseccao += 1

uniao = (len(p1) + len(textos1)) - interseccao
print("Textos: ", len(textos1))
print(uniao)

jaccard = interseccao / uniao
print(f"{jaccard * 100 :.2f}%")
# print(f"Jaccard: {jaccard:.2f}%")
