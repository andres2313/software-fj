"""Reserva (cliente + servicio + duración + estado) y el gestor con listas internas."""
from entidades import EntidadBase, Cliente  # clase base y Cliente
from servicios import Servicio  # clase abstracta de servicios
from registro import log  # logger compartido que escribe en software_fj.log
from excepciones import (  # errores propios usados en las reservas
    SoftwareFJError, ClienteInvalidoError, ServicioInvalidoError,
    ServicioNoDisponibleError, ReservaInvalidaError, OperacionNoPermitidaError,
)  # fin de la importación


class Reserva(EntidadBase):  # une cliente, servicio, duración y estado
    def __init__(self, cliente, servicio, horas):  # constructor de la reserva
        super().__init__()  # llama al constructor de EntidadBase
        if not isinstance(cliente, Cliente):  # el cliente debe ser un objeto Cliente
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")  # error si no lo es
        if not isinstance(servicio, Servicio):  # el servicio debe ser un objeto Servicio
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")  # error si no lo es
        if not servicio.disponible:  # no se reserva un servicio bloqueado
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")  # error de disponibilidad
        try:  # intenta validar la duración con las reglas del servicio
            servicio.validar_parametros(horas)  # cada servicio valida con su propia regla
        except ServicioInvalidoError as e:  # si la duración no es válida
            # Encadenamiento de excepciones: "from e" conserva la causa original
            raise ReservaInvalidaError("Duración inválida para la reserva.") from e  # lanza un error nuevo encadenado
        self.cliente = cliente  # guarda el cliente de la reserva
        self.servicio = servicio  # guarda el servicio reservado
        self.horas = horas  # guarda la duración en horas
        self.estado = "PENDIENTE"  # toda reserva nace pendiente
        self._asignar_id("reserva")  # numera la reserva solo si todo fue válido

    def confirmar(self):  # pasa la reserva a CONFIRMADA
        if self.estado != "PENDIENTE":  # solo se confirma una reserva pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self.estado}.")  # error si el estado no lo permite
        self.estado = "CONFIRMADA"  # cambia el estado
        log.info("Reserva #%s confirmada.", self.id)  # deja el evento en el log

    def cancelar(self):  # pasa la reserva a CANCELADA
        if self.estado in ("CANCELADA", "PROCESADA"):  # no se cancela lo ya cancelado o procesado
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self.estado}.")  # error si el estado no lo permite
        self.estado = "CANCELADA"  # cambia el estado
        log.info("Reserva #%s cancelada.", self.id)  # deja el evento en el log

    def procesar(self, descuento=0.0):  # calcula el cobro; el descuento es opcional
        """try/except/else/finally: calcula el costo y deja constancia siempre."""
        costo = None  # variable que guardará el costo calculado
        try:  # bloque donde pueden ocurrir errores
            if self.estado != "CONFIRMADA":  # solo se procesan reservas confirmadas
                raise OperacionNoPermitidaError("Solo se procesan reservas confirmadas.")  # error si no está confirmada
            costo = self.servicio.costo_total(self.horas, descuento)  # usa el método sobrecargado con descuento
        except SoftwareFJError as e:  # captura cualquier error propio del sistema
            log.error("Fallo al procesar reserva #%s: %s", self.id, e)  # registra el error en el log
            raise  # vuelve a lanzar el error para que lo maneje quien llamó
        else:  # se ejecuta solo si NO hubo errores en el try
            self.estado = "PROCESADA"  # marca la reserva como procesada
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{costo:,.2f}")  # registra el éxito y el total
            return costo  # devuelve el costo calculado
        finally:  # se ejecuta SIEMPRE, haya o no error
            log.info("Intento de procesamiento de reserva #%s finalizado (estado: %s).",
                     self.id, self.estado)  # deja constancia del intento y el estado final

    def describir(self):  # implementa el método abstracto
        return (f"Reserva #{self.id} [{self.estado}] {self.cliente.nombre} -> "  # inicio del texto: id, estado y cliente
                f"{self.servicio.nombre} x {self.horas}h")  # fin del texto: servicio y horas


class GestorFJ:  # administra las listas y controla los errores
    def __init__(self):  # constructor del gestor
        self.clientes, self.servicios, self.reservas = [], [], []  # tres listas internas, sin base de datos

    def registrar_cliente(self, *args):  # crea un cliente con los datos recibidos
        try:  # intenta crear el cliente
            c = Cliente(*args)  # desempaqueta los datos hacia el constructor
        except (ClienteInvalidoError, TypeError) as e:  # datos inválidos o parámetros faltantes
            log.error("Registro de cliente fallido: %s", e)  # registra el error en el log
            print(f"   ✗ Cliente rechazado: {e}")  # informa en pantalla
            return None  # no devuelve cliente, pero el programa sigue
        self.clientes.append(c)  # guarda el cliente en la lista
        log.info("Cliente registrado: %s", c.describir())  # registra el evento
        print(f"   ✓ {c.describir()}")  # informa en pantalla
        return c  # devuelve el cliente creado

    def crear_servicio(self, clase, *args):  # crea un servicio de la clase indicada
        try:  # intenta crear el servicio
            s = clase(*args)  # instancia la clase recibida (polimorfismo)
        except (ServicioInvalidoError, TypeError) as e:  # parámetros inválidos o faltantes
            log.error("Creación de servicio fallida (%s): %s", clase.__name__, e)  # registra el error
            print(f"   ✗ Servicio rechazado: {e}")  # informa en pantalla
            return None  # no devuelve servicio, pero el programa sigue
        self.servicios.append(s)  # guarda el servicio en la lista
        log.info("Servicio creado: %s", s.describir())  # registra el evento
        print(f"   ✓ {s.describir()}")  # informa en pantalla
        return s  # devuelve el servicio creado

    def reservar(self, cliente, servicio, horas, confirmar=True, descuento=0.0):  # crea y procesa una reserva
        try:  # agrupa todos los pasos que pueden fallar
            r = Reserva(cliente, servicio, horas)  # crea la reserva (valida todo)
            self.reservas.append(r)  # la guarda en la lista
            if confirmar:  # si se pidió confirmarla
                r.confirmar()  # pasa a CONFIRMADA
            total = r.procesar(descuento) if confirmar else None  # procesa solo si fue confirmada
        except SoftwareFJError as e:  # cualquier error propio del sistema
            causa = f" (causa: {e.__cause__})" if e.__cause__ else ""  # si hay excepción encadenada, muestra su causa
            log.error("Reserva fallida: %s%s", e, causa)  # registra el error y su causa
            print(f"   ✗ Reserva fallida: {e}{causa}")  # informa en pantalla
            return None  # no devuelve reserva, pero el programa sigue
        if total is not None:  # reserva confirmada y procesada
            print(f"   ✓ {r.describir()} | Total: ${total:,.2f}")  # muestra la reserva con su total
        else:  # reserva creada pero sin confirmar
            print(f"   ✓ {r.describir()}")  # muestra la reserva sin total
        return r  # devuelve la reserva creada
