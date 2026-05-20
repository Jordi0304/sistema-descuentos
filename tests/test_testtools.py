"""
test_testtools.py
=================
Suite de pruebas con testtools (matchers avanzados).
Usa testtools.TestCase con ExpectedException y MatchesStructure.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import testtools
from testtools.matchers import (
    Equals,
    GreaterThan,
    LessThan,
    IsInstance,
    MatchesAll,
    MatchesAny,
    Not,
)
from calculadora_descuentos import calcular_precio_final


class TestR2PrecioPositivoTesttools(testtools.TestCase):
    """R2 — Precio positivo con matchers de testtools."""

    def test_precio_negativo_lanza_valueerror(self):
        self.assertRaises(ValueError, calcular_precio_final, -1, 10)

    def test_precio_cero_lanza_valueerror(self):
        self.assertRaises(ValueError, calcular_precio_final, 0, 10)

    def test_precio_valido_retorna_float(self):
        result = calcular_precio_final(100, 10)
        self.assertThat(result, IsInstance(float))


class TestR1RangoDescuentoTesttools(testtools.TestCase):
    """R1 — Descuento en [0,100] con matchers."""

    def test_descuento_negativo_lanza_excepcion(self):
        self.assertRaises(ValueError, calcular_precio_final, 100, -5)

    def test_descuento_mayor_100_lanza_excepcion(self):
        self.assertRaises(ValueError, calcular_precio_final, 100, 200)

    def test_descuento_valido_retorna_positivo_o_cero(self):
        result = calcular_precio_final(100, 50)
        self.assertThat(result, MatchesAny(Equals(0.0), GreaterThan(0)))


class TestR3FormulaTesttools(testtools.TestCase):
    """R3 — Fórmula básica con matchers avanzados."""

    def test_formula_200_50(self):
        result = calcular_precio_final(200, 50)
        self.assertThat(result, Equals(100.0))

    def test_sin_descuento_igual_a_original(self):
        result = calcular_precio_final(99.99, 0)
        self.assertThat(result, Equals(99.99))

    def test_resultado_nunca_mayor_que_original(self):
        precio = 500.0
        result = calcular_precio_final(precio, 30)
        self.assertThat(result, MatchesAll(
            GreaterThan(-0.01),
            Not(GreaterThan(precio)),
        ))


class TestR5AdicionalTesttools(testtools.TestCase):
    """R5 — Descuento adicional con matchers."""

    def test_descuento_85_menor_que_sin_adicional(self):
        """Con desc > 80, el precio final debe ser menor que sin el 5% extra."""
        precio = 200.0
        desc = 85.0
        sin_extra = round(precio * (1 - desc / 100), 2)
        con_extra = calcular_precio_final(precio, desc)
        self.assertThat(con_extra, LessThan(sin_extra))

    def test_descuento_80_igual_a_formula_simple(self):
        """Con desc = 80 exacto, NO se aplica extra."""
        result = calcular_precio_final(100, 80)
        self.assertThat(result, Equals(20.0))

    def test_descuento_81_es_float(self):
        result = calcular_precio_final(100, 81)
        self.assertThat(result, IsInstance(float))

    def test_resultado_siempre_no_negativo(self):
        result = calcular_precio_final(100, 100)
        self.assertThat(result, MatchesAny(Equals(0.0), GreaterThan(0)))


class TestR4RedondeoTesttools(testtools.TestCase):
    """R4 — Redondeo a 2 decimales con testtools."""

    def test_redondeo_33_porciento(self):
        result = calcular_precio_final(100, 33)
        self.assertThat(result, Equals(round(result, 2)))

    def test_tipo_resultado(self):
        result = calcular_precio_final(77.77, 13)
        self.assertThat(result, IsInstance(float))
