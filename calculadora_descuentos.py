#!/usr/bin/env python3
"""
Calculadora de Descuentos - Aplicación de Consola Profesional
=============================================================
Implementa la función `calcular_precio_final` siguiendo los requisitos R1-R5.
Ofrece una interfaz interactiva, moderna y robusta mediante menús, colores ANSI
y validaciones exhaustivas.

Autor: Práctica de Aula
Versión: 1.0.0
"""

import sys
import time
from typing import Tuple
import registro_auditoria as auditoria

# Contador global de cálculos (usado para el resumen de sesión)
_num_calculos: int = 0

# ------------------------------------------------------------------------------
# CÓDIGOS DE COLOR ANSI (compatibles con la mayoría de terminales modernas)
# ------------------------------------------------------------------------------
class Color:
    """Define códigos de escape ANSI para texto y fondo."""
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    UNDERLINE   = "\033[4m"
    BLACK       = "\033[30m"
    RED         = "\033[31m"
    GREEN       = "\033[32m"
    YELLOW      = "\033[33m"
    BLUE        = "\033[34m"
    MAGENTA     = "\033[35m"
    CYAN        = "\033[36m"
    WHITE       = "\033[37m"
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_YELLOW   = "\033[43m"
    BG_BLUE     = "\033[44m"

# ------------------------------------------------------------------------------
# FUNCIÓN PRINCIPAL (REQUISITOS R1-R5)
# ------------------------------------------------------------------------------
def calcular_precio_final(precio_original: float, descuento: float) -> float:
    """
    Calcula el precio final tras aplicar un descuento porcentual.

    Parámetros
    ----------
    precio_original : float
        Precio inicial del producto (debe ser > 0).
    descuento : float
        Porcentaje de descuento a aplicar (0-100 inclusive).

    Retorna
    -------
    float
        Precio final redondeado a 2 decimales.

    Lanza
    -----
    ValueError
        Si el precio original no es positivo.
    ValueError
        Si el descuento no está en el rango [0, 100].

    Notas
    -----
    - Si el descuento es superior al 80%, se aplica un 5% adicional
      sobre el precio ya descontado.
    - El resultado se redondea a 2 decimales.
    """
    # R2: Validar precio original positivo
    if precio_original <= 0:
        raise ValueError(
            f"El precio original debe ser un número positivo. Recibido: {precio_original}"
        )

    # R1: Validar descuento entre 0 y 100
    if not (0 <= descuento <= 100):
        raise ValueError(
            f"El descuento debe estar entre 0 y 100 (inclusive). Recibido: {descuento}"
        )

    # R3: Cálculo básico
    precio_descontado = precio_original * (1 - descuento / 100)

    # R5: Descuento adicional del 5% si descuento > 80%
    if descuento > 80:
        precio_descontado *= 0.95  # Aplica 5% sobre el ya descontado

    # R4: Redondear a 2 decimales
    return round(precio_descontado, 2)

# ------------------------------------------------------------------------------
# FUNCIONES AUXILIARES DE INTERFAZ
# ------------------------------------------------------------------------------
def limpiar_pantalla():
    """Limpia la consola (funciona en Windows y Unix)."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def imprimir_encabezado():
    """Muestra un banner llamativo con el nombre de la aplicación."""
    print(f"{Color.CYAN}{Color.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║       CALCULADORA DE DESCUENTOS          ║")
    print("║         Profesional & Creativa           ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Color.RESET}")

def leer_numero_positivo(mensaje: str) -> float:
    """
    Solicita un número positivo por consola con manejo de errores.
    Repite hasta obtener un valor válido.
    """
    while True:
        raw = input(f"{Color.YELLOW}{mensaje}{Color.RESET}")
        try:
            valor = float(raw)
            if valor <= 0:
                print(f"{Color.RED}⚠ El valor debe ser mayor que cero.{Color.RESET}")
                auditoria.registrar_error("Precio no positivo", precio_raw=raw)
                continue
            return valor
        except ValueError:
            print(f"{Color.RED}⚠ Entrada inválida. Ingrese un número válido.{Color.RESET}")
            auditoria.registrar_error("Precio no numérico", precio_raw=raw)

def leer_descuento(mensaje: str = "Ingrese el descuento (%): ") -> float:
    """Solicita el porcentaje de descuento (0-100)."""
    while True:
        raw = input(f"{Color.YELLOW}{mensaje}{Color.RESET}")
        try:
            descuento = float(raw)
            if descuento < 0 or descuento > 100:
                print(f"{Color.RED}⚠ El descuento debe estar entre 0 y 100.{Color.RESET}")
                auditoria.registrar_error("Descuento fuera de rango [0,100]", descuento_raw=raw)
                continue
            return descuento
        except ValueError:
            print(f"{Color.RED}⚠ Entrada inválida. Ingrese un número (ej: 15.5).{Color.RESET}")
            auditoria.registrar_error("Descuento no numérico", descuento_raw=raw)

def mostrar_resultado(precio_original: float, descuento: float, precio_final: float):
    """Muestra una caja con los detalles del cálculo."""
    ahorro = precio_original - precio_final
    print(f"\n{Color.BG_GREEN}{Color.BLACK}{Color.BOLD}  RESULTADO DEL CÁLCULO  {Color.RESET}")
    print(f"{Color.GREEN}{'─' * 40}{Color.RESET}")
    print(f"  Precio original:       ${precio_original:>10.2f}")
    print(f"  Descuento aplicado:     {descuento:>10.2f}%")
    if descuento > 80:
        print(f"  {Color.MAGENTA}¡Descuento adicional del 5% aplicado!{Color.RESET}")
    print(f"  Precio final:          ${precio_final:>10.2f}")
    print(f"  Ahorro total:          ${ahorro:>10.2f}")
    print(f"{Color.GREEN}{'─' * 40}{Color.RESET}\n")

def mostrar_resultado_multiple(productos: list):
    """Muestra tabla resumen de varios productos calculados."""
    total_orig   = sum(p[1] for p in productos)
    total_final  = sum(p[3] for p in productos)
    total_ahorro = total_orig - total_final
    sep = "─" * 74
    print(f"\n{Color.BG_GREEN}{Color.BLACK}{Color.BOLD}  RESUMEN — CÁLCULO MÚLTIPLE  {Color.RESET}")
    print(f"{Color.GREEN}{sep}{Color.RESET}")
    print(f"  {'#':<3} {'Producto':<18} {'Precio Orig':>12} {'Desc.':>7} {'Precio Final':>13} {'Ahorro':>11}")
    print(f"  {'─'*3} {'─'*18} {'─'*12} {'─'*7} {'─'*13} {'─'*11}")
    for i, (nombre, precio, desc, final) in enumerate(productos, 1):
        ahorro = precio - final
        marca  = f"{Color.MAGENTA}★{Color.RESET}" if desc > 80 else " "
        print(f"  {i:<3} {nombre:<18} ${precio:>11.2f} {desc:>6.1f}% {marca} ${final:>11.2f} ${ahorro:>9.2f}")
    print(f"  {'─'*3} {'─'*18} {'─'*12} {'─'*7} {'─'*13} {'─'*11}")
    print(f"  {'':3} {Color.BOLD}{'TOTALES':<18}{Color.RESET} ${total_orig:>11.2f} {'':>8} ${total_final:>11.2f} ${total_ahorro:>9.2f}")
    print(f"{Color.GREEN}{sep}{Color.RESET}")
    if any(p[2] > 80 for p in productos):
        print(f"  {Color.MAGENTA}★ Descuento adicional del 5% aplicado (desc. > 80%){Color.RESET}")
    print()

def ejecutar_calculo_multiple():
    """Calcula descuentos de varios productos en una sola sesión."""
    limpiar_pantalla()
    imprimir_encabezado()
    print(f"{Color.BLUE}→ CÁLCULO MÚLTIPLE DE PRODUCTOS{Color.RESET}\n")

    while True:
        try:
            raw = input(f"{Color.YELLOW}¿Cuántos productos desea calcular? (mín. 2): {Color.RESET}")
            n = int(raw)
            if n < 2:
                print(f"{Color.RED}⚠ Ingrese al menos 2 productos.{Color.RESET}")
                continue
            break
        except ValueError:
            print(f"{Color.RED}⚠ Ingrese un número entero válido.{Color.RESET}")

    productos = []
    for i in range(1, n + 1):
        print(f"\n{Color.CYAN}── Producto {i} de {n} {'─' * 28}{Color.RESET}")
        nombre = input(f"{Color.YELLOW}  Nombre del producto #{i}: {Color.RESET}").strip()
        if not nombre:
            nombre = f"Producto #{i}"
        precio = leer_numero_positivo(f"  Precio de '{nombre}': $ ")
        desc   = leer_descuento(f"  Descuento para '{nombre}' (%): ")
        try:
            resultado = calcular_precio_final(precio, desc)
        except ValueError as e:
            print(f"{Color.RED}⚠ Error inesperado: {e}{Color.RESET}")
            auditoria.registrar_error(str(e), precio_raw=str(precio), descuento_raw=str(desc))
            continue
        productos.append((nombre, precio, desc, resultado))
        print(f"  {Color.GREEN}✔ Precio final: ${resultado:.2f}{Color.RESET}")

    if not productos:
        print(f"{Color.RED}No se registró ningún producto válido.{Color.RESET}")
        input(f"{Color.CYAN}Presione ENTER para continuar...{Color.RESET}")
        return

    print(f"\n{Color.CYAN}Calculando totales", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f"{Color.RESET}\n")

    mostrar_resultado_multiple(productos)
    auditoria.registrar_calculo_multiple(productos)
    input(f"{Color.CYAN}Presione ENTER para continuar...{Color.RESET}")

def ejecutar_calculo():
    """Maneja el flujo de un cálculo: entrada → cálculo → salida."""
    limpiar_pantalla()
    imprimir_encabezado()
    print(f"{Color.BLUE}→ NUEVO CÁLCULO{Color.RESET}\n")

    # Entrada de datos
    precio = leer_numero_positivo("Ingrese el precio original: $ ")
    desc = leer_descuento()

    # Animación simple de "pensando"
    print(f"\n{Color.CYAN}Calculando", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(f"{Color.RESET}\n")

    # Calcular
    try:
        resultado = calcular_precio_final(precio, desc)
    except ValueError as e:
        # Esto no debería ocurrir si validamos antes, pero por seguridad
        print(f"{Color.RED}⚠ Error inesperado: {e}{Color.RESET}")
        auditoria.registrar_error(f"ValueError inesperado: {e}",
                                  precio_raw=str(precio), descuento_raw=str(desc))
        return

    # Registrar el cálculo exitoso en la auditoría
    auditoria.registrar_calculo(precio, desc, resultado)

    mostrar_resultado(precio, desc, resultado)

    input(f"{Color.CYAN}Presione ENTER para continuar...{Color.RESET}")

def menu_principal():
    """Bucle principal del menú interactivo."""
    global _num_calculos
    _num_calculos = 0
    while True:
        limpiar_pantalla()
        imprimir_encabezado()
        print(f"{Color.WHITE}Seleccione una opción:{Color.RESET}")
        print(f"  {Color.YELLOW}1{Color.RESET}. Calcular descuento  (un producto)")
        print(f"  {Color.YELLOW}2{Color.RESET}. Calcular descuentos (varios productos)")
        print(f"  {Color.YELLOW}3{Color.RESET}. Salir\n")
        opcion = input(f"{Color.CYAN}Opción (1-3): {Color.RESET}").strip()

        if opcion == "1":
            ejecutar_calculo()
            _num_calculos += 1
        elif opcion == "2":
            ejecutar_calculo_multiple()
            _num_calculos += 1
        elif opcion == "3":
            limpiar_pantalla()
            print(f"{Color.GREEN}{Color.BOLD}¡Gracias por usar la Calculadora de Descuentos!{Color.RESET}")
            print(f"{Color.CYAN}Desarrollado con Python + ANSI art.{Color.RESET}\n")
            auditoria.cerrar_sesion(_num_calculos)
            sys.exit(0)
        else:
            print(f"{Color.RED}⚠ Opción no válida. Intente de nuevo.{Color.RESET}")
            time.sleep(1)

# ------------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    auditoria.iniciar_sesion()       # Registra inicio de sesión en el log
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}Ejecución interrumpida por el usuario.{Color.RESET}")
        auditoria.cerrar_sesion(_num_calculos)
        sys.exit(0)