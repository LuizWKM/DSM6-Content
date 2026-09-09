import nltk

texto= "No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

vocabulario = []

palavras = nltk.word_tokenize(texto.lower())

tamanho_original = len(palavras)

stop_words = nltk.corpus.stopwords.words("portuguese")

for palavra in palavras:
    if not(palavra in stop_words):
        vocabulario.append(palavra)

#print(stop_words)
tamanho_sem_stopwords = len(vocabulario)
print(vocabulario)

tamanho_sem_repetidos = len(set(vocabulario))

print("TAMANHO ORIGINAL:")
print(tamanho_original)

print("TAMANHO SEM STOPWORDS:")
print(tamanho_sem_stopwords)

print("TAMANHO SEM REPETIDOS:")
print(tamanho_sem_repetidos)

reducao = (1 - (tamanho_sem_repetidos/tamanho_original)) * 100
print("REDUCAO:")
print(reducao)