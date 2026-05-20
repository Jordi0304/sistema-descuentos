"""
steps_descuentos.py
===================
Implementación de los steps de BDD (pytest-bdd)
para los escenarios definidos en descuentos.feature.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from calculadora_descuentos import calcular_precio_final

# Cargar todos los escenarios del archivo .feature
scenarios(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "features", "descuentos.feature"))


# ─── Fixture compartida para datos del escenario ────────────────────────────
@pytest.fixture
def contexto():
    return {}


# ─── GIVEN ──────────────────────────────────────────────────────────────────
@given(
    parsers.parse("que el precio original es {precio:g}"),
    target_fixture="contexto",
)
def dado_precio_original(precio):
    return {"precio": precio}


@given(parsers.parse("el descuento es {descuento:g} por ciento"))
def dado_descuento(contexto, descuento):
    contexto["descuento"] = descuento


# ─── WHEN ───────────────────────────────────────────────────────────────────
@when("calculo el precio final")
def cuando_calculo(contexto):
    contexto["resultado"] = calcular_precio_final(
        contexto["precio"], contexto["descuento"]
    )


@when("calculo el precio final debe fallar")
def cuando_calculo_falla(contexto):
    try:
        calcular_precio_final(contexto["precio"], contexto["descuento"])
        contexto["error"] = None
    except ValueError as e:
        contexto["error"] = e


# ─── THEN ───────────────────────────────────────────────────────────────────
@then(parsers.parse("el precio final debe ser {esperado:g}"))
def entonces_precio_final(contexto, esperado):
    assert abs(contexto["resultado"] - esperado) < 0.01, (
        f"Esperado {esperado}, obtenido {contexto['resultado']}"
    )


@then("se debe lanzar un error de valor")
def entonces_error_valor(contexto):
    assert contexto["error"] is not None, "Se esperaba ValueError pero no ocurrió"
    assert isinstance(contexto["error"], ValueError)
