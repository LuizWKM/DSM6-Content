import pandas as pd

import re 
#Trabalha com expressões regulares, limpar dados e remover caracteres indesejados

import unicodedata
#Tratamento de caracteres Unicode, remover acentos e ajudar na padronização de textos.

from pathlib import Path
#Permite localizar o arquivo CSV de forma mais segura, independentemente da pasta em que o terminal foi aberto.

from sklearn.preprocessing import MinMaxScaler
#ferramenta de Normalização, transformar valores numericos para uma escala entre 0 e 1

from sklearn.preprocessing import StandardScaler
#Ferrramenta de padronização Z-score, os dados ficaram com média próxima de 0 e desvio-padrão proximo de 1.

from sklearn.preprocessing import RobustScaler
#Ferramenta de transformacao mais resistente a outliners, utiliza a medina e os quartis, em vez da média e do desvio-padrão

from sklearn.model_selection import train_test_split
#Função utilizada para dividir uma base de dados em conjunto de treinamento e conjuto de teste. É importe para avaliar modelos de MAchine Learning utilizando dados que não participam do treinamento.

#Configuração

#Localizar o CSV na mesma pasta do programa
arquivo = Path(__file__).resolve().parent / 'base_ecommerce_brasil_2026_suja.csv'

#Carregar a base externa
df=pd.read_csv(arquivo, sep=';', encoding='utf-8')

#Fução auxiliar: remove acentos, pontuação e difereças de maiusculo/minusculo.
def padronizar(valor):
    if pd.isna(valor):
        return valor

    valor = str(valor).strip().upper()
    valor = ''.join(
        letra for letra in unicodedata.normalize('NFKD',valor)
        if not unicodedata.combining(letra)
    )
    valor = re.sub(r'[^A-Z0-9]','',valor)
    return re.sub(r'\s+',' ',valor)

# Conhecer a base sem alterar nada.
print('Linhas Recebidas:', len(df))
print('Duplicado Exatos:', df.duplicated().sum())
print('IDs de pedido repetidos:', df.duplicated('id_pedido').sum())
print('Pedidos Unicos:', df['id_pedido'].nunique())

#Remover apenas as linhas totalmente iguais
limpo = df.drop_duplicates().copy()

#Padronizar campos textuais importes.
limpo['nome_cliente'] = limpo['nome_cliente'].str.strip().str.title()
limpo['email'] = limpo['email'].str.strip().str.lower()
limpo['telefone'] = limpo['telefone'].str.replace(r'\D','',regex=True)
limpo['data_pedido'] = pd.to_datetime(limpo['data_pedido'],errors='coerce', dayfirst=True, format='mixed').dt.strftime('%Y-%m-%d')

#Estados escritos por extenso serão convertidos para suas siglas
mapa_uf = {
    'ACRE':'AC','ALAGOAS':'AL', 'AMAPA':'AP', 'AMAZONAS':'AM', 'BAHIA':'BA',
    'CEARA':'CE', 'DISTRITO FEDERAL':'DF','ESPIRITO SANTO':'ES', 'GOIAS':'GO',
    'MARANHAO':'MA','MATO GROSSO':'MT', 'MATO GROSSO DO SUL':'MS',
    'MINAS GERAIS':'MG','PARA':'PA','PARAIBA':'PB','PARANA':'PR',
    'PERNAMBUCO':'PE', 'PIAUI':'PI', 'RIO DE JANEIRO':'RJ',
    'RIO GRANDE DO NORTE':'RN', 'RIO GRANDE DO SUL':'RS', 'RONDONIA':'RO',
    'RORAIMA':'RR', 'SANTA CATARINA':'SC', 'SAO PAULO':'SP', 'SERGIPE':'SE', 'TOCANTINS':'TO'
}

limpo['estado'] = limpo['estado'].map(padronizar).replace(mapa_uf)

#categorias diferentes que significam a mesma coisa recebem um unico padrão
limpo['forma_pagamento']=(limpo['forma_pagamento'].map(padronizar).replace({
    'PAGMENTO INSTANTANEO':'PIX',
    'CARTAOCREDITO':'CARTAO_CREDITO',
    'CARTAO CREDITO':'CARTAO_CREDITO',
    'CARTAODEBITO':'CARTAO_DEBITO',
    'CARTAO DEBITO':'CARTAO_DEBITO',
    'DEBITO':'CARTAO_DEBITO',
    'BOLETO BANCARIO':'BOLETO',
    'CARTEIRADIGITAL':'CARTEIRA_DIGITAL',
    'CARTEIRA DIGITAL':'CARTEIRA_DIGITAL',
    'WALLET':'CARTEIRA_DIGITAL',
}))

limpo['canal_venda'] = (
    limpo['canal_venda'].map(padronizar).replace({
        'APLICATIVO':'APP',
        'WEB':'SITE',
        'MARKET PLACE':'MARKETPLACE',
        'LOJAFISICA':'LOJA_FISICA',
        'LOJA FISICA':'LOJA_FISICA',
        'PDV':'LOJA_FISICA',
    })
)

limpo['dispositivo']=limpo['dispositivo'].map(padronizar)
limpo['categoria_produto']=limpo['categoria_produto'].map(padronizar)

#Após padronizar, registros antes "diferentes" podem se tornar iguais
print('Duplicados revelados após padronizacao:', limpo.duplicated().sum())
#Remover essas duplicidade
limpo = limpo.drop_duplicates().copy()
print('Linhas após limpeza:', len(limpo))
print('Estados após padronização:', limpo['estado'].nunique())
print('Formas de Pagamento:', limpo['forma_pagamento'].nunique())
print('Canais de Vendas:', limpo['canal_venda'].nunique())

#Padronização e Normalização
variaveis = ['idade_cliente','renda_mensal','valor_total']

#Mostra como idade, renda e valor de compra possum escalas muito diferentes
print('\nEscala Original:')
print(limpo[variaveis].agg(['min','max','mean']).round(2))

#Min - Max transforma cada atributo para o intervalo de 0 a 1
limpo[['idade_minmax', 'renda_minmax','valor_minmax']]=(MinMaxScaler().fit_transform(limpo[variaveis]))

#Z-score deixar a média proxima a 0 eo desvio-padrão proximo a 1.
limpo[['idade_z','renda_z','valor_z']]=(StandardScaler().fit_transform(limpo[variaveis]))

# RobustScaler uma a mediana e quartis, sendo útil quando existem outliers.
limpo['renda_robusta']=(RobustScaler().fit_transform(limpo[['renda_mensal']]).ravel())

print('\nExemplo das transformações:')
print (
    limpo[
        ['idade_cliente','idade_minmax','idade_z',
        'renda_mensal','renda_minmax','renda_z','renda_robusta']
    ].head(5).round(3).to_string(index=False)
)

# Discritização e Binarização

#CUT: transforma idade contínua em faixas definidas pelo problema.

limpo['faixa_etaria'] = pd.cut( #pd.cut(): divide os valores em intervalos.
    limpo['idade_cliente'],# coluna com a idade de cada cliente.
    bins=[17,24,34,44,54,64,120], # define os limites das faixas.
    labels=['18-24','25-34','35-44','45-54','55-64','65+']) #dá um nome para cada faixa.

#QCUT: divide o valor das compras em quatro grupos com quantidades semelhantes

limpo['faixa_ticket'] = pd.qcut( #divide os dados em quantis, tentando colocar aproximadamente a mesma quantidade de clientes em cada grupo.
    limpo['valor_total'],
    q=4, #cria 4 grupos (quartis).
    labels=['Baixo','Medio-baixo','Medio-alto','Alto']
)

#Binarização: acima de R$ 1.000 recebe 1; caso contrário, recebe 0.
limpo['alto_ticket']=(limpo['valor_total']>1000).astype(int)

print('\nFaixas Etárias:')
print (limpo['faixa_etaria'].value_counts(sort=False))

print('\nFaixas de Ticket:')
print (limpo['faixa_ticket'].value_counts(sort=False))

print('\nPedidos acima de R$1.000,00:')
print (limpo['alto_ticket'].value_counts().sort_index())
print (f"Percentual de alto ticket:{limpo['alto_ticket'].mean()*100:.2f}%")

#Codificação de Variáveis Categóricas
## One-Hot: cria uma coluna 0/1 para cada categoria, sem inventar uma ordem.

modelo = pd.get_dummies(
    limpo,
    columns=['forma_pagamento','canal_venda','dispositivo'],
    dtype=int
)

dummies = [
    c for c in modelo.columns
    if c.startswith(('forma_pagamento_','canal_venda_','dispositivo_'))
    ]

print ('Colunas criadas pelo One-Hot:', len(dummies))
print(dummies)

#Labe/Ordinal Enconding: como fidelidade possui ordem natural, usamos numeros que representam Bronze < Prata < Ouro < Diamante.

ordem = {'BRONZE': 0, 'PRATA': 1, 'OURO': 2, 'DIAMANTE': 3}
limpo['fidelidade_cod'] = limpo['nivel_fidelidade'].str.upper().map(ordem)

print('\nCodificação da Fidelidade: ')
print(
    limpo[['nivel_fidelidade', 'fidelidade_cod']]
    .drop_duplicates()
    .sort_values('fidelidade_cod')
    .to_string(index=False)
)

# Target Encoding precisa aprender SOMENTE com o treino, evitando que informações do teste vazem para o modelo.
treino,teste = train_test_split(
    limpo,
    test_size=0.25,
    random_state=42,
    stratify=limpo['recomprou_90d']
)

media_global = treino['recomprou_90d'].mean()
mapa_target = treino.groupby('id_parceiro')['recomprou_90d'].mean()
teste = teste.copy()
teste['parceiro_te']=(
    teste['id_parceiro'].map(mapa_target).fillna(media_global)
)

print("\nTreino:", len(treino), '|Teste:', len(teste))
print(f'Média global de recompra: {100 * media_global:.3f}%')

print('\nExemplo de Target Encoding:')
print(
    teste[['id_parceiro', 'recomprou_90d', 'parceiro_te']]
    .head(8)
    .round(3)
    .to_string(index=False)
)

# Resumo
print('\n === Resumo do Pré-Processamento ===')
print('Base Recebida:', len(df), 'linhas')
print('Base Limpa:', len(limpo), 'linhas')
print('O dado passou por: limpeza -> transformação -> discritização')