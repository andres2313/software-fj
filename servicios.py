"""Servicio abstracto y servicios especializados (sala, equipo, asesoría)."""
from abc import ABC, abstractmethod  # herramientas para crear clases y métodos abstractos

from entidades import EntidadBase  # clase base de la que hereda Servicio
from excepciones import ServicioInvalidoError, CalculoInconsistenteError  # errores propios usados aquí


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
