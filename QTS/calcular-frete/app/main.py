import string
from functools import lru_cache
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Calculadora de Frete Simplificada")

NORTE_UFS = {"AM", "RR", "AP", "PA", "AC", "RO", "TO"}

VALID_UFS = NORTE_UFS.union({
    "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE",
    "DF", "GO", "MT", "MS", "ES", "MG", "RJ", "SP", "PR",
    "RS", "SC"
})

class FreteRequest(BaseModel):
    peso: float
    uf: str

def calcular_frete(peso: float, uf: str) -> float:
    if peso < 0.1:
        raise ValueError("O peso minimo do produto e 0.1kg.")
    if peso > 30:
        raise ValueError("O peso excede o limite máximo permitido de 30kg.")

    uf_upper = uf.strip().upper()

    if len(uf_upper) != 2 or not uf_upper.isalpha():
        raise ValueError("UF deve conter exatamente 2 caracteres alfabéticos.")

    if not all(char in string.ascii_uppercase for char in uf_upper):
        raise ValueError("UF deve conter apenas letras sem acentuação.")

    if uf_upper not in VALID_UFS:
        raise ValueError("UF invalida.")

    if peso <= 10.0:
        valor_base = 20.0
    else:
        valor_base = 50.0

    adicional = 15.0 if uf_upper in NORTE_UFS else 0.0

    return valor_base + adicional

@app.post("/frete")
def post_calcular_frete(payload: FreteRequest):
    try:
        valor = calcular_frete(peso=payload.peso, uf=payload.uf)

        return {
            "peso": payload.peso,
            "uf": payload.uf.strip().upper(),
            "valor_frete": valor
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )