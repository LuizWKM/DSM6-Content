import nltk

texto1="No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra."

texto2 = "Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

palavras1 = nltk.word_tokenize(texto1.lower())
palavras2 = nltk.word_tokenize(texto2.lower())
p1 = set(palavras1)
p2 = set(palavras2)

interseccao = 0
p3 = []
for palavra1 in p1:
    for palavra2 in p2:
        if (palavra1 == palavra2):
            interseccao += 1

uniao = (len(p1) + len(p2)) - interseccao
# for palavra1 in p1:
#     p3.append(palavra1)
# for palavra2 in p2:
#     p3.append(palavra2)            

# palavras_diferentes = set(p3)
# uniao = len(palavras_diferentes)
# print(uniao)
# print(interseccao)
# print(len(p1))
# print(len(p2))

jaccard = interseccao / uniao
print(f"Jaccard: {jaccard:.2f}%")
