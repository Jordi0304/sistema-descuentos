# language: es

Característica: Calculadora de Descuentos
  Como usuario de la calculadora
  Quiero calcular precios finales con descuento
  Para saber cuánto pagaré por un producto

  Escenario: Descuento básico del 50%
    Dado que el precio original es 200.00
    Y el descuento es 50.0 por ciento
    Cuando calculo el precio final
    Entonces el precio final debe ser 100.00

  Escenario: Sin descuento el precio no cambia
    Dado que el precio original es 150.75
    Y el descuento es 0.0 por ciento
    Cuando calculo el precio final
    Entonces el precio final debe ser 150.75

  Escenario: Descuento del 100% devuelve cero
    Dado que el precio original es 999.99
    Y el descuento es 100.0 por ciento
    Cuando calculo el precio final
    Entonces el precio final debe ser 0.00

  Escenario: Descuento mayor al 80% activa bonificación adicional del 5%
    Dado que el precio original es 200.00
    Y el descuento es 85.0 por ciento
    Cuando calculo el precio final
    Entonces el precio final debe ser 28.50

  Escenario: Descuento exacto del 80% no activa bonificación adicional
    Dado que el precio original es 100.00
    Y el descuento es 80.0 por ciento
    Cuando calculo el precio final
    Entonces el precio final debe ser 20.00

  Escenario: Precio negativo genera error
    Dado que el precio original es -50.00
    Y el descuento es 10.0 por ciento
    Cuando calculo el precio final debe fallar
    Entonces se debe lanzar un error de valor

  Escenario: Descuento fuera de rango genera error
    Dado que el precio original es 100.00
    Y el descuento es 150.0 por ciento
    Cuando calculo el precio final debe fallar
    Entonces se debe lanzar un error de valor
