import httpx
import pytest
from starlette.testclient import TestClient
from app.gateway_pagamento import (
    GatewayIndisponivelError,
    GatewayPagamentoError,
    GatewayPagamentoClient,
    GatewayTimeoutError
)

@pytest.mark.integration
@pytest.mark.mocks
def test_criar_pedido_aprovado_com_sucesso(
    client: TestClient,
    payload_pedido_valido: dict,
    resposta_gateway_sucesso: dict,
    mocker
):
    """ Testa o fluxo completo de criação de pedido com pagamento aprovado no gateway. """

    # Arrange: Mock da chamada externa ao gateway
    mock_gateway = mocker.patch(
        "app.service.GatewayPagamentoClient.processar_transacao",
        return_value=resposta_gateway_sucesso
    )

    # Act: Disparar requisição HTTP POST
    response = client.post("/pedidos", json=payload_pedido_valido)

    # Assert: Validar contrato e persistencia
    assert response.status_code == 201
    dados = response.json()
    assert dados["status"] == "PAGO"
    assert dados["transacao_id"] == "TX-99887766"
    assert dados["valor_total"] == 500.00
    assert "autorizada com sucesso" in dados["mensagem"]

    # Verificação do comportamento do Mock (spy)
    mock_gateway.assert_called_once_with(
        valor=500.00,
        metodo="PIX",
        cliente_cpf="12345678901",
        dados_pagamento={"chave_pix": "carlos.eduardo@exemplo.com"}
    )

    # Validação de persistencia no repostiório via endpoint GET
    pedido_id = dados["pedido_id"]
    get_response = client.get(f"/pedidos/{pedido_id}")
    assert get_response.status_code == 200
    pedido_salvo = get_response.json()
    assert pedido_salvo["id"] == pedido_id
    assert pedido_salvo["status"] == "PAGO"
    assert pedido_salvo["cliente"]["cpf"] == "12345678901"


@pytest.mark.integration
@pytest.mark.mocks
def test_criar_pedido_pagamento_recusado(
    client: TestClient,
    payload_pedido_valido: dict,
    resposta_gateway_recusado: dict,
    mocker
):
    """Testa integracao quando a operadora de pagamentos recusa a transacao."""
    # Arrange
    mocker.patch(
        "app.service.GatewayPagamentoClient.processar_transacao",
        return_value=resposta_gateway_recusado
    )

    # Act
    response = client.post("/pedidos", json=payload_pedido_valido)

    # Assert
    assert response.status_code == 201
    dados = response.json()
    assert dados["status"] == "FALHA_PAGAMENTO"
    assert dados["transacao_id"] is None
    assert "Saldo ou limite insuficiente" in dados["mensagem"]

    # Verifica se o pedido foi persistido com status de falha
    pedido_id = dados["pedido_id"]
    get_response = client.get(f"/pedidos/{pedido_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "FALHA_PAGAMENTO"


@pytest.mark.integration
@pytest.mark.mocks
def test_gateway_timeout_deve_retornar_http_504(
    client: TestClient,
    payload_pedido_valido: dict,
    mocker
):
    """Testa resiliencia da API diante de timeout na comunicacao com o gateway."""
    # Arrange
    mocker.patch(
        "app.service.GatewayPagamentoClient.processar_transacao",
        side_effect=GatewayTimeoutError("Servico demorou mais que 5 segundos.")
    )

    # Act
    response = client.post("/pedidos", json=payload_pedido_valido)

    # Assert
    assert response.status_code == 504
    assert "Gateway de pagamentos demorou a responder" in response.json()["detail"]

@pytest.mark.integration
@pytest.mark.mocks
def test_gateway_indisponivel_deve_retornar_http_503(
    client: TestClient,
    payload_pedido_valido: dict,
    mocker
):
    """Testa resiliencia da API quando o servico de pagamentos esta fora do ar."""
    # Arrange
    mocker.patch(
        "app.service.GatewayPagamentoClient.processar_transacao",
        side_effect=GatewayIndisponivelError("Conexao recusada pelo host remoto.")
    )

    # Act
    response = client.post("/pedidos", json=payload_pedido_valido)

    # Assert
    assert response.status_code == 503
    assert "temporariamente indisponivel" in response.json()["detail"]

@pytest.mark.integration
def test_obter_pedido_inexistente_deve_retornar_404(client: TestClient):
    """Testa busca por identificador de pedido inexistente."""
    response = client.get("/pedidos/id-inexistente-xyz")
    assert response.status_code == 404
    assert "nao encontrado" in response.json()["detail"]