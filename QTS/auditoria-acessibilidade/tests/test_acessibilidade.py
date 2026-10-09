import pytest
from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe
from pathlib import Path

HTML_FILE_PATH = f"file://{Path(__file__).parent.resolve()}/formulario.html"


@pytest.mark.accessibility
def test_auditoria_acessibilidade_wcag_aa(page: Page):
    # Arrange
    page.goto(HTML_FILE_PATH)

    # Act
    axe = Axe()
    results = axe.run(
        page,
        options={
            "runOnly" : {
                "type": "tag",
                "values": [ "wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]
            }
        }
    )

    # Formata a mensagem de erro caso existam violações
    violations = results.violations_count
    report = results.generate_report()

    # Assert 
    assert violations == 0, f"Foram encontradas {violations} violações de acessibilidade: \n {report}"