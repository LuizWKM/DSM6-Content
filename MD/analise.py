import pandas as pd

dados = {
    'nome': ['Ana', 'Ano', 'Ona', 'Ono', 'Nan'],
    'idade': [21, 22, 33, 24, 25],
    'salario': [40000, 50000, 60000, 70000, 80000],
    'departamento': ['TI', 'Vendas', 'TI', 'Marketing', 'Vendas']
}

df = pd.DataFrame(dados)
#print(df)

#Ver as primeiras linhas
#print(df.head(1))

#print(df.describe())

print(df[df['idade']<=30])