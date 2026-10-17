import pytest
from main import(
    calcular_matching_ineficiente,
    calcular_matching_otimizado,
    VOLUNTARIOS,
    DEMANDAS
)

def ordenar_matches(matches: list[dict]) -> list[tuple[int, int, int]]:
    """ Ordena a saída por voluntario_id e demanda_id para comparação exata """
    return sorted(
        (m["voluntario_id"], m["demanda_id"], m["score"])
        for m in matches
    )

def test_equivalencia_com_massa_completa():
    resultado_original = calcular_matching_ineficiente(VOLUNTARIOS, DEMANDAS)
    resultado_otimizado = calcular_matching_otimizado(VOLUNTARIOS, DEMANDAS)

    assert len(resultado_original) > 0, "A massa de testes deve gerar correspondência válidas"
    assert len(resultado_original) == len(resultado_otimizado)
    assert ordenar_matches(resultado_original) == ordenar_matches(resultado_otimizado)

def test_equivalencia_casos_vazios():
    assert calcular_matching_otimizado([], []) == []
    assert calcular_matching_otimizado(VOLUNTARIOS[:5], []) == []
    assert calcular_matching_otimizado([], DEMANDAS[:5]) == []

def test_equivalencia_sem_matches_de_cidade():
    voluntarios = [{"id": 1, "cidade": "Santos", "habilidades": ["cozinha"]}]
    demandas = [{"id": 101, "cidade": "Campinas", "habilidades_requeridas": ["cozinha"]}]

    assert calcular_matching_ineficiente(voluntarios, demandas) == []
    assert calcular_matching_otimizado(voluntarios, demandas) == []