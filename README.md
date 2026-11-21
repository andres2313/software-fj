# Software FJ – Sistema de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso Programación (213023) – UNAD.
Sistema orientado a objetos en Python, sin base de datos: usa objetos, listas y un archivo de logs.

## Contenido
- `software_fj.py`: código completo, documentado línea por línea.
- `software_fj.log`: registro de eventos y errores de la última simulación.

## Cómo ejecutarlo
1. Instalar Python 3.8 o superior.
2. En una terminal, dentro de la carpeta del proyecto: `python software_fj.py`
3. Se muestran en pantalla 12 operaciones (válidas e inválidas) y se genera `software_fj.log`.

## Conceptos aplicados
- Abstracción: `EntidadBase` y `Servicio` (clases abstractas).
- Herencia y polimorfismo: `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- Sobrecarga simulada: `costo_total(horas, *args)`.
- Encapsulación: atributos privados y validaciones en `Cliente`.
- Excepciones: personalizadas, `try/except/else/finally` y encadenamiento (`raise ... from`).
