"""Programa principal: simula 12 operaciones (válidas e inválidas) de Software FJ."""
from datetime import datetime  # permite obtener la fecha actual para el log

from registro import log  # logger compartido que escribe en software_fj.log
from excepciones import OperacionNoPermitidaError, CalculoInconsistenteError  # errores que se capturan en la simulación
from servicios import ReservaSala, AlquilerEquipo, Asesoria  # los tres servicios especializados
from reservas import GestorFJ  # gestor con las listas internas


def simular():  # ejecuta las 12 operaciones de prueba
    print("=" * 62)  # línea decorativa
    print(" SOFTWARE FJ - Simulación de 12 operaciones")  # título
    print("=" * 62)  # línea decorativa
    g = GestorFJ()  # crea el gestor con sus listas vacías
    log.info("Inicio de simulación %s", datetime.now().strftime("%Y-%m-%d"))  # registra la fecha de inicio

    print("\n1. Cliente válido")  # operación 1
    ana = g.registrar_cliente("ana maria rojas", "1090123456", "ana@correo.com", "3101234567")  # cliente correcto
    print("\n2. Cliente con correo inválido")  # operación 2
    g.registrar_cliente("Luis Perez", "1098765432", "luis#correo", "3207654321")  # correo sin @: debe fallar
    print("\n3. Cliente con parámetro faltante")  # operación 3
    g.registrar_cliente("Carlos Diaz", "1012345678", "carlos@correo.com")  # falta el teléfono: debe fallar
    print("\n4. Segundo cliente válido")  # operación 4
    juan = g.registrar_cliente("Juan Gomez", "80123456", "juan@correo.com", "3001112233")  # cliente correcto
    print("\n5. Sala válida")  # operación 5
    sala = g.crear_servicio(ReservaSala, "Sala Innovación", 50000, 25)  # sala correcta
    print("\n6. Equipo con tarifa inválida")  # operación 6
    g.crear_servicio(AlquilerEquipo, "Portátil", -100, "Computador")  # tarifa negativa: debe fallar
    print("\n7. Equipo y asesoría válidos")  # operación 7
    equipo = g.crear_servicio(AlquilerEquipo, "Video Beam", 20000, "Proyector", True)  # equipo con seguro
    asesoria = g.crear_servicio(Asesoria, "Asesoría Python", 80000, "Programación", "senior")  # asesoría senior
    print("\n8. Reserva exitosa de sala (3h, 10% descuento)")  # operación 8
    g.reservar(ana, sala, 3, True, 0.10)  # reserva correcta, confirmada y procesada
    print("\n9. Reserva con duración inválida (12h en sala)")  # operación 9
    g.reservar(juan, sala, 12)  # 12 h supera el máximo de 8: debe fallar
    print("\n10. Reserva de servicio no disponible")  # operación 10
    equipo.disponible = False  # bloquea el equipo
    g.reservar(juan, equipo, 5)  # servicio no disponible: debe fallar
    print("\n11. Reserva sin pagar y cancelación doble")  # operación 11
    r = g.reservar(juan, asesoria, 2, confirmar=False)  # reserva pendiente, sin confirmar
    if r:  # si la reserva se creó
        r.cancelar()  # primera cancelación: válida
        try:  # intenta cancelar por segunda vez
            r.cancelar()  # segunda cancelación: no permitida
        except OperacionNoPermitidaError as e:  # captura el error esperado
            log.error("Cancelación inválida: %s", e)  # registra el error
            print(f"   ✗ Operación no permitida: {e}")  # informa en pantalla
    print("\n12. Polimorfismo: costo de 2h en cada servicio con sobrecarga")  # operación 12
    equipo.disponible = True  # vuelve a habilitar el equipo
    for s in g.servicios:  # recorre todos los servicios sin importar su tipo
        print(f"   {s.nombre:<16} base: ${s.calcular_costo(2):>10,.2f} | "  # costo base de 2 horas
              f"con IVA: ${s.costo_total(2):>10,.2f} | "  # variante 1: solo horas
              f"desc. 15%: ${s.costo_total(2, 0.15):>10,.2f} | "  # variante 2: horas y descuento
              f"desc. 15% + imp. 8%: ${s.costo_total(2, 0.15, 0.08):>10,.2f}")  # variante 3: descuento e impuesto
    try:  # prueba un descuento imposible
        sala.costo_total(2, 1.5)  # descuento de 150 %: debe fallar
    except CalculoInconsistenteError as e:  # captura el error esperado
        log.error("Cálculo inconsistente: %s", e)  # registra el error
        print(f"   ✗ Cálculo inconsistente controlado: {e}")  # informa en pantalla

    print("\n" + "=" * 62)  # línea decorativa
    print(f" Resumen: {len(g.clientes)} clientes | {len(g.servicios)} servicios | {len(g.reservas)} reservas")  # totales finales
    print(" El sistema siguió funcionando ante todos los errores.")  # mensaje de cierre
    print(" Detalle de eventos y errores en: software_fj.log")  # indica dónde está el log
    print("=" * 62)  # línea decorativa


if __name__ == "__main__":  # se cumple solo al ejecutar este archivo directamente
    simular()  # lanza la simulación
