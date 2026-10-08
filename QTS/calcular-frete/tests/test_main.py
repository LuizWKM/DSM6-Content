import pytest
from app.main import calcular_frete

@pytest.mark.unit
def test_frete_peso_invalido_zero_ou_negativo():
    with pytest.raises(ValueError, match="O Peso deve ser maior que zero."):
        calcular_frete(peso=0.0, uf="SP")

    with pytest.raises(ValueError, match="O Peso deve ser maior que zero."):
        calcular_frete(peso=-5.0, uf="SP")

@pytest.mark.unit
def test_frete_excede_limite_maximo():
    assert calcular_frete(peso=30.0, uf="SP") == 50.0

    with pytest.raises(ValueError, match="O peso excede o limite máximo permitido de 30kg."):
            calcular_frete(peso=30.01, uf="SP")

@pytest.mark.unit
def test_frete_uf_invalida():
    with pytest.raises(ValueError, match="UF invalida."):
        calcular_frete(peso=5.0, uf="XX")

    with pytest.raises(ValueError, match="UF invalida."):
        calcular_frete(peso=5.0, uf="xY")

    with pytest.raises(ValueError, match="UF invalida."):
        calcular_frete(peso=5.0, uf="xx")

    with pytest.raises(ValueError, match="UF invalida."):
        calcular_frete(peso=5.0, uf="Yx")

@pytest.mark.unit
def test_frete_normalizacao_uf():
    assert calcular_frete(peso=5.0, uf="   sp    ") == 20.0

    assert calcular_frete(peso=5.0, uf="am") == 35.0

@pytest.mark.parametrize("peso, uf, esperado", [
    (0.01, "SP", 20.0),
    (10.0, "SP", 20.0),
    (10.01, "SP", 50.0),
    (30.0, "SP", 50.0),
    (5.0, "AM", 35.0),
    (15.0, "AM", 65.0),
    (5.0, "RJ", 20.0),
])
@pytest.mark.unit
def test_frete_calculos_validos_parametrizados(peso, uf, esperado):
    assert calcular_frete(peso=peso, uf=uf) == esperado