#!/usr/bin/env python3
"""
registro_auditoria.py
=====================
Módulo de auditoría para la Calculadora de Descuentos.
Registra en 'auditoria_descuentos.txt' cada sesión y cada cálculo
con el desglose matemático completo y la verificación de requisitos.
"""

import os
from datetime import datetime

# Ruta del archivo de auditoría (mismo directorio que el script)
_DIR_BASE     = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_LOG   = os.path.join(_DIR_BASE, "auditoria_descuentos.txt")

# Contadores de sesión
_num_calculo  = 0          # Número de cálculo dentro de la sesión
_id_sesion    = ""         # Identificador único de la sesión

# ──────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN DE SESIÓN
# ──────────────────────────────────────────────────────────────────────────────
def iniciar_sesion() -> None:
    """
    Registra el inicio de una nueva sesión de ejecución en el log.
    Debe llamarse una sola vez al arrancar la aplicación.
    """
    global _num_calculo, _id_sesion

    _num_calculo = 0
    _id_sesion   = datetime.now().strftime("%Y%m%d-%H%M%S")
    ahora        = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    bloque = (
        "\n"
        "╔══════════════════════════════════════════════════════════════════╗\n"
        f"║  NUEVA SESIÓN  ▸  ID: {_id_sesion:<43}║\n"
        f"║  Inicio       ▸  {ahora:<47}║\n"
        "║  Aplicación   ▸  Calculadora de Descuentos v1.0.0              ║\n"
        "╚══════════════════════════════════════════════════════════════════╝\n"
    )

    _escribir(bloque)


def cerrar_sesion(total_calculos: int) -> None:
    """
    Registra el cierre formal de la sesión con un resumen.
    """
    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    bloque = (
        "\n"
        "┌──────────────────────────────────────────────────────────────────┐\n"
        f"│  FIN DE SESIÓN  ▸  ID: {_id_sesion:<42}│\n"
        f"│  Cierre        ▸  {ahora:<46}│\n"
        f"│  Cálculos realizados en esta sesión: {total_calculos:<29}│\n"
        "└──────────────────────────────────────────────────────────────────┘\n"
    )

    _escribir(bloque)


# ──────────────────────────────────────────────────────────────────────────────
# REGISTRO DE UN CÁLCULO COMPLETO
# ──────────────────────────────────────────────────────────────────────────────
def registrar_calculo(precio_original: float,
                      descuento: float,
                      precio_final: float) -> None:
    """
    Registra un cálculo con su desglose matemático completo y la
    verificación de cada requisito (R1-R5).

    Parámetros
    ----------
    precio_original : float  Precio ingresado por el usuario.
    descuento       : float  Porcentaje de descuento (0-100).
    precio_final    : float  Precio calculado por calcular_precio_final().
    """
    global _num_calculo
    _num_calculo += 1

    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    # ── Paso a paso matemático ───────────────────────────────────────────────
    paso1_decimal     = descuento / 100
    paso2_factor      = 1 - paso1_decimal
    paso3_descontado  = precio_original * paso2_factor
    aplica_adicional  = descuento > 80
    paso4_extra       = paso3_descontado * 0.95 if aplica_adicional else None
    ahorro            = precio_original - precio_final
    pct_efectivo      = (ahorro / precio_original) * 100 if precio_original else 0

    # ── Verificaciones de requisitos ─────────────────────────────────────────
    v_r1 = "✔ CUMPLE" if 0 <= descuento <= 100          else "✘ FALLA"
    v_r2 = "✔ CUMPLE" if precio_original > 0             else "✘ FALLA"
    v_r3 = "✔ CUMPLE" if abs(paso3_descontado -
                              precio_original * (1 - descuento / 100)) < 0.0001 else "✘ FALLA"
    v_r4 = "✔ CUMPLE" if precio_final == round(precio_final, 2) else "✘ FALLA"
    v_r5 = ("✔ CUMPLE" if (aplica_adicional and
                            abs(precio_final - round(paso3_descontado * 0.95, 2)) < 0.0001)
            else ("✔ NO APLICA" if not aplica_adicional else "✘ FALLA"))

    # ── Sección del adicional 5% ─────────────────────────────────────────────
    if aplica_adicional:
        lineas_extra = (
            "\n"
            "  ► R5 | DESCUENTO ADICIONAL DEL 5% (descuento > 80%)\n"
            f"       Precio tras descuento base       = ${paso3_descontado:>12.6f}\n"
            f"       Factor adicional                  = 0.95  (100% - 5%)\n"
            f"       ${paso3_descontado:.6f}  ×  0.95            = ${paso4_extra:>12.6f}\n"
        )
    else:
        lineas_extra = (
            "\n"
            f"  ► R5 | Descuento ≤ 80% → No se aplica el 5% adicional.\n"
        )

    bloque = (
        "\n"
        "  ┌────────────────────────────────────────────────────────────────┐\n"
        f"  │  CÁLCULO #{_num_calculo:<3}  ▸  Sesión: {_id_sesion}  │\n"
        f"  │  Fecha / Hora:  {ahora:<49}│\n"
        "  └────────────────────────────────────────────────────────────────┘\n"
        "\n"
        "  DATOS DE ENTRADA\n"
        "  ─────────────────────────────────────────────────────────────────\n"
        f"    Precio original ingresado : ${precio_original:>12.2f}\n"
        f"    Descuento ingresado       :  {descuento:>12.2f} %\n"
        "\n"
        "  DESGLOSE MATEMÁTICO PASO A PASO\n"
        "  ─────────────────────────────────────────────────────────────────\n"
        "\n"
        "  ► PASO 1 | Convertir el porcentaje a decimal\n"
        f"       {descuento} ÷ 100  =  {paso1_decimal:.10f}\n"
        "\n"
        "  ► PASO 2 | Calcular el factor de precio (proporción que se PAGA)\n"
        f"       1  -  {paso1_decimal:.10f}  =  {paso2_factor:.10f}\n"
        "\n"
        "  ► PASO 3 | Aplicar el factor al precio original (R3)\n"
        f"       ${precio_original:.2f}  ×  {paso2_factor:.10f}  =  ${paso3_descontado:.6f}\n"
        f"{lineas_extra}"
        "\n"
        "  ► PASO FINAL | Redondear a 2 decimales (R4)\n"
        f"       round({paso4_extra if aplica_adicional else paso3_descontado:.6f}, 2)  =  ${precio_final:.2f}\n"
        "\n"
        "  RESULTADO FINAL\n"
        "  ─────────────────────────────────────────────────────────────────\n"
        f"    Precio original           : ${precio_original:>12.2f}\n"
        f"    Precio final              : ${precio_final:>12.2f}\n"
        f"    Ahorro total              : ${ahorro:>12.2f}\n"
        f"    Descuento efectivo real   :  {pct_efectivo:>12.4f} %\n"
        "\n"
        "  VERIFICACIÓN DE REQUISITOS\n"
        "  ─────────────────────────────────────────────────────────────────\n"
        f"    R1 — Descuento en rango [0, 100]                : {v_r1}\n"
        f"    R2 — Precio original positivo                   : {v_r2}\n"
        f"    R3 — Fórmula precio × (1 − desc/100)            : {v_r3}\n"
        f"    R4 — Resultado redondeado a 2 decimales         : {v_r4}\n"
        f"    R5 — Descuento adicional 5% si desc > 80%       : {v_r5}\n"
        "\n"
    )

    _escribir(bloque)


# ──────────────────────────────────────────────────────────────────────────────
# REGISTRO DE ERRORES / ENTRADAS INVÁLIDAS
# ──────────────────────────────────────────────────────────────────────────────
def registrar_calculo_multiple(productos: list) -> None:
    """
    Registra un cálculo múltiple con desglose por producto y totales.

    Parámetros
    ----------
    productos : list of tuple  (nombre, precio_original, descuento, precio_final)
    """
    global _num_calculo
    _num_calculo += 1

    ahora        = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    n            = len(productos)
    total_orig   = sum(p[1] for p in productos)
    total_final  = sum(p[3] for p in productos)
    total_ahorro = total_orig - total_final
    pct_total    = (total_ahorro / total_orig * 100) if total_orig else 0

    encabezado = (
        "\n"
        "  ┌────────────────────────────────────────────────────────────────┐\n"
        f"  │  CÁLCULO #{_num_calculo:<3} [MÚLTIPLE — {n} productos]"
        f"  Sesión: {_id_sesion}  │\n"
        f"  │  Fecha / Hora:  {ahora:<49}│\n"
        "  └────────────────────────────────────────────────────────────────┘\n\n"
    )

    items_lines = ""
    for idx, (nombre, precio, descuento, precio_final) in enumerate(productos, 1):
        paso1      = descuento / 100
        paso2      = 1 - paso1
        paso3      = precio * paso2
        aplica     = descuento > 80
        paso4      = paso3 * 0.95 if aplica else None
        ahorro     = precio - precio_final
        pct        = (ahorro / precio * 100) if precio else 0

        v_r1 = "✔" if 0 <= descuento <= 100 else "✘"
        v_r2 = "✔" if precio > 0             else "✘"
        v_r3 = "✔" if abs(paso3 - precio * (1 - descuento / 100)) < 0.0001 else "✘"
        v_r4 = "✔" if precio_final == round(precio_final, 2) else "✘"
        v_r5 = ("✔" if (aplica and abs(precio_final - round(paso3 * 0.95, 2)) < 0.0001)
                else ("N/A" if not aplica else "✘"))

        extra = (
            f"\n       ► R5 (desc>80%): ${paso3:.6f} × 0.95 = ${paso4:.6f}\n"
            if aplica else
            "\n       ► R5: descuento ≤ 80%, sin descuento adicional.\n"
        )

        items_lines += (
            f"  ── ÍTEM #{idx}: {nombre}\n"
            f"     Precio orig.: ${precio:.2f}  |  Descuento: {descuento:.2f}%\n"
            f"     Paso 1: {descuento} ÷ 100 = {paso1:.10f}\n"
            f"     Paso 2: 1 − {paso1:.10f} = {paso2:.10f}\n"
            f"     Paso 3: ${precio:.2f} × {paso2:.10f} = ${paso3:.6f}"
            f"{extra}"
            f"     Paso final: round({paso4 if aplica else paso3:.6f}, 2) = ${precio_final:.2f}\n"
            f"     Ahorro: ${ahorro:.2f}  |  Desc. efectivo: {pct:.4f}%\n"
            f"     Verificación → R1:{v_r1}  R2:{v_r2}  R3:{v_r3}  R4:{v_r4}  R5:{v_r5}\n\n"
        )

    consolidado = (
        "  CONSOLIDADO GENERAL\n"
        "  ─────────────────────────────────────────────────────────────────\n"
        f"    Productos procesados         : {n}\n"
        f"    Total precio original        : ${total_orig:>12.2f}\n"
        f"    Total precio final           : ${total_final:>12.2f}\n"
        f"    Ahorro total                 : ${total_ahorro:>12.2f}\n"
        f"    Descuento efectivo global    :  {pct_total:>12.4f} %\n\n"
    )

    _escribir(encabezado + items_lines + consolidado)


def registrar_error(mensaje: str, precio_raw: str = "", descuento_raw: str = "") -> None:
    """
    Registra un intento de cálculo que resultó en error de validación.
    """
    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

    bloque = (
        "\n"
        f"  [ERROR] {ahora}  |  Sesión: {_id_sesion}\n"
        f"    Entrada precio   : {precio_raw!r}\n"
        f"    Entrada descuento: {descuento_raw!r}\n"
        f"    Motivo           : {mensaje}\n"
    )

    _escribir(bloque)


# ──────────────────────────────────────────────────────────────────────────────
# UTILIDAD INTERNA DE ESCRITURA
# ──────────────────────────────────────────────────────────────────────────────
def _escribir(texto: str) -> None:
    """Agrega `texto` al archivo de auditoría en modo append (UTF-8)."""
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(texto)
