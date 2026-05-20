"""
test_unittest.py
================
Suite de pruebas con unittest.TestCase.
Estructura clásica con setUp/tearDown y métodos agrupados por requisito.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculadora_descuentos import calcular_precio_final


class TestR1DescuentoRango(unittest.TestCase):
    """R1 — Descuento debe estar en [0, 100]."""

    def test_descuento_negativo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(100, -1)

    def test_descuento_mayor_100_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(100, 101)

    def test_descuento_cero_es_valido(self):
        result = calcular_precio_final(100, 0)
        self.assertEqual(result, 100.0)

    def test_descuento_100_es_valido(self):
        result = calcular_precio_final(100, 100)
        self.assertEqual(result, 0.0)

    def test_descuento_50_es_valido(self):
        result = calcular_precio_final(200, 50)
        self.assertEqual(result, 100.0)


class TestR2PrecioPositivo(unittest.TestCase):
    """R2 — Precio original debe ser > 0."""

    def test_precio_cero_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(0, 10)

    def test_precio_negativo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            calcular_precio_final(-50, 10)

    def test_precio_minimo_valido(self):
        result = calcular_precio_final(0.01, 0)
        self.assertEqual(result, 0.01)

    def test_precio_grande(self):
        result = calcular_precio_final(10000, 10)
        self.assertEqual(result, 9000.0)


class TestR3FormulaBasica(unittest.TestCase):
    """R3 — Fórmula precio × (1 − descuento/100)."""

    def setUp(self):
        """Prepara datos de prueba reutilizables."""
        self.casos = [
            (200.00, 50.0, 100.00),
            (100.00, 10.0,  90.00),
            (300.00, 25.0, 225.00),
            (  1.00,  1.0,   0.99),
        ]

    def test_formula_correcta_multiples_casos(self):
        for precio, desc, esperado in self.casos:
            with self.subTest(precio=precio, desc=desc):
                self.assertAlmostEqual(
                    calcular_precio_final(precio, desc), esperado, places=2
                )

    def test_sin_descuento_devuelve_original(self):
        self.assertEqual(calcular_precio_final(250.50, 0), 250.50)

    def test_descuento_total_devuelve_cero(self):
        self.assertEqual(calcular_precio_final(500, 100), 0.0)


class TestR4Redondeo(unittest.TestCase):
    """R4 — Resultado redondeado a 2 decimales."""

    def test_resultado_redondeado(self):
        result = calcular_precio_final(100.0, 33.0)
        self.assertEqual(result, round(result, 2))

    def test_resultado_es_float(self):
        result = calcular_precio_final(100, 10)
        self.assertIsInstance(result, float)

    def test_multiples_redondeos(self):
        pares = [(99.99, 15.0), (333.33, 10.0), (7.77, 7.0), (123.456, 33.33)]
        for precio, desc in pares:
            with self.subTest(precio=precio, desc=desc):
                r = calcular_precio_final(precio, desc)
                self.assertEqual(r, round(r, 2))


class TestR5DescuentoAdicional(unittest.TestCase):
    """R5 — 5% adicional cuando descuento > 80%."""

    def test_descuento_85_aplica_extra(self):
        result = calcular_precio_final(200.0, 85.0)
        esperado = round(200.0 * 0.15 * 0.95, 2)
        self.assertAlmostEqual(result, esperado, places=2)

    def test_descuento_80_no_aplica_extra(self):
        result = calcular_precio_final(100.0, 80.0)
        self.assertEqual(result, 20.0)

    def test_descuento_81_aplica_extra(self):
        result = calcular_precio_final(100.0, 81.0)
        esperado = round(100.0 * 0.19 * 0.95, 2)
        self.assertAlmostEqual(result, esperado, places=2)

    def test_descuento_99_aplica_extra(self):
        result = calcular_precio_final(1000.0, 99.0)
        esperado = round(1000.0 * 0.01 * 0.95, 2)
        self.assertAlmostEqual(result, esperado, places=2)

    def test_resultado_nunca_negativo(self):
        result = calcular_precio_final(100.0, 100.0)
        self.assertGreaterEqual(result, 0)


class TestMensajesError(unittest.TestCase):
    """Verifica que los mensajes de error sean descriptivos."""

    def test_error_precio_menciona_valor(self):
        with self.assertRaises(ValueError) as ctx:
            calcular_precio_final(-10, 10)
        self.assertIn("-10", str(ctx.exception))

    def test_error_descuento_menciona_valor(self):
        with self.assertRaises(ValueError) as ctx:
            calcular_precio_final(100, 150)
        self.assertIn("150", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
