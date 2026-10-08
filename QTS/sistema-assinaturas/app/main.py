# app/main.py
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Motor de Faturamento de Assinaturas")

VALORES_PLANOS = {
    "BASICO": 50.0,
    "PRO": 150.0,
    "ENTERPRISE": 500.0
}

CUPONS_VALIDOS = {
    "PROMO10": ("PORCENTAGEM", 10.0),
    "DESCONTO20": ("PORCENTAGEM", 20.0),
    "BEMVINDO50": ("FIXO", 50.0),
    "CREDITO100": ("FIXO", 100.0)
}

class RequisicaoFatura(BaseModel):
    plano: str
    cupom: Optional[str] = None
    dias_atraso: int = 0

class RespostaFatura(BaseModel):
    plano:str
    valor_base: float
    valor_com_desconto: float
    valor_multa_juros: float
    valor_final: float

def calcular_faturamento(plano: str, cupom: Optional[str] = None, dias_atraso: int = 0) -> float:
    if not isinstance(plano, str) or not plano.strip():
        raise ValueError("O plano informado nao pode ser vazio ou nulo.")

    plano_normalizado = plano.strip().upper()
    if plano_normalizado not in VALORES_PLANOS:
        raise ValueError(f"Plano invalido: {plano}. Planos disponiveis: {list(VALORES_PLANOS.keys)}")

    if not isinstance(dias_atraso, int) or dias_atraso < 0:
        raise ValueError("Dias de atraso nao podem ser negativos.")

    

    valor_base = VALORES_PLANOS[plano_normalizado]
    valor_com_desconto = valor_base

    if cupom is not None and isinstance(cupom, str):
        cupom_normalizado = cupom.strip().upper()
        if cupom_normalizado != "":
            if cupom_normalizado not in CUPONS_VALIDOS:
                raise ValueError(f"Cupom invalido ou inexistente: {cupom}.")

            tipo, taxa = CUPONS_VALIDOS[cupom_normalizado]
            if tipo == "PORCENTAGEM":
                valor_com_desconto = valor_base - (valor_base * (taxa / 100))
            elif tipo == "FIXO":
                valor_com_desconto = valor_base - taxa

    if valor_com_desconto < 0.0:
        valor_com_desconto = 0.0

    if dias_atraso > 0:
        multa = 5.0
        juros = valor_com_desconto * (0.01 * dias_atraso)
        valor_final = valor_com_desconto + multa + juros
    else:
        valor_final = valor_com_desconto

    return round(valor_final, 2)