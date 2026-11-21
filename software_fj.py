"""
Software FJ - Sistema integral de gestión de clientes, servicios y reservas.
Programación (213023) - UNAD. Sin bases de datos: solo objetos, listas y un
archivo de texto para el registro de eventos y errores.
"""
import logging  # módulo estándar para escribir el archivo de logs
import re  # expresiones regulares, usadas para validar el correo
from abc import ABC, abstractmethod  # herramientas para crear clases y métodos abstractos
from datetime import datetime  # permite obtener la fecha actual para el log

# ---------------------------------------------------------------
# 1. REGISTRO DE EVENTOS (archivo de logs)
# ---------------------------------------------------------------
logging.basicConfig(  # configura el sistema de logs
    filename="software_fj.log",  # nombre del archivo donde se guardan los eventos
    filemode="w",  # "w" crea el archivo nuevo en cada ejecución
    level=logging.INFO,  # registra mensajes desde nivel INFO hacia arriba
    format="%(asctime)s | %(levelname)-8s | %(message)s",  # formato: fecha | nivel | mensaje
    encoding="utf-8",  # codificación que permite tildes y ñ
)  # fin de la configuración
log = logging.getLogger("SoftwareFJ")  # objeto logger que usará todo el programa


# ---------------------------------------------------------------
# 2. EXCEPCIONES PERSONALIZADAS
# ---------------------------------------------------------------
class SoftwareFJError(Exception):  # excepción base: todas las demás heredan de ella
    """Excepción base del sistema."""  # descripción de la clase


class ClienteInvalidoError(SoftwareFJError):  # error por datos de cliente inválidos
    """Datos de cliente inválidos o incompletos."""  # descripción de la clase


class ServicioInvalidoError(SoftwareFJError):  # error por parámetros de servicio inválidos
    """Parámetros de servicio inválidos."""  # descripción de la clase


class ServicioNoDisponibleError(SoftwareFJError):  # error cuando el servicio está bloqueado
    """El servicio no está disponible para reservar."""  # descripción de la clase


class ReservaInvalidaError(SoftwareFJError):  # error por una reserva mal formada
    """Intento de reserva incorrecto."""  # descripción de la clase


class OperacionNoPermitidaError(SoftwareFJError):  # error por acciones no válidas según el estado
    """Operación no permitida para el estado actual."""  # descripción de la clase


class CalculoInconsistenteError(SoftwareFJError):  # error por cálculos de costo incoherentes
    """El cálculo de costos produjo un resultado inconsistente."""  # descripción de la clase


# ---------------------------------------------------------------
# 3. CLASE ABSTRACTA GENERAL
# ---------------------------------------------------------------
class EntidadBase(ABC):  # clase abstracta: no se puede instanciar directamente
    """Representa cualquier entidad del sistema (cliente, servicio, reserva)."""
    _contadores = {}  # diccionario compartido que cuenta cuántas entidades hay por categoría

    def __init__(self):  # constructor de la entidad
        self._id = None  # el id se asigna solo cuando la entidad se creó sin errores

    def _asignar_id(self, categoria):  # método que numera la entidad dentro de su categoría
        EntidadBase._contadores[categoria] = EntidadBase._contadores.get(categoria, 0) + 1  # suma 1 al contador de la categoría
        self._id = EntidadBase._contadores[categoria]  # guarda el número como id de este objeto

    @property  # permite leer el id como si fuera un atributo
    def id(self):  # getter del id
        return self._id  # devuelve el id (solo lectura)

    @abstractmethod  # obliga a las clases hijas a implementar este método
    def describir(self) -> str:  # firma del método abstracto
        """Devuelve una descripción legible de la entidad."""  # descripción del método


# ---------------------------------------------------------------
# 4. CLIENTE (encapsulación y validaciones)
# ---------------------------------------------------------------
class Cliente(EntidadBase):  # clase Cliente, hija de EntidadBase
    def __init__(self, nombre, documento, correo, telefono):  # constructor con los 4 datos personales
        super().__init__()  # llama al constructor de la clase padre
        self.nombre = nombre  # usa el setter de nombre (valida el dato)
        self.documento = documento  # usa el setter de documento (valida el dato)
        self.correo = correo  # usa el setter de correo (valida el dato)
        self.telefono = telefono  # usa el setter de teléfono (valida el dato)
        self._asignar_id("cliente")  # solo si todo fue válido, se numera el cliente

    @property  # getter del nombre
    def nombre(self):  # lectura del nombre
        return self.__nombre  # atributo privado (doble guion bajo = encapsulado)

    @nombre.setter  # setter del nombre
    def nombre(self, valor):  # recibe el nombre a validar
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # debe ser texto de al menos 3 caracteres
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")  # lanza error si no cumple
        if not all(c.isalpha() or c.isspace() for c in valor):  # solo letras y espacios
            raise ClienteInvalidoError("El nombre solo puede contener letras.")  # lanza error si hay otros símbolos
        self.__nombre = valor.strip().title()  # guarda el nombre limpio y con mayúscula inicial

    @property  # getter del documento
    def documento(self):  # lectura del documento
        return self.__documento  # devuelve el atributo privado

    @documento.setter  # setter del documento
    def documento(self, valor):  # recibe el documento a validar
        if valor is None:  # si no se envió documento
            raise ClienteInvalidoError("Falta el documento del cliente.")  # lanza error por dato faltante
        valor = str(valor).strip()  # convierte a texto y quita espacios
        if not valor.isdigit() or not 6 <= len(valor) <= 10:  # solo dígitos y entre 6 y 10 caracteres
            raise ClienteInvalidoError("El documento debe tener entre 6 y 10 dígitos.")  # lanza error si no cumple
        self.__documento = valor  # guarda el documento válido

    @property  # getter del correo
    def correo(self):  # lectura del correo
        return self.__correo  # devuelve el atributo privado

    @correo.setter  # setter del correo
    def correo(self, valor):  # recibe el correo a validar
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor):  # texto con formato usuario@dominio.ext
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")  # lanza error mostrando el valor recibido
        self.__correo = valor.lower()  # guarda el correo en minúsculas

    @property  # getter del teléfono
    def telefono(self):  # lectura del teléfono
        return self.__telefono  # devuelve el atributo privado

    @telefono.setter  # setter del teléfono
    def telefono(self, valor):  # recibe el teléfono a validar
        valor = str(valor).strip()  # convierte a texto y quita espacios
        if not valor.isdigit() or len(valor) != 10:  # solo dígitos y exactamente 10
            raise ClienteInvalidoError("El teléfono debe tener 10 dígitos.")  # lanza error si no cumple
        self.__telefono = valor  # guarda el teléfono válido

    def describir(self):  # implementa el método abstracto de EntidadBase
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo}"  # texto con los datos del cliente


# ---------------------------------------------------------------
# 5. SERVICIO ABSTRACTO Y SERVICIOS ESPECIALIZADOS
# ---------------------------------------------------------------
class Servicio(EntidadBase, ABC):  # clase abstracta de la que heredan todos los servicios
    IVA = 0.19  # impuesto por defecto (19 %), compartido por todos los servicios

    def __init__(self, nombre, tarifa_hora):  # constructor con nombre y tarifa por hora
        super().__init__()  # llama al constructor de EntidadBase
        if not isinstance(nombre, str) or not nombre.strip():  # el nombre debe ser texto no vacío
            raise ServicioInvalidoError("El servicio requiere un nombre.")  # error si falta el nombre
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # la tarifa debe ser número positivo
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor a 0.")  # error si la tarifa no es válida
        self._nombre = nombre.strip()  # guarda el nombre sin espacios sobrantes
        self._tarifa_hora = float(tarifa_hora)  # guarda la tarifa como número decimal
        self._disponible = True  # todo servicio nuevo empieza disponible

    @property  # getter del nombre
    def nombre(self):  # lectura del nombre del servicio
        return self._nombre  # devuelve el nombre

    @property  # getter de disponibilidad
    def disponible(self):  # lectura de la disponibilidad
        return self._disponible  # devuelve True o False

    @disponible.setter  # setter de disponibilidad
    def disponible(self, valor):  # recibe el nuevo estado
        self._disponible = bool(valor)  # lo convierte a booleano y lo guarda

    @abstractmethod  # cada servicio debe implementarlo a su manera
    def calcular_costo(self, horas):  # firma del cálculo de costo base
        """Costo base (sin impuestos ni descuentos)."""  # descripción del método

    @abstractmethod  # cada servicio debe implementarlo a su manera
    def validar_parametros(self, horas):  # firma de la validación propia del servicio
        """Valida los parámetros propios de cada servicio."""  # descripción del método

    # Método "sobrecargado": Python no tiene sobrecarga nativa, se simula con *args
    #   costo_total(horas)                       -> con IVA por defecto
    #   costo_total(horas, descuento)            -> con descuento + IVA
    #   costo_total(horas, descuento, impuesto)  -> con descuento e impuesto propios
    def costo_total(self, horas, *args):  # *args recibe 0, 1 o 2 parámetros extra
        if len(args) > 2:  # más de 2 extras no está permitido
            raise CalculoInconsistenteError("costo_total admite como máximo 2 parámetros extra.")  # error por exceso de parámetros
        descuento = args[0] if len(args) >= 1 else 0.0  # primer extra = descuento; si no hay, 0
        impuesto = args[1] if len(args) == 2 else self.IVA  # segundo extra = impuesto; si no hay, IVA
        if not 0 <= descuento < 1 or not 0 <= impuesto < 1:  # ambos deben estar entre 0 y 1
            raise CalculoInconsistenteError("Descuento e impuesto deben estar entre 0 y 1.")  # error si están fuera de rango
        base = self.calcular_costo(horas)  # polimorfismo: cada servicio calcula su costo base
        total = base * (1 - descuento) * (1 + impuesto)  # aplica descuento y luego impuesto
        if total <= 0:  # un total no positivo es incoherente
            raise CalculoInconsistenteError("El costo total calculado no es válido.")  # error por cálculo inválido
        return round(total, 2)  # devuelve el total con 2 decimales


class ReservaSala(Servicio):  # servicio especializado: reserva de salas
    def __init__(self, nombre, tarifa_hora, capacidad):  # recibe además la capacidad de la sala
        super().__init__(nombre, tarifa_hora)  # reutiliza el constructor de Servicio
        if not isinstance(capacidad, int) or capacidad < 1:  # la capacidad debe ser entero positivo
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")  # error si no cumple
        self._capacidad = capacidad  # guarda la capacidad
        self._asignar_id("servicio")  # numera el servicio solo si todo fue válido

    def validar_parametros(self, horas):  # sobrescribe la validación para salas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:  # una sala se reserva de 1 a 8 horas
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")  # error si la duración no es válida

    def calcular_costo(self, horas):  # sobrescribe el cálculo de costo para salas
        self.validar_parametros(horas)  # valida las horas antes de calcular
        recargo = 1.10 if self._capacidad > 20 else 1.0  # salas de más de 20 personas cuestan 10 % más
        return self._tarifa_hora * horas * recargo  # tarifa x horas x recargo

    def describir(self):  # sobrescribe la descripción
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"  # texto con los datos de la sala


class AlquilerEquipo(Servicio):  # servicio especializado: alquiler de equipos
    def __init__(self, nombre, tarifa_hora, tipo_equipo, seguro=False):  # seguro es un parámetro opcional
        super().__init__(nombre, tarifa_hora)  # reutiliza el constructor de Servicio
        if not tipo_equipo:  # el tipo de equipo es obligatorio
            raise ServicioInvalidoError("Falta el tipo de equipo.")  # error si falta
        self._tipo = tipo_equipo  # guarda el tipo de equipo
        self._seguro = seguro  # guarda si incluye seguro
        self._asignar_id("servicio")  # numera el servicio solo si todo fue válido

    def validar_parametros(self, horas):  # sobrescribe la validación para equipos
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:  # un equipo se alquila de 1 a 72 horas
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")  # error si la duración no es válida

    def calcular_costo(self, horas):  # sobrescribe el cálculo de costo para equipos
        self.validar_parametros(horas)  # valida las horas antes de calcular
        costo = self._tarifa_hora * horas  # costo base = tarifa x horas
        return costo * 1.05 if self._seguro else costo  # con seguro se suma 5 %

    def describir(self):  # sobrescribe la descripción
        extra = " con seguro" if self._seguro else ""  # texto adicional si incluye seguro
        return f"Equipo '{self.nombre}' ({self._tipo}{extra}) - ${self._tarifa_hora:,.0f}/h"  # texto con los datos del equipo


class Asesoria(Servicio):  # servicio especializado: asesorías
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # multiplicador de tarifa según el nivel del asesor

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):  # nivel por defecto: junior
        super().__init__(nombre, tarifa_hora)  # reutiliza el constructor de Servicio
        if nivel not in self.NIVELES:  # el nivel debe existir en el diccionario
            raise ServicioInvalidoError(f"Nivel de asesor inválido: {nivel!r}")  # error si el nivel no existe
        self._especialidad = especialidad  # guarda la especialidad
        self._nivel = nivel  # guarda el nivel del asesor
        self._asignar_id("servicio")  # numera el servicio solo si todo fue válido

    def validar_parametros(self, horas):  # sobrescribe la validación para asesorías
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 6:  # una asesoría dura de 0.5 a 6 horas
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 6 horas.")  # error si la duración no es válida

    def calcular_costo(self, horas):  # sobrescribe el cálculo de costo para asesorías
        self.validar_parametros(horas)  # valida las horas antes de calcular
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]  # tarifa x horas x multiplicador del nivel

    def describir(self):  # sobrescribe la descripción
        return f"Asesoría '{self.nombre}' ({self._especialidad}, {self._nivel}) - ${self._tarifa_hora:,.0f}/h"  # texto con los datos de la asesoría


# ---------------------------------------------------------------
# 6. RESERVA
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
# 7. GESTOR (listas internas) Y SIMULACIÓN
# ---------------------------------------------------------------
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
