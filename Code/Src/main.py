import sys
from pathlib import Path
import os

#Definimos la ruta principal del proyecto
main_path = Path(os.getcwd()).parent.parent

#Definimos rutas relativas
config_path = main_path / "Config"
data_path = main_path / "Data"
log_path = main_path / "Logs"

#Subrutas dentro de Data
input_data_path = data_path / "Input"
output_data_path = data_path / "Output"
other_data_path = data_path / "Other"

#Rutas de modelos
#models_path = other_data_path / "Models_Classification"

