import pytest
from app.main import calcular_faturamento

@pytest.mark.unit
def test_faturamento_plano_basico_sem_cupom():
    resultado = calcular_faturamento("BASICO")
    assert resultado == 50.0

@pytest.mark.unit
def test_faturamento_plano_pro_com_cupom_porcentagem():
    resultado = calcular_faturamento("PRO", cupom="PROMO10")
    assert resultado == 135.0

@pytest.mark.unit
def test_faturamento_com_atraso():
    resultado = calcular_faturamento("BASICO", dias_atraso=10)
    assert resultado == 60.0