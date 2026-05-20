"""
test_faker.py
=============
Suite de pruebas con Faker para datos aleatorios masivos.
Genera precios y descuentos aleatorios, verifica invariantes
matemáticos que siempre deben cumplirse.
"""

import pytest
import sys
import os
from faker import Faker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculadora_descuentos import calcular_precio_final

fake = Faker("es_MX")
Faker.seed(42)  # Semilla fija para reproducibilidad


# ─────────────────────────────────────────────────────────────────────────────
# Generación de datos aleatorios con Faker
# ─────────────────────────────────────────────────────────────────────────────
def generar_precios_validos(n=50):
    """Genera n precios aleatorios válidos (0.01 – 99999.99)."""
    return [round(fake.pyfloat(min_value=0.01, max_value=99999.99, right_digits=2), 2)
            for _ in range(n)]


def generar_descuentos_validos(n=50):
    """Genera n descuentos aleatorios válidos (0.0 – 100.0)."""
    return [round(fake.pyfloat(min_value=0.0, max_value=100.0, right_digits=2), 2)
            for _ in range(n)]


def generar_precios_invalidos(n=20):
    """Genera n precios inválidos (≤ 0)."""
    return [round(fake.pyfloat(min_value=-9999.99, max_value=0.0, right_digits=2), 2)
            for _ in range(n)]


def generar_descuentos_invalidos(n=20):
    """Genera n descuentos inválidos (fuera de [0,100])."""
    negativos = [round(fake.pyfloat(min_value=-100.0, max_value=-0.01, right_digits=2), 2)
                 for _ in range(n // 2)]
    excesivos = [round(fake.pyfloat(min_value=100.01, max_value=500.0, right_digits=2), 2)
                 for _ in range(n // 2)]
    return negativos + excesivos


PRECIOS_VALIDOS      = generar_precios_validos()
DESCUENTOS_VALIDOS   = generar_descuentos_validos()
PRECIOS_INVALIDOS    = generar_precios_invalidos()
DESCUENTOS_INVALIDOS = generar_descuentos_invalidos()


# ─────────────────────────────────────────────────────────────────────────────
# Tests con datos aleatorios válidos — Invariantes
# ─────────────────────────────────────────────────────────────────────────────
class TestFakerInvariantesValidos:
    """Verifica invariantes matemáticos con datos aleatorios válidos."""

    @pytest.mark.parametrize("precio", PRECIOS_VALIDOS[:25])
    def test_resultado_nunca_supera_original(self, precio):
        """El precio final nunca debe ser mayor que el original."""
        desc = fake.pyfloat(min_value=0.0, max_value=100.0, right_digits=2)
        desc = round(desc, 2)
        result = calcular_precio_final(precio, desc)
        assert result <= precio, (
            f"Resultado {result} supera el original {precio} con desc={desc}%"
        )

    @pytest.mark.parametrize("precio", PRECIOS_VALIDOS[:25])
    def test_resultado_nunca_negativo(self, precio):
        """El precio final nunca debe ser negativo."""
        desc = round(fake.pyfloat(min_value=0.0, max_value=100.0, right_digits=2), 2)
        result = calcular_precio_final(precio, desc)
        assert result >= 0, f"Resultado negativo: {result}"

    @pytest.mark.parametrize("desc", DESCUENTOS_VALIDOS[:25])
    def test_resultado_redondeado_dos_decimales(self, desc):
        """El resultado siempre tiene máximo 2 decimales."""
        precio = round(fake.pyfloat(min_value=0.01, max_value=9999.0, right_digits=2), 2)
        result = calcular_precio_final(precio, desc)
        assert result == round(result, 2)

    @pytest.mark.parametrize("desc", DESCUENTOS_VALIDOS[:25])
    def test_resultado_es_float(self, desc):
        """El resultado siempre es de tipo float."""
        precio = round(fake.pyfloat(min_value=0.01, max_value=5000.0, right_digits=2), 2)
        result = calcular_precio_final(precio, desc)
        assert isinstance(result, float)


# ─────────────────────────────────────────────────────────────────────────────
# Tests con datos inválidos — Excepciones
# ─────────────────────────────────────────────────────────────────────────────
class TestFakerDatosInvalidos:
    """Verifica que datos inválidos generados por Faker lancen ValueError."""

    @pytest.mark.parametrize("precio_invalido", PRECIOS_INVALIDOS)
    def test_precio_invalido_lanza_excepcion(self, precio_invalido):
        with pytest.raises(ValueError):
            calcular_precio_final(precio_invalido, 10)

    @pytest.mark.parametrize("desc_invalido", DESCUENTOS_INVALIDOS)
    def test_descuento_invalido_lanza_excepcion(self, desc_invalido):
        with pytest.raises(ValueError):
            calcular_precio_final(100, desc_invalido)


# ─────────────────────────────────────────────────────────────────────────────
# Test R5 con Faker — Verificar 5% adicional
# ─────────────────────────────────────────────────────────────────────────────
class TestFakerR5Adicional:
    """Verifica R5 con descuentos aleatorios > 80%."""

    def test_descuentos_altos_aplican_factor_095(self):
        """50 descuentos > 80 deben producir resultado × 0.95."""
        for _ in range(50):
            precio = round(fake.pyfloat(min_value=1.0, max_value=5000.0, right_digits=2), 2)
            desc   = round(fake.pyfloat(min_value=80.01, max_value=100.0, right_digits=2), 2)
            result = calcular_precio_final(precio, desc)
            esperado = round(precio * (1 - desc / 100) * 0.95, 2)
            assert result == pytest.approx(esperado, abs=0.01), (
                f"Fallo: precio={precio}, desc={desc}, result={result}, esperado={esperado}"
            )

    def test_descuentos_bajos_no_aplican_factor_095(self):
        """50 descuentos ≤ 80 NO deben aplicar el factor 0.95."""
        for _ in range(50):
            precio = round(fake.pyfloat(min_value=1.0, max_value=5000.0, right_digits=2), 2)
            desc   = round(fake.pyfloat(min_value=0.0, max_value=80.0, right_digits=2), 2)
            result = calcular_precio_final(precio, desc)
            esperado = round(precio * (1 - desc / 100), 2)
            assert result == pytest.approx(esperado, abs=0.01), (
                f"Fallo: precio={precio}, desc={desc}, result={result}, esperado={esperado}"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Test con nombres de productos ficticios (Faker locale)
# ─────────────────────────────────────────────────────────────────────────────
class TestFakerProductosFicticios:
    """Genera nombres de productos ficticios y verifica cálculos."""

    def test_productos_ficticios_invariantes(self):
        """Simula 30 productos ficticios y verifica invariantes."""
        for _ in range(30):
            nombre = fake.word().capitalize()
            precio = round(fake.pyfloat(min_value=0.50, max_value=2000.0, right_digits=2), 2)
            desc   = round(fake.pyfloat(min_value=0.0, max_value=100.0, right_digits=2), 2)
            result = calcular_precio_final(precio, desc)

            assert result >= 0, f"{nombre}: resultado negativo {result}"
            assert result <= precio, f"{nombre}: resultado {result} > original {precio}"
            assert result == round(result, 2), f"{nombre}: no redondeado {result}"
