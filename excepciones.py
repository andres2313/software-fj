"""Excepciones personalizadas de Software FJ."""


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
