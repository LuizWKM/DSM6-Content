import random 
from faker import Faker 
from app.schemas import Cliente, CriarPedidoRequest, ItemPedido, MetodoPagamento

fake = Faker("pt_BR")

class ClienteFactory:
    @classmethod
    def build(cls, **kwargs) -> Cliente:
        cpf_bruto = fake.cpf()
        dados = {
            "nome": fake.name(),
            "email": fake.email(),
            "cpf": "".join(filter(str.isdigit, cpf_bruto))
        }
        dados.update(kwargs)
        return Cliente(**dados)

class ItemPedidoFactory:
    """  Gerador de dados sintéticos para itens de pedido """
    @classmethod
    def build(cls, **kwargs) -> ItemPedido:
        dados = {
            "produto_id": f"PROD-{fake.unique.random_int(min=1000, max=9999)}",
            "nome": fake.word().capitalize() + " " + fake.word().capitalize(),
            "quantidade": random.randint(1, 5),
            "preco_unitario": round(random.uniform(10.0, 500.0), 2),
        }
        dados.update(kwargs)
        return ItemPedido(**dados)

    @classmethod
    def build_batch(cls, size: int = 3, **kwargs) -> list[ItemPedido]:
        return [cls.build(**kwargs) for _ in range(size)]

class CriarPedidoRequestFactory:
    """ Factory para criação de requisições de pedido completas e válidas """

    @classmethod
    def build(cls, **kwargs) -> CriarPedidoRequest:
        itens = kwargs.pop("itens", None) or ItemPedidoFactory.build_batch(size=random.randint(1, 4))
        cliente = kwargs.pop("client", None) or ClienteFactory.build()
        metodo = kwargs.pop("metodo_pagamento", random.choice(list(MetodoPagamento)))

        dados_pagamento = {}

        if metodo == MetodoPagamento.PIX:
            dados_pagamento = {"chave_pix": cliente.email}
        elif metodo == MetodoPagamento.CARTAO_CREDITO:
            dados_pagamento = {
                "numero_cartao": fake.credit_card_number(card_type="mastercard"),
                "cvv": fake.credit_card_security_code(),
                "titular": cliente.nome
                               }
            dados = {
                "cliente": cliente,
                "itens": itens,
                "metodo_pagamento": metodo,
                "dados_pagamento": dados_pagamento
            }
            dados.update(kwargs)
            return CriarPedidoRequest(**dados)