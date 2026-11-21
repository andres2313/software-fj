"""Entidades base del sistema: clase abstracta EntidadBase y Cliente."""
import re  # expresiones regulares, usadas para validar el correo
from abc import ABC, abstractmethod  # herramientas para crear clases y métodos abstractos

from excepciones import ClienteInvalidoError  # error propio para datos de cliente inválidos


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
