###################### Funciones para el manejo de archivos LOG ######################
import os
import logging
from datetime import datetime

def setup_logger(log_paths, alarma, desarrollador=""):
    """
    Configura un logger personalizado con múltiples rutas de archivos log.
    :param log_paths: Lista de rutas donde se guardarán los logs.
    :param alarma: Nombre del logger.
    :param desarrollador: Nombre del desarrollador.
    :param MOM: Identificador MOM.
    :param hora_ejecucion: Hora de ejecución proporcionada por el usuario.
    :return: Logger configurado.
    """
    
    # Asegurar que log_paths sea una lista (acepta una sola ruta también)
    if isinstance(log_paths, str):
        log_paths = [log_paths]

    # Crear directorios si no existen
    for path in log_paths:
        os.makedirs(path, exist_ok=True)

    class CustomFormatter(logging.Formatter):
        def __init__(self, desarrollador,  *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.desarrollador = desarrollador
        
        def format(self, record):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Se utiliza la hora_ejecucion proporcionada por el usuario
            return (
                f"{record.levelname} [{current_time}]- {self.desarrollador}- {record.getMessage()}"
            )

    # Crear o recuperar el logger
    logger = logging.getLogger(alarma)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Evitar añadir múltiples handlers en caso de que ya existan
    if not logger.handlers:
        formatter = CustomFormatter(desarrollador)

        # Handler para la consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handlers para archivos en múltiples rutas
        for path in log_paths:
            log_file = os.path.join(path, f"{alarma}.log")
            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

def log_message(logger, level, msg):
    """
    Registra un mensaje en el logger proporcionado.
    """
    if level.upper() == "INFO":
        logger.info(msg)
    elif level.upper() == "WARNING":
        logger.warning(msg)
    elif level.upper() == "ERROR":
        logger.error(msg)
    elif level.upper() == "DEBUG":
        logger.debug(msg)
    else:
        logger.info(msg)  # Por defecto usa INFO


############################### Funciones para la generacion de features ###############################
import polars as pl

def generar_características(df, agg_num_exprs, agg_cat_exprs):
    df = (
        df
        .with_columns(pl.col("S_2").str.strptime(pl.Date, "%Y-%m-%d"))
        .sort(["customer_ID", "S_2"])
    )

    features = (
        df
        .group_by("customer_ID")
        .agg(agg_num_exprs + agg_cat_exprs)
        .collect()
    )

    return features