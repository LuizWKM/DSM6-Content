from playwright.sync_api import Locator, Page
from pages.base_pages import BasePage

class CampanhasPage(BasePage):
    """Encapsula a gestao e o cadastro de campanhas solidarias."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.titulo_painel: Locator = page.get_by_role("heading", name="Painel de Campanhas")
        self.botao_nova_campanha: Locator = page.get_by_role("button", name="Nova Campanha")
        self.campo_titulo: Locator = page.get_by_label("Titulo da Acao")
        self.campo_meta: Locator = page.get_by_label("Meta de Arrecadacao (R$)")
        self.campo_categoria: Locator = page.get_by_label("Categoria")
        self.botao_salvar: Locator = page.get_by_role("button", name="Salvar Campanha")
        self.campo_busca: Locator = page.get_by_placeholder("Buscar campanhas...")
        self.notificacao_status: Locator = page.get_by_role("status")
        self.alerta_erro: Locator = page.get_by_role("alert")
        self.tabela_campanhas: Locator = page.get_by_role("table")

    def acessar_painel(self, base_url: str) -> None:
        """Acessa a tela de campanhas."""
        self.navegar_para(f"{base_url}/campanhas")

    def cadastrar_campanha(self, titulo: str, meta: str, categoria: str) -> None:
        """Preenche e salva uma nova campanha."""
        self.botao_nova_campanha.click()
        self.campo_titulo.fill(titulo)
        self.campo_meta.fill(meta)
        self.campo_categoria.select_option(categoria)
        self.botao_salvar.click()

    def filtrar_campanhas(self, termo: str) -> None:
        """Filtra as campanhas na tabela."""
        self.campo_busca.fill(termo)

    def obter_linha_campanha(self, titulo: str) -> Locator:
        """Retorna o localizador da linha correspondente ao titulo da campanha."""
        return self.tabela_campanhas.get_by_role("row", name=titulo)