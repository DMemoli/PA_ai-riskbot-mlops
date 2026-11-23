"""Tests locales sin consumo de Gemini; no sustituyen evaluación semántica."""
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from main import InferenceRequest, app

RAIZ = Path(__file__).resolve().parents[1]


def test_salud():
    respuesta = TestClient(app).get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "ok"


def test_rechazo_de_caracteres_no_permitidos():
    respuesta = TestClient(app).post("/inferencia", json={"prompt": "<script>alert(1)</script>"})
    assert respuesta.status_code == 400


def test_rechazo_de_modelo_no_permitido():
    respuesta = TestClient(app).post(
        "/inferencia", json={"prompt": "Interes Tier B", "model": "modelo-inventado"}
    )
    assert respuesta.status_code == 400


def test_cuarenta_casos_respetan_contrato():
    for archivo in ("eval_security.json", "eval_functional.json"):
        datos = json.loads((RAIZ / "eval_data" / archivo).read_text(encoding="utf-8"))
        assert len(datos) >= 20
        for caso in datos:
            InferenceRequest(prompt=caso["prompt"])


def test_politicas_contienen_los_valores_clave():
    datos = json.loads((RAIZ / "politicas_credito.json").read_text(encoding="utf-8"))
    politica = datos["politicas_credito"]
    assert politica["requisitos_hipoteca"]["edad_minima"] == 25
    assert politica["tasas_interes_anual"]["tier_B_estandar"] == 7.5
    assert politica["limites_sin_aval"]["prestamo_personal"] == 20000
