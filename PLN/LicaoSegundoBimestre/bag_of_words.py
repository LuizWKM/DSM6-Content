import nltk
import string
from collections import Counter
import numpy as np

textos = [ "Vontade, única loucura feita para a estocada de novos horizontes.", "Como é bom ver um novo mundo.", "Boa tarde, novidade no blog, um novo lutador foi criado para o jogo, fiquem ligados para outras novidades."]

textos_limpos = []

stop_words = nltk.corpus.stopwords.words("portuguese")
vocabulario = []
def bag_of_words(texts, words):
    size_x = len(words)
    size_y = len(texts)
    matrix = np.zeros ((size_x, size_y))

    for x in range(1, size_x):
        for y in range(1, size_y):
            if (words[x] in texts[y]):
                matrix[x,y] = 1
            else:
                matrix[x,y] = 0
                
for texto in textos:
    palavras = nltk.word_tokenize(texto.lower())
    palavras = [palavra for palavra in palavras if palavra not in string.punctuation]
    texto_limpo = "".join([c for c in texto.lower() if c not in string.punctuation])

    for palavra in palavras:
        if  not(palavra in stop_words):
            vocabulario.append(palavra)

frequencia_pares = Counter(vocabulario)

p1 = set(vocabulario)
