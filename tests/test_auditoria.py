"""
test_auditoria.py
=================
Pruebas del módulo registro_auditoria.py
Usa directorio temporal para no contaminar el log real.
"""

import pytest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import registro_auditoria as auditoria


@pytest.fixture(autouse=True)
def log_temporal(tmp_path):
    """Redirige el archivo de auditoría a un directorio temporal."""
    original = auditoria.ARCHIVO_LOG
    auditoria.ARCHIVO_LOG = str(tmp_path / "auditoria_test.txt")
    yield tmp_path / "auditoria_test.txt"
    auditoria.ARCHIVO_LOG = original


class TestInicioSesion:
    """Verifica que iniciar_sesion crea el archivo y escribe encabezado."""

    def test_archivo_se_crea(self, log_temporal):
        auditoria.iniciar_sesion()
        assert log_temporal.exists()

    def test_encabezado_contiene_nueva_sesion(self, log_temporal):
        auditoria.iniciar_sesion()
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "NUEVA SESIÓN" in contenido

    def test_encabezado_contiene_id_sesion(self, log_temporal):
        auditoria.iniciar_sesion()
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "ID:" in contenido


class TestRegistroCalculo:
    """Verifica que registrar_calculo escribe el desglose completo."""

    def test_calculo_simple_se_registra(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(200.0, 50.0, 100.0)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "CÁLCULO #" in contenido

    def test_datos_entrada_presentes(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(150.0, 20.0, 120.0)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "150.00" in contenido
        assert "20.00" in contenido

    def test_desglose_matematico_presente(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(200.0, 50.0, 100.0)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "PASO 1" in contenido
        assert "PASO 2" in contenido
        assert "PASO 3" in contenido

    def test_verificacion_requisitos_presente(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(200.0, 50.0, 100.0)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "R1" in contenido
        assert "R2" in contenido
        assert "R3" in contenido
        assert "R4" in contenido
        assert "R5" in contenido

    def test_descuento_mayor_80_muestra_adicional(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(200.0, 85.0, 28.50)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "DESCUENTO ADICIONAL" in contenido

    def test_descuento_menor_80_no_muestra_adicional(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_calculo(200.0, 50.0, 100.0)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "DESCUENTO ADICIONAL" not in contenido


class TestRegistroError:
    """Verifica que registrar_error escribe la entrada inválida."""

    def test_error_se_registra(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_error("Precio no positivo", precio_raw="-50")
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "[ERROR]" in contenido

    def test_error_contiene_motivo(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.registrar_error("Descuento no numérico", descuento_raw="abc")
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "Descuento no numérico" in contenido
        assert "abc" in contenido


class TestCierreSesion:
    """Verifica que cerrar_sesion escribe el resumen."""

    def test_cierre_presente(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.cerrar_sesion(3)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "FIN DE SESIÓN" in contenido

    def test_cierre_contiene_total(self, log_temporal):
        auditoria.iniciar_sesion()
        auditoria.cerrar_sesion(5)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "5" in contenido


class TestCalculoMultiple:
    """Verifica que registrar_calculo_multiple escribe correctamente."""

    def test_multiple_se_registra(self, log_temporal):
        auditoria.iniciar_sesion()
        productos = [
            ("Laptop", 1000.0, 20.0, 800.0),
            ("Mouse", 50.0, 10.0, 45.0),
        ]
        auditoria.registrar_calculo_multiple(productos)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "MÚLTIPLE" in contenido

    def test_consolidado_presente(self, log_temporal):
        auditoria.iniciar_sesion()
        productos = [
            ("A", 100.0, 10.0, 90.0),
            ("B", 200.0, 20.0, 160.0),
        ]
        auditoria.registrar_calculo_multiple(productos)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "CONSOLIDADO" in contenido

    def test_cada_item_presente(self, log_temporal):
        auditoria.iniciar_sesion()
        productos = [
            ("Teclado", 80.0, 15.0, 68.0),
            ("Monitor", 400.0, 25.0, 300.0),
        ]
        auditoria.registrar_calculo_multiple(productos)
        contenido = log_temporal.read_text(encoding="utf-8")
        assert "Teclado" in contenido
        assert "Monitor" in contenido
