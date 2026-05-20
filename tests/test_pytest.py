"""
test_pytest.py
==============
Suite de pruebas con PyTest puro.
Cubre los requisitos R1-R5 de calcular_precio_final mediante:
  - Tests parametrizados
  - Tests de excepciones
  - Tests de casos límite (boundary)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculadora_descuentos import calcular_precio_final


# ─────────────────────────────────────────────────────────────────────────────
# R2 — Precio original debe ser positivo
# ─────────────────────────────────────────────────────────────────────────────
class TestR2PrecioPositivo:
    """Grupo: precio_original debe ser > 0 (Requisito R2)."""

    @pytest.mark.parametrize("precio_invalido", [0, -1, -100, -0.01, -999.99])
    def test_precio_no_positivo_lanza_valueerror(self, precio_invalido):
        """Precios ≤ 0 deben lanzar ValueError."""
        with pytest.raises(ValueError, match="positivo"):
            calcular_precio_final(precio_invalido, 10)

    @pytest.mark.parametrize("precio_valido", [0.01, 1, 50, 100, 99999.99])
    def test_precio_positivo_no_lanza_excepcion(self, precio_valido):
        """Precios > 0 no deben lanzar excepción."""
        result = calcular_precio_final(precio_valido, 0)
        assert result >= 0


# ─────────────────────────────────────────────────────────────────────────────
# R1 — Descuento debe estar en [0, 100]
# ─────────────────────────────────────────────────────────────────────────────
class TestR1RangoDescuento:
    """Grupo: descuento en rango [0, 100] (Requisito R1)."""

    @pytest.mark.parametrize("desc_invalido", [-1, -0.01, 100.01, 101, 200])
    def test_descuento_fuera_de_rango_lanza_valueerror(self, desc_invalido):
        """Descuentos fuera de [0,100] deben lanzar ValueError."""
        with pytest.raises(ValueError, match="[Dd]escuento"):
            calcular_precio_final(100, desc_invalido)

    @pytest.mark.parametrize("desc_valido", [0, 0.01, 50, 99.99, 100])
    def test_descuento_en_rango_no_lanza_excepcion(self, desc_valido):
        """Descuentos en [0,100] no deben lanzar excepción."""
        result = calcular_precio_final(100, desc_valido)
        assert isinstance(result, float)


# ─────────────────────────────────────────────────────────────────────────────
# R3 — Fórmula: precio × (1 − descuento/100)
# ─────────────────────────────────────────────────────────────────────────────
class TestR3Formula:
    """Grupo: cálculo básico correcto (Requisito R3)."""

    @pytest.mark.parametrize("precio, desc, esperado", [
        (200.00, 50.0,  100.00),
        (100.00, 10.0,   90.00),
        (99.99,   0.0,   99.99),
        (500.00, 20.0,  400.00),
        (1000.0, 75.0,  250.00),
    ])
    def test_formula_basica(self, precio, desc, esperado):
        """Verifica precio × (1 − desc/100) cuando desc ≤ 80."""
        assert calcular_precio_final(precio, desc) == pytest.approx(esperado, abs=0.01)

    def test_descuento_cero_devuelve_precio_original(self):
        """Con descuento 0 el precio no cambia."""
        assert calcular_precio_final(150.75, 0) == 150.75

    def test_descuento_100_devuelve_cero(self):
        """Con descuento 100 el precio es 0."""
        assert calcular_precio_final(999.99, 100) == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# R4 — Resultado redondeado a 2 decimales
# ─────────────────────────────────────────────────────────────────────────────
class TestR4Redondeo:
    """Grupo: resultado redondeado a 2 decimales (Requisito R4)."""

    @pytest.mark.parametrize("precio, desc", [
        (100.0, 33.0),
        (99.99, 15.0),
        (333.33, 10.0),
        (7.77, 7.0),
    ])
    def test_resultado_tiene_maximo_dos_decimales(self, precio, desc):
        """El resultado no debe tener más de 2 decimales."""
        result = calcular_precio_final(precio, desc)
        assert result == round(result, 2)

    def test_resultado_es_float(self):
        """El resultado debe ser de tipo float."""
        result = calcular_precio_final(100, 10)
        assert isinstance(result, float)


# ─────────────────────────────────────────────────────────────────────────────
# R5 — Descuento adicional del 5% si descuento > 80%
# ─────────────────────────────────────────────────────────────────────────────
class TestR5DescuentoAdicional:
    """Grupo: descuento extra 5% cuando desc > 80% (Requisito R5)."""

    @pytest.mark.parametrize("precio, desc, esperado", [
        (200.00, 85.0,  28.50),   # 200×0.15×0.95
        (100.00, 81.0,  18.05),   # 100×0.19×0.95
        (500.00, 90.0,  47.50),   # 500×0.10×0.95
        (1000.0, 99.0,   9.50),   # 1000×0.01×0.95
    ])
    def test_descuento_mayor_80_aplica_extra(self, precio, desc, esperado):
        """Cuando desc > 80 se aplica un 5% adicional sobre el descontado."""
        assert calcular_precio_final(precio, desc) == pytest.approx(esperado, abs=0.01)

    @pytest.mark.parametrize("desc_limite", [79.0, 79.99, 80.0])
    def test_descuento_80_o_menor_no_aplica_extra(self, desc_limite):
        """Con desc ≤ 80 NO se aplica el 5% adicional."""
        precio = 100.0
        sin_extra = round(precio * (1 - desc_limite / 100), 2)
        assert calcular_precio_final(precio, desc_limite) == sin_extra

    def test_limite_exacto_80_no_activa_extra(self):
        """El límite exacto (80%) NO activa el descuento adicional."""
        result = calcular_precio_final(100.0, 80.0)
        assert result == 20.0   # 100 × 0.20, sin factor 0.95

    def test_limite_81_si_activa_extra(self):
        """81% SÍ activa el descuento adicional."""
        result = calcular_precio_final(100.0, 81.0)
        assert result == pytest.approx(100 * 0.19 * 0.95, abs=0.01)


# ─────────────────────────────────────────────────────────────────────────────
# Casos de frontera / edge cases
# ─────────────────────────────────────────────────────────────────────────────
class TestEdgeCases:
    """Casos extremos y de frontera."""

    def test_precio_minimo_valido(self):
        """El precio mínimo válido (0.01) no lanza excepción."""
        assert calcular_precio_final(0.01, 0) == 0.01

    def test_precio_muy_grande(self):
        """Precios muy grandes se calculan correctamente."""
        result = calcular_precio_final(1_000_000.00, 50.0)
        assert result == 500_000.00

    def test_descuento_exactamente_100(self):
        """Descuento de exactamente 100% devuelve 0."""
        assert calcular_precio_final(500.0, 100.0) == 0.0

    def test_mensaje_error_precio_contiene_valor(self):
        """El mensaje de error para precio inválido menciona el valor."""
        with pytest.raises(ValueError) as exc_info:
            calcular_precio_final(-5, 10)
        assert "-5" in str(exc_info.value)

    def test_mensaje_error_descuento_contiene_valor(self):
        """El mensaje de error para descuento inválido menciona el valor."""
        with pytest.raises(ValueError) as exc_info:
            calcular_precio_final(100, 150)
        assert "150" in str(exc_info.value)
