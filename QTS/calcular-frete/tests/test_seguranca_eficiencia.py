"""
Testes de Segurança e Eficiência — Calculadora de Frete
========================================================
Referência: docs/prd_frete.md (ISO 25010)

Segurança
---------
A UF de destino deve ter exatamente 2 caracteres e conter exclusivamente
letras do alfabeto (A-Z).  Se a entrada não atender a essa regra, o sistema
deve lançar ValueError com a mensagem exata:
    "UF deve conter exatamente 2 caracteres alfabéticos."
Espaços extras no início ou no fim da UF devem ser removidos (strip) antes
da validação — ou seja, "  SP  " é tratado como "SP" e é válido.

Eficiência
----------
O sistema deve empregar lru_cache com maxsize=128 em calcular_frete, de modo
que chamadas repetidas com os mesmos parâmetros retornem o resultado da cache
em vez de recomputar.

ATENÇÃO: os testes de conformidade abaixo *documentam o contrato do PRD*.
Enquanto app/main.py não estiver em conformidade com o PRD, alguns testes
falharão intencionalmente — esse é o comportamento esperado de uma suíte TDD
que guia a implementação.
"""

import pytest
from app.main import calcular_frete

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MSG_UF_INVALIDA = "UF deve conter exatamente 2 caracteres alfabéticos."


# ===========================================================================
# SEGURANÇA — Requisito ISO 25010: validação estrita da UF
# ===========================================================================

class TestSegurancaValidacaoUF:
    """Cobre todos os cenários de segurança descritos no prd_frete.md."""

    # --- Entradas com números --------------------------------------------------

    @pytest.mark.unit
    def test_uf_com_digito_unico(self):
        """UF '1P' contém número → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="1P")

    @pytest.mark.unit
    def test_uf_somente_numeros(self):
        """UF '12' contém apenas números → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="12")

    @pytest.mark.unit
    def test_uf_numero_no_final(self):
        """UF 'S2' contém número no final → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="S2")

    # --- Entradas com caracteres especiais ------------------------------------

    @pytest.mark.unit
    def test_uf_com_arroba(self):
        """UF '@P' contém caractere especial → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="@P")

    @pytest.mark.unit
    def test_uf_com_hifen(self):
        """UF 'S-' contém hífen → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="S-")

    @pytest.mark.unit
    def test_uf_com_ponto(self):
        """UF 'S.' contém ponto → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="S.")

    @pytest.mark.unit
    def test_uf_com_espaco_interno(self):
        """UF 'S P' possui espaço interno (não é trim) → deve ser inválida."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="S P")

    # --- Entradas com tamanho incorreto ---------------------------------------

    @pytest.mark.unit
    def test_uf_vazia(self):
        """UF vazia '' → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="")

    @pytest.mark.unit
    def test_uf_com_1_caractere(self):
        """UF 'S' com 1 caractere → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="S")

    @pytest.mark.unit
    def test_uf_com_3_caracteres(self):
        """UF 'SPP' com 3 caracteres → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="SPP")

    @pytest.mark.unit
    def test_uf_com_5_caracteres(self):
        """UF 'SPBRA' com 5 caracteres → ValueError com mensagem exata do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="SPBRA")

    # --- Sanitização (strip) antes da validação --------------------------------

    @pytest.mark.unit
    def test_uf_com_espacos_externos_valida(self):
        """UF '  SP  ' deve ter espaços removidos e ser aceita normalmente."""
        resultado = calcular_frete(peso=5.0, uf="  SP  ")
        assert resultado == 20.0

    @pytest.mark.unit
    def test_uf_com_espacos_externos_minusculo_valida(self):
        """UF '  sp  ' deve ser normalizada para 'SP' e aceita."""
        resultado = calcular_frete(peso=5.0, uf="  sp  ")
        assert resultado == 20.0

    @pytest.mark.unit
    def test_uf_com_espacos_externos_regiao_norte_valida(self):
        """UF '  AM  ' deve ser normalizada e retornar frete com adicional Norte."""
        resultado = calcular_frete(peso=5.0, uf="  AM  ")
        assert resultado == 35.0

    @pytest.mark.unit
    def test_uf_somente_espacos_apos_strip_vira_vazia(self):
        """UF '   ' após strip fica vazia → deve ser rejeitada."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf="   ")

    # --- Parametrização cobrindo múltiplas entradas inválidas -----------------

    @pytest.mark.unit
    @pytest.mark.parametrize("uf_invalida", [
        "1P",    # número no início
        "P1",    # número no fim
        "12",    # apenas números
        "@P",    # caractere especial
        "S-",    # hífen
        "S.",    # ponto
        "S P",   # espaço interno
        "",      # vazia
        "S",     # 1 caractere
        "SPP",   # 3 caracteres
        "SPBRA", # 5 caracteres
        "   ",   # somente espaços
    ])
    def test_uf_invalida_parametrizada(self, uf_invalida):
        """Garante que todas as entradas malformadas levantam ValueError com mensagem do PRD."""
        with pytest.raises(ValueError, match=MSG_UF_INVALIDA):
            calcular_frete(peso=5.0, uf=uf_invalida)


# ===========================================================================
# EFICIÊNCIA — Requisito ISO 25010: lru_cache com maxsize=128
# ===========================================================================

class TestEficienciaCache:
    """Cobre todos os cenários de eficiência descritos no prd_frete.md."""

    def setup_method(self):
        """Limpa o cache antes de cada teste para garantir isolamento."""
        if hasattr(calcular_frete, "cache_clear"):
            calcular_frete.cache_clear()

    # --- Presença e configuração do cache -------------------------------------

    @pytest.mark.unit
    def test_funcao_possui_cache_info(self):
        """calcular_frete deve expor cache_info(), confirmando que lru_cache foi aplicado."""
        assert hasattr(calcular_frete, "cache_info"), (
            "calcular_frete não possui cache_info — lru_cache não foi aplicado."
        )

    @pytest.mark.unit
    def test_cache_maxsize_e_128(self):
        """O lru_cache deve ter maxsize=128 conforme o PRD."""
        info = calcular_frete.cache_info()
        assert info.maxsize == 128, (
            f"maxsize esperado: 128, obtido: {info.maxsize}"
        )

    @pytest.mark.unit
    def test_funcao_possui_cache_clear(self):
        """calcular_frete deve expor cache_clear() — parte da interface de lru_cache."""
        assert hasattr(calcular_frete, "cache_clear"), (
            "calcular_frete não possui cache_clear — lru_cache não foi aplicado."
        )

    # --- Comportamento do cache: hits e misses --------------------------------

    @pytest.mark.unit
    def test_primeira_chamada_e_miss(self):
        """A primeira chamada com determinados argumentos deve resultar em miss."""
        calcular_frete(peso=5.0, uf="SP")
        info = calcular_frete.cache_info()
        assert info.misses >= 1, "Esperava ao menos 1 miss após primeira chamada."

    @pytest.mark.unit
    def test_chamada_repetida_incrementa_hits(self):
        """Chamadas repetidas com os mesmos parâmetros devem incrementar hits no cache."""
        calcular_frete(peso=5.0, uf="SP")   # miss
        calcular_frete(peso=5.0, uf="SP")   # hit
        info = calcular_frete.cache_info()
        assert info.hits >= 1, (
            "Esperava ao menos 1 hit após chamada repetida com mesmos argumentos."
        )

    @pytest.mark.unit
    def test_multiplas_chamadas_repetidas_acumulam_hits(self):
        """Múltiplas repetições acumulam hits proporcionalmente."""
        for _ in range(5):
            calcular_frete(peso=5.0, uf="SP")
        info = calcular_frete.cache_info()
        # 1 miss (primeira chamada) + 4 hits
        assert info.hits >= 4, (
            f"Esperava ao menos 4 hits, obteve {info.hits}."
        )

    @pytest.mark.unit
    def test_parametros_distintos_geram_entradas_separadas(self):
        """Parâmetros diferentes criam entradas separadas no cache (sem colisão)."""
        calcular_frete(peso=5.0, uf="SP")   # miss
        calcular_frete(peso=15.0, uf="SP")  # miss (peso diferente)
        calcular_frete(peso=5.0, uf="AM")   # miss (uf diferente)
        info = calcular_frete.cache_info()
        assert info.misses >= 3, (
            "Combinações distintas de parâmetros devem gerar misses separados."
        )

    @pytest.mark.unit
    def test_cache_retorna_mesmo_valor_em_hits(self):
        """O valor retornado pelo cache deve ser idêntico ao da computação original."""
        primeiro = calcular_frete(peso=5.0, uf="SP")
        segundo = calcular_frete(peso=5.0, uf="SP")  # vem do cache
        assert primeiro == segundo, (
            "O valor retornado pelo cache diverge do valor calculado originalmente."
        )

    @pytest.mark.unit
    def test_cache_clear_zera_hits_e_misses(self):
        """Após cache_clear(), hits e misses devem ser zerados."""
        calcular_frete(peso=5.0, uf="SP")
        calcular_frete(peso=5.0, uf="SP")
        calcular_frete.cache_clear()
        info = calcular_frete.cache_info()
        assert info.hits == 0 and info.misses == 0, (
            "cache_clear() deve zerar hits e misses."
        )

    @pytest.mark.unit
    def test_cache_currsize_cresce_com_novas_entradas(self):
        """currsize deve refletir o número de entradas distintas armazenadas."""
        calcular_frete(peso=5.0, uf="SP")
        calcular_frete(peso=5.0, uf="AM")
        info = calcular_frete.cache_info()
        assert info.currsize >= 2, (
            f"Esperava currsize >= 2, obteve {info.currsize}."
        )

    # --- Capacidade máxima (128 entradas) ------------------------------------

    @pytest.mark.unit
    def test_cache_nao_excede_maxsize(self):
        """O cache não deve armazenar mais de maxsize=128 entradas (comportamento LRU)."""
        # Alimenta o cache com 130 combinações únicas de peso (UF fixo)
        for i in range(1, 131):
            try:
                calcular_frete(peso=float(i), uf="SP")
            except ValueError:
                pass  # pesos > 30 levantam ValueError, ignoramos aqui

        info = calcular_frete.cache_info()
        assert info.currsize <= 128, (
            f"currsize {info.currsize} excede maxsize 128 — lru_cache não está limitando."
        )
