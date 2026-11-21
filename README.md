# Software FJ – Sistema de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso Programación (213023) – UNAD.
Sistema orientado a objetos en Python, sin base de datos: usa objetos, listas y un archivo de logs.

## Estructura
| Archivo | Contenido |
|---|---|
| `main.py` | Programa principal: simulación de 12 operaciones (válidas e inválidas) |
| `registro.py` | Configuración del archivo de logs |
| `excepciones.py` | Excepciones personalizadas |
| `entidades.py` | Clase abstracta `EntidadBase` y `Cliente` |
| `servicios.py` | Clase abstracta `Servicio`, `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reservas.py` | `Reserva` y `GestorFJ` (listas internas) |
| `software_fj.log` | Registro de eventos y errores de la última ejecución |

## Cómo ejecutarlo
1. Instalar Python 3.8 o superior.
2. En una terminal, dentro de la carpeta del proyecto: `python main.py`
3. Se muestran en pantalla 12 operaciones y se genera `software_fj.log`.

## Conceptos aplicados
- Abstracción: `EntidadBase` y `Servicio` (clases abstractas).
- Herencia y polimorfismo: `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- Sobrecarga simulada: `costo_total(horas, *args)`.
- Encapsulación: atributos privados y validaciones en `Cliente`.
- Excepciones: personalizadas, `try/except/else/finally` y encadenamiento (`raise ... from`).
