"""
Suite de testes unitários — Motor de Gamificação
=================================================

Cobre as três funções de negócio responsáveis pela progressão do jogador:

    calcular_xp(tempo_resposta: float) -> int
        Retorna o XP ganho com base no tempo de resposta:
          - t <= 5 s   → 100 XP  (rápido)
          - t <= 15 s  → 50 XP   (médio)
          - t >  15 s  → 25 XP   (lento)

    calcular_nivel(xp_total: int) -> int
        Nível = xp_total // 1000 + 1

    subiu_de_nivel(xp_antes: int, xp_depois: int) -> bool
        True quando calcular_nivel(xp_depois) > calcular_nivel(xp_antes)

Técnicas aplicadas:
  - Análise de Valor de Fronteira (BVA)
  - Particionamento de Equivalência
  - Testes parametrizados (pytest.mark.parametrize)
  - Cenário de acumulação progressiva (smoke end-to-end unitário)
"""

import pytest

from app.business import calcular_nivel, calcular_xp, subiu_de_nivel


# ===========================================================================
# 1. calcular_xp — Análise de Valor de Fronteira
# ===========================================================================
class TestCalcularXpFronteiras:
    """
    Valida os pontos exatos nas fronteiras das três faixas de tempo.
    Qualquer off-by-one na condição (<= vs <) é capturado aqui.
    """

    # -----------------------------------------------------------------------
    # Fronteira inferior: t <= 5 s → 100 XP
    # -----------------------------------------------------------------------

    @pytest.mark.unit
    def test_tempo_zero_retorna_100(self):
        """t = 0 s: menor valor possível → 100 XP."""
        assert calcular_xp(0) == 100

    @pytest.mark.unit
    def test_tempo_abaixo_de_5_retorna_100(self):
        """t = 4.9 s: imediatamente antes da fronteira → 100 XP."""
        assert calcular_xp(4.9) == 100

    @pytest.mark.unit
    def test_tempo_exatamente_5_retorna_100(self):
        """t = 5.0 s: INCLUSO na faixa rápida (<=5) → 100 XP."""
        assert calcular_xp(5.0) == 100

    @pytest.mark.unit
    def test_tempo_5_1_retorna_50(self):
        """t = 5.1 s: primeiro ponto na faixa média → 50 XP."""
        assert calcular_xp(5.1) == 50

    # -----------------------------------------------------------------------
    # Fronteira intermediária: t <= 15 s → 50 XP
    # -----------------------------------------------------------------------

    @pytest.mark.unit
    def test_tempo_abaixo_de_15_retorna_50(self):
        """t = 14.9 s: imediatamente antes da segunda fronteira → 50 XP."""
        assert calcular_xp(14.9) == 50

    @pytest.mark.unit
    def test_tempo_exatamente_15_retorna_50(self):
        """t = 15.0 s: INCLUSO na faixa média (<=15) → 50 XP."""
        assert calcular_xp(15.0) == 50

    @pytest.mark.unit
    def test_tempo_15_1_retorna_25(self):
        """t = 15.1 s: primeiro ponto na faixa lenta → 25 XP."""
        assert calcular_xp(15.1) == 25

    # -----------------------------------------------------------------------
    # Faixa lenta: t > 15 s → 25 XP
    # -----------------------------------------------------------------------

    @pytest.mark.unit
    def test_tempo_muito_alto_retorna_25(self):
        """t = 300 s: valor extremo na faixa lenta → 25 XP."""
        assert calcular_xp(300) == 25


# ===========================================================================
# 2. calcular_xp — Particionamento de Equivalência
# ===========================================================================
class TestCalcularXpParticoes:
    """
    Um valor representativo por partição confirma o comportamento
    de toda a classe sem repetir as fronteiras já testadas acima.
    """

    @pytest.mark.unit
    @pytest.mark.parametrize("tempo, xp_esperado", [
        (1.0,  100),   # partição rápida  (0 < t <= 5)
        (7.5,   50),   # partição média   (5 < t <= 15)
        (30.0,  25),   # partição lenta   (t > 15)
    ])
    def test_xp_por_particao(self, tempo, xp_esperado):
        """Valor central de cada partição retorna o XP correto."""
        assert calcular_xp(tempo) == xp_esperado

    @pytest.mark.unit
    def test_xp_retorna_inteiro(self):
        """A função deve retornar sempre um int, nunca float."""
        resultado = calcular_xp(3.0)
        assert isinstance(resultado, int)

    @pytest.mark.unit
    def test_xp_valores_possiveis_sao_apenas_tres(self):
        """Apenas 25, 50 e 100 são valores válidos de retorno."""
        valores_validos = {25, 50, 100}
        amostras = [0, 1, 5, 5.1, 10, 15, 15.1, 100, 999]
        for t in amostras:
            assert calcular_xp(t) in valores_validos, (
                f"calcular_xp({t}) retornou valor inesperado"
            )


# ===========================================================================
# 3. calcular_nivel — Progressão de nível
# ===========================================================================
class TestCalcularNivel:
    """
    Verifica que nivel = xp // 1000 + 1 está implementado corretamente
    para o nível inicial, fronteiras de virada e valores altos.
    """

    @pytest.mark.unit
    def test_nivel_inicial_xp_zero(self):
        """Jogador sem XP começa no nível 1."""
        assert calcular_nivel(0) == 1

    @pytest.mark.unit
    def test_nivel_1_antes_da_virada(self):
        """999 XP: um ponto antes da virada — ainda nível 1."""
        assert calcular_nivel(999) == 1

    @pytest.mark.unit
    def test_nivel_2_na_fronteira_exata(self):
        """1000 XP: fronteira exata de subida — nível 2."""
        assert calcular_nivel(1000) == 2

    @pytest.mark.unit
    def test_nivel_2_logo_apos_virada(self):
        """1001 XP: um ponto após a virada — permanece nível 2."""
        assert calcular_nivel(1001) == 2

    @pytest.mark.unit
    def test_nivel_3_segunda_virada(self):
        """2000 XP: segunda fronteira exata — nível 3."""
        assert calcular_nivel(2000) == 3

    @pytest.mark.unit
    def test_nivel_6_com_5000_xp(self):
        """5000 XP: 5000 // 1000 + 1 = 6."""
        assert calcular_nivel(5000) == 6

    @pytest.mark.unit
    def test_nivel_10_com_9999_xp(self):
        """9999 XP: último XP antes do nível 11 → nível 10."""
        assert calcular_nivel(9999) == 10

    @pytest.mark.unit
    def test_nivel_11_com_10000_xp(self):
        """10000 XP: fronteira exata do nível 11."""
        assert calcular_nivel(10000) == 11

    @pytest.mark.unit
    def test_nivel_retorna_inteiro(self):
        """calcular_nivel deve sempre retornar um int."""
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
        (4999,  5),
        (5000,  6),
    ])
    def test_nivel_parametrizado_fronteiras(self, xp, nivel_esperado):
        """Cobertura parametrizada das fronteiras de todos os primeiros níveis."""
        assert calcular_nivel(xp) == nivel_esperado


# ===========================================================================
# 4. subiu_de_nivel — Detecção de transição
# ===========================================================================
class TestSubiuDeNivel:
    """
    Verifica que a função retorna True somente quando há cruzamento real
    de fronteira de nível, e False em todos os demais casos.
    """

    # -----------------------------------------------------------------------
    # Casos que devem retornar True (houve subida)
    # -----------------------------------------------------------------------

    @pytest.mark.unit
    def test_subiu_cruzando_1000(self):
        """900 → 1100: cruza a fronteira de 1000 XP (nível 1→2) → True."""
        assert subiu_de_nivel(900, 1100) is True

    @pytest.mark.unit
    def test_subiu_na_fronteira_exata(self):
        """999 → 1000: exatamente na fronteira → True."""
        assert subiu_de_nivel(999, 1000) is True

    @pytest.mark.unit
    def test_subiu_multiplos_niveis_de_uma_vez(self):
        """0 → 3000: salto do nível 1 direto para o nível 4 → True."""
        assert subiu_de_nivel(0, 3000) is True

    @pytest.mark.unit
    def test_subiu_em_nivel_alto(self):
        """4999 → 5000: transição de nível 5 para nível 6 → True."""
        assert subiu_de_nivel(4999, 5000) is True

    @pytest.mark.unit
    def test_subiu_de_nivel_2_para_3(self):
        """1500 → 2000: transição de nível 2 para nível 3 → True."""
        assert subiu_de_nivel(1500, 2000) is True

    # -----------------------------------------------------------------------
    # Casos que devem retornar False (sem subida)
    # -----------------------------------------------------------------------

    @pytest.mark.unit
    def test_nao_subiu_dentro_do_nivel_1(self):
        """100 → 500: permanece no nível 1 → False."""
        assert subiu_de_nivel(100, 500) is False

    @pytest.mark.unit
    def test_nao_subiu_xp_zero_sem_ganho(self):
        """0 → 0: sem ganho de XP → False."""
        assert subiu_de_nivel(0, 0) is False

    @pytest.mark.unit
    def test_nao_subiu_um_ponto_antes_da_fronteira(self):
        """998 → 999: um ponto abaixo da virada → False."""
        assert subiu_de_nivel(998, 999) is False

    @pytest.mark.unit
    def test_nao_subiu_dentro_do_mesmo_nivel_alto(self):
        """5001 → 5500: ambos no nível 6 → False."""
        assert subiu_de_nivel(5001, 5500) is False

    @pytest.mark.unit
    def test_nao_subiu_com_xp_identico(self):
        """1500 → 1500: nenhum ganho → False."""
        assert subiu_de_nivel(1500, 1500) is False

    @pytest.mark.unit
    def test_nao_subiu_com_xp_regressivo(self):
        """
        1500 → 1000: XP diminuiu (situação anormal).
        A função não deve indicar subida de nível.
        """
        assert subiu_de_nivel(1500, 1000) is False

    @pytest.mark.unit
    def test_nao_subiu_xp_alto_sem_cruzar_fronteira(self):
        """9000 → 9500: ambos no nível 10, sem cruzar 10000 → False."""
        assert subiu_de_nivel(9000, 9500) is False


# ===========================================================================
# 5. Acumulação progressiva — Cenário de sessão de jogo
# ===========================================================================
class TestAcumulacaoProgressiva:
    """
    Simula sessões de jogo completas acumulando XP resposta a resposta.
    Valida que a progressão de nível ocorre no momento correto.
    """

    @pytest.mark.unit
    def test_9_respostas_rapidas_permanece_nivel_1(self):
        """
        9 respostas rápidas × 100 XP = 900 XP.
        Jogador deve permanecer no nível 1.
        """
        xp = sum(calcular_xp(3.0) for _ in range(9))
        assert xp == 900
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_10_respostas_rapidas_sobe_para_nivel_2(self):
        """
        10 respostas rápidas × 100 XP = 1000 XP.
        Jogador deve estar exatamente no nível 2.
        """
        xp = sum(calcular_xp(3.0) for _ in range(10))
        assert xp == 1000
        assert calcular_nivel(xp) == 2

    @pytest.mark.unit
    def test_20_respostas_medias_permanece_nivel_1(self):
        """
        20 respostas médias × 50 XP = 1000 XP → nível 2.
        (Verifica que respostas médias também progridem o nível.)
        """
        xp = sum(calcular_xp(10.0) for _ in range(20))
        assert xp == 1000
        assert calcular_nivel(xp) == 2

    @pytest.mark.unit
    def test_subida_de_nivel_detectada_na_decima_resposta(self):
        """
        Simula 15 respostas rápidas e verifica que a subida de nível
        ocorre exatamente uma vez, na 10ª resposta (900 → 1000 XP).
        """
        xp = 0
        subidas = []

        for i in range(15):
            xp_ganho = calcular_xp(3.0)
            xp_novo = xp + xp_ganho
            if subiu_de_nivel(xp, xp_novo):
                subidas.append({"resposta": i + 1, "xp_antes": xp, "xp_depois": xp_novo})
            xp = xp_novo

        # Ao final: 15 × 100 = 1500 XP → nível 2
        assert xp == 1500
        assert calcular_nivel(xp) == 2

        # Subida deve ter ocorrido exatamente 1 vez
        assert len(subidas) == 1

        # Subiu na 10ª resposta (900 → 1000)
        evento = subidas[0]
        assert evento["resposta"] == 10
        assert evento["xp_antes"] == 900
        assert evento["xp_depois"] == 1000

    @pytest.mark.unit
    def test_jogo_misto_xp_e_niveis(self):
        """
        Simula jogo com respostas variadas (rápidas, médias, lentas).
        Verifica XP total acumulado e nível final corretos.

        Sequência: 5 rápidas (500), 4 médias (200), 2 lentas (50)
        Total: 750 XP → nível 1
        """
        xp = 0
        xp += sum(calcular_xp(2.0) for _ in range(5))   # 5 × 100 = 500
        xp += sum(calcular_xp(10.0) for _ in range(4))  # 4 × 50  = 200
        xp += sum(calcular_xp(20.0) for _ in range(2))  # 2 × 25  = 50

        assert xp == 750
        assert calcular_nivel(xp) == 1

    @pytest.mark.unit
    def test_pontuacao_maxima_por_sessao_de_10_questoes(self):
        """
        10 respostas rápidas é a pontuação máxima possível em 10 questões.
        Deve resultar em exatamente 1000 XP e atingir o nível 2.
        """
        xp_maximo = sum(calcular_xp(1.0) for _ in range(10))
        assert xp_maximo == 1000
        assert calcular_nivel(xp_maximo) == 2

    @pytest.mark.unit
    def test_pontuacao_minima_por_sessao_de_10_questoes(self):
        """
        10 respostas lentas é a pontuação mínima possível em 10 questões.
        Deve resultar em exatamente 250 XP e permanecer no nível 1.
        """
        xp_minimo = sum(calcular_xp(30.0) for _ in range(10))
        assert xp_minimo == 250
        assert calcular_nivel(xp_minimo) == 1
