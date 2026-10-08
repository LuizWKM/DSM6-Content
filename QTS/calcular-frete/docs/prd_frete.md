# Requisitos de Segurança e Eficiência - Calculadora de Frete

## Requisitos de Segurança (ISO 25010)
- A UF de destino deve ter exatamente 2 caracteres e conter exclusivamente letras do alfabeto (A-Z).
- Se a UF informada contiver números, caracteres especiais ou tamanho diferente de 2, o sistema deve lançar um erro `ValueError` com a mensagem: "UF deve conter exatamente 2 caracteres alfabéticos."
- Espaços extras no início ou no fim da UF devem ser removidos (sanitização) antes da validação.

## Requisitos de Eficiência (ISO 25010)
- Como a tabela de frete e regras de UF são fixas, consultas consecutivas com os mesmos parâmetros (mesmo peso e mesma UF) devem ser otimizadas para evitar recomputação.
- O sistema de cálculo de frete deve empregar um cache em memória limitado (lru_cache) com capacidade para até 128 registros.