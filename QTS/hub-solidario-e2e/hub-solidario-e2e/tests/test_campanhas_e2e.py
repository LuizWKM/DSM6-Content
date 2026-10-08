import pytest
from playwright.sync_api import Page, expect
from pages.campanhas_page import CampanhasPage

@pytest.mark.e2e
def test_cadastro_de_nova_campanha_com_sucesso(page: Page, server_url: str):
    """ Valida o cadastro e inclusão de nova campanha na tabela """
    # Arrange
    campanhas_page = CampanhasPage(page)
    campanhas_page.acessar_painel(server_url)

    # Act
    campanhas_page.cadastrar_campanha(
        titulo="Mochila Solidaria 2026",
        meta="18000.0",
        categoria="Material Escolar",
    )

    # Assert
    expect(campanhas_page.notificacao_status).to_be_visible()
    expect(campanhas_page.notificacao_status).to_contain_text("Campanha cadastrada com sucesso")
    expect(campanhas_page.obter_linha_campanha("Mochila Solidaria 2026")).to_be_visible()

@pytest.mark.e2e
def test_validacao_de_campos_obrigatorios_ao_salvar_campanha(page: Page, server_url: str):
    """ Valida que a tentativa de submeter o formulario vazio exibe alerta de erro. """
    # Arrange
    campanhas_page = CampanhasPage(page)
    campanhas_page.acessar_painel(server_url)

    # Act
    campanhas_page.botao_nova_campanha.click()
    campanhas_page.botao_salvar.click()

    # Assert
    expect(campanhas_page.alerta_erro).to_be_visible()
    expect(campanhas_page.alerta_erro).to_contain_text("Preencha todos os campos obrigatorios")