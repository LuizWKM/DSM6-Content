"""
Suite de testes unitários — Sistema de Pontuação
=================================================

Cobre as três funções de negócio do módulo app.business:

    calcular_xp(tempo_resposta: float) -> int
        XP ganho com base no tempo de resposta:
          - t <= 5 s   → 100 XP  (rápido)
          - t <= 15 s  →  50 XP  (médio)
          - t >  15 s  →  25 XP  (lento)

    verificar_resposta(resposta: str, gabarito: str) -> bool
        Compara resposta do aluno com gabarito de forma
        case-insensitive e ignorando espaços nas extremidades.

    calcular_nivel(xp_total: int) -> int
        Nível = xp_total // 1000 + 1

Técnicas aplicadas:
  - Análise de Valor de Fronteira (BVA)
  - Particionamento de Equivalência
  - Testes parametrizados (pytest.mark.parametrize)
"""

import pytest

from app.business import calcular_nivel, calcular_xp, verificar_resposta


# ===========================================================================
# 1. calcular_xp — XP por tempo de resposta
# ===========================================================================

class TestCalcularXpFronteiras:
    """Análise de Valor de Fronteira nas três faixas de tempo."""

    # --- Faixa rápida: t <= 5 s → 100 XP ---

    @pytest.mark.unit
    def test_tempo_zero_retorna_100(self):
        """t = 0 s: menor valor possível → 100 XP."""
        assert calcular_xp(0) == 100

    @pytest.mark.unit
    def test_tempo_4_9_retorna_100(self):
        """t = 4.9 s: imediatamente abaixo da fronteira → 100 XP."""
        assert calcular_xp(4.9) == 100

    @pytest.mark.unit
    def test_tempo_exatamente_5_retorna_100(self):
        """t = 5.0 s: fronteira inclusiva (<=5) → 100 XP."""
        assert calcular_xp(5.0) == 100

    @pytest.mark.unit
    def test_tempo_5_1_retorna_50(self):
        """t = 5.1 s: primeiro valor acima da faixa rápida → 50 XP."""
        assert calcular_xp(5.1) == 50

    # --- Faixa média: 5 < t <= 15 s → 50 XP ---

    @pytest.mark.unit
    def test_tempo_14_9_retorna_50(self):
        """t = 14.9 s: imediatamente abaixo da segunda fronteira → 50 XP."""
        assert calcular_xp(14.9) == 50

    @pytest.mark.unit
    def test_tempo_exatamente_15_retorna_50(self):
        """t = 15.0 s: fronteira inclusiva (<=15) → 50 XP."""
        assert calcular_xp(15.0) == 50

    @pytest.mark.unit
    def test_tempo_15_1_retorna_25(self):
        """t = 15.1 s: primeiro valor na faixa lenta → 25 XP."""
        assert calcular_xp(15.1) == 25

    # --- Faixa lenta: t > 15 s → 25 XP ---

    @pytest.mark.unit
    def test_tempo_alto_retorna_25(self):
        """t = 300 s: valor extremo na faixa lenta → 25 XP."""
        assert calcular_xp(300) == 25


class TestCalcularXpParticoes:
    """Particionamento de Equivalência: um valor representativo por classe."""

    @pytest.mark.unit
    @pytest.mark.parametrize("tempo, xp_esperado", [
        (2.0,  100),  # partição rápida  (0 < t <= 5)
        (10.0,  50),  # partição média   (5 < t <= 15)
        (30.0,  25),  # partição lenta   (t > 15)
    ])
    def test_xp_por_particao(self, tempo, xp_esperado):
        """Valor central de cada partição retorna o XP correto."""
        assert calcular_xp(tempo) == xp_esperado

    @pytest.mark.unit
    def test_xp_retorna_inteiro(self):
        """calcular_xp deve retornar sempre int, nunca float."""
        assert isinstance(calcular_xp(3.0), int)

    @pytest.mark.unit
    def test_xp_so_valores_validos(self):
        """Apenas 25, 50 e 100 são valores de retorno válidos."""
        valores_validos = {25, 50, 100}
        amostras = [0, 1, 5, 5.1, 10, 15, 15.1, 100, 999]
        for t in amostras:
            assert calcular_xp(t) in valores_validos, (
                f"calcular_xp({t}) retornou valor inesperado"
            )


# ===========================================================================
# 2. verificar_resposta — Verificação de resposta
# ===========================================================================

class TestVerificarResposta:
    """Cobre acertos, erros e variações de formatação."""

    # --- Casos de acerto ---

    @pytest.mark.unit
    def test_resposta_correta_identica(self):
        """Resposta idêntica ao gabarito → True."""
        assert verificar_resposta("print", "print") is True

    @pytest.mark.unit
    def test_resposta_correta_numerica(self):
        """Gabarito numérico: '42' == '42' → True."""
        assert verificar_resposta("42", "42") is True

    @pytest.mark.unit
    def test_resposta_ignora_espacos_antes_e_depois(self):
        """Espaços nas extremidades devem ser ignorados → True."""
        assert verificar_resposta("  print  ", "print") is True

    @pytest.mark.unit
    def test_resposta_ignora_maiusculas(self):
        """Comparação deve ser case-insensitive → True."""
        assert verificar_resposta("Print", "print") is True

    @pytest.mark.unit
    def test_resposta_ignora_maiusculas_e_espacos(self):
        """Combinação de maiúsculas e espaços → True."""
        assert verificar_resposta("  PRINT  ", "print") is True

    @pytest.mark.unit
    def test_gabarito_maiusculo_resposta_minuscula(self):
        """Gabarito em maiúsculas, resposta em minúsculas → True."""
        assert verificar_resposta("true", "True") is True

    # --- Casos de erro ---

    @pytest.mark.unit
    def test_resposta_incorreta_retorna_false(self):
        """Resposta diferente do gabarito → False."""
        assert verificar_resposta("5", "4") is False

    @pytest.mark.unit
    def test_resposta_vazia_gabarito_preenchido(self):
        """Resposta vazia para gabarito preenchido → False."""
        assert verificar_resposta("", "print") is False

    @pytest.mark.unit
    def test_resposta_parcialmente_correta(self):
        """Resposta que é subconjunto do gabarito → False."""
        assert verificar_resposta("prin", "print") is False

    @pytest.mark.unit
    def test_resposta_com_caractere_extra(self):
        """Resposta com caractere extra ao final → False."""
        assert verificar_resposta("print()", "print") is False

    # --- Parametrizado ---

    @pytest.mark.unit
    @pytest.mark.parametrize("resposta, gabarito, esperado", [
        ("4",       "4",       True),
        ("  4  ",   "4",       True),
        ("True",    "true",    True),
        ("FALSE",   "false",   True),
        ("x",       "y",       False),
        ("",        "algo",    False),
        ("print()", "print",   False),
    ])
    def test_verificar_resposta_parametrizado(self, resposta, gabarito, esperado):
        """Cobertura parametrizada de acertos, variações e erros."""
        assert verificar_resposta(resposta, gabarito) is esperado

    @pytest.mark.unit
    def test_verificar_retorna_bool(self):
        """verificar_resposta deve sempre retornar bool."""
        resultado = verificar_resposta("a", "a")
        assert isinstance(resultado, bool)


# ===========================================================================
# 3. calcular_nivel — Progressão de nível
# ===========================================================================

class TestCalcularNivel:
    """Verifica a fórmula nivel = xp // 1000 + 1 para fronteiras e valores altos."""

    @pytest.mark.unit
    def test_nivel_inicial_xp_zero(self):
        """Jogador sem XP começa no nível 1."""
        assert calcular_nivel(0) == 1

    @pytest.mark.unit
    def test_nivel_1_antes_da_virada(self):
        """999 XP: um ponto antes da virada → nível 1."""
        assert calcular_nivel(999) == 1

    @pytest.mark.unit
    def test_nivel_2_na_fronteira_exata(self):
        """1000 XP: fronteira exata → nível 2."""
        assert calcular_nivel(1000) == 2

    @pytest.mark.unit
    def test_nivel_2_logo_apos_virada(self):
        """1001 XP: um ponto após a virada → ainda nível 2."""
        assert calcular_nivel(1001) == 2

    @pytest.mark.unit
    def test_nivel_3_segunda_fronteira(self):
        """2000 XP: segunda fronteira exata → nível 3."""
        assert calcular_nivel(2000) == 3

    @pytest.mark.unit
    def test_nivel_6_com_5000_xp(self):
        """5000 XP: 5000 // 1000 + 1 = 6."""
        assert calcular_nivel(5000) == 6

    @pytest.mark.unit
    def test_nivel_retorna_inteiro(self):
        """calcular_nivel deve sempre retornar int."""
        assert isinstance(calcular_nivel(500), int)

    @pytest.mark.unit
    @pytest.mark.parametrize("xp, nivel_esperado", [
        (0,     1),
        (999,   1),
        (1000,  2),
        (1999,  2),
        (2000,  3),
        (2999,  3),
        (3000,  4),
        (4000,  5),
        (5000,  6),
        (9999, 10),
        (10000, 11),
    ])
    def test_nivel_parametrizado(self, xp, nivel_esperado):
        """Cobertura parametrizada das fronteiras de nível."""
        assert calcular_nivel(xp) == nivel_esperado


# ===========================================================================
# 4. Integração entre as três funções — Cenário de sessão de jogo
# ===========================================================================

class TestSessaoDeJogo:
    """
    Valida que calcular_xp, verificar_resposta e calcular_nivel
    funcionam corretamente em conjunto numa sessão de jogo simulada.
    """

    @pytest.mark.unit
    def test_xp_acumulado_10_respostas_rapidas(self):
        """10 respostas rápidas × 100 XP = 1000 XP → nível 2."""
        xp = sum(calcular_xp(3.0) for _ in range(10))
        assert xp == 1000
        assert calcular_nivel(xp) == 2

    @pytest.mark.unit
    def test_xp_acumulado_9_respostas_rapidas_permanece_nivel_1(self):
        """9 respostas rápidas × 100 XP = 900 XP → nível 1."""
        xp = sum(calcular_xp(3.0) for _ in range(9))
        assert xp == 900
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_xp_minimo_10_questoes(self):
        """10 respostas lentas × 25 XP = 250 XP → nível 1."""
        xp = sum(calcular_xp(30.0) for _ in range(10))
        assert xp == 250
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_resposta_correta_concede_xp_rapido(self):
        """
        Fluxo completo: verificar_resposta retorna True →
        calcular_xp(3.0) retorna 100 → nivel ainda 1 com 100 XP.
        """
        acertou = verificar_resposta("print", "print")
        xp = calcular_xp(3.0) if acertou else 0
        assert xp == 100
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_resposta_errada_nao_concede_xp(self):
        """
        Fluxo completo: verificar_resposta retorna False →
        XP não é concedido → nível permanece 1.
        """
        acertou = verificar_resposta("errado", "print")
        xp = calcular_xp(3.0) if acertou else 0
        assert xp == 0
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_jogo_misto_xp_e_nivel_final(self):
        """
        5 rápidas (500 XP) + 4 médias (200 XP) + 2 lentas (50 XP)
        = 750 XP → nível 1.
        """
        xp = 0
        xp += sum(calcular_xp(2.0) for _ in range(5))   # 5 × 100 = 500
        xp += sum(calcular_xp(10.0) for _ in range(4))  # 4 × 50  = 200
        xp += sum(calcular_xp(20.0) for _ in range(2))  # 2 × 25  =  50
        assert xp == 750
        assert calcular_nivel(xp) == 1
