"""Módulo de registro: configura el archivo de logs de Software FJ."""
import logging  # módulo estándar para escribir el archivo de logs

logging.basicConfig(  # configura el sistema de logs
    filename="software_fj.log",  # nombre del archivo donde se guardan los eventos
    filemode="w",  # "w" crea el archivo nuevo en cada ejecución
    level=logging.INFO,  # registra mensajes desde nivel INFO hacia arriba
    format="%(asctime)s | %(levelname)-8s | %(message)s",  # formato: fecha | nivel | mensaje
    encoding="utf-8",  # codificación que permite tildes y ñ
)  # fin de la configuración
log = logging.getLogger("SoftwareFJ")  # objeto logger que usará todo el programa
