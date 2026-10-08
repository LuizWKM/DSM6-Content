import pytest
from starlette.testclient import TestClient
from tests.factories import ClienteFactory, CriarPedidoRequestFactory, ItemPedidoFactory
from app.schemas import MetodoPagamento, StatusPedido

@pytest.mark.synthetic_data
@pytest.mark.integration
def test_criar_pedido_com_dados_sinteticos_fake_factory(
    client: TestClient,
    resposta_gateway_sucesso: dict,
    mocker
):
    """ Testa integração de pedido utilizando carga de dados gerada via Faker """
    # Arrange Constroi requisição sintética completa
    requisicao = CriarPedidoRequestFactory.build()
    mocker.patch(
        "app.service.GatewayPagamentoClient.processar_transacao",
        return_value = resposta_gateway_sucesso
    )

    # Act
    response = client.post("/pedidos", json=requisicao.model_dump())

    # Assert
    assert response.status_code == 201
    dados = response.json()
    assert dados["status"] == StatusPedido.PAGO.value
    assert dados["transacao_id"] == "TX-99887766"

    # Confirmar que o valor total bate com a soma exata dos itens sintéticos
    total_esperado = round(sum(i.quantidade * i.preco_unitario for i in requisicao.itens), 2)
    assert dados["valor_total"] == total_esperado

    # Consulta no endpoint para verificar a integridade dos dados sintéticos persistidos
    pedido_id = dados["pedido_id"]
    get_res = client.get(f"/pedidos/{pedido_id}")
    assert get_res.status_code == 200
    pedido_banco = get_res.json()
    assert pedido_banco["cliente"]["nome"] == requisicao.cliente.nome
    assert pedido_banco["cliente"]["cpf"] == requisicao.cliente.cpf
    assert len(pedido_banco["itens"]) == len(requisicao.itens)