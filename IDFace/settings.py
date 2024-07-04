import os
from pathlib import Path

# DIRECTORIO BASE
BASE_DIR = Path(__file__).resolve().parent

# ARCHIVOS ESTATICOS
MODELS_DIR = os.path.join(BASE_DIR, "models")

# CODIGOS DE ERROR
DOCUMENT_NOT_FOUND_ERROR = "DOCUMENT_NOT_FOUND_ERROR"
FACE_NOT_FOUND_ERROR = "FACE_NOT_FOUND_ERROR"
FACE_NOT_MATCH_ERROR = "FACE_NOT_MATCH_ERROR"
IDENTIFICATION_NOT_FOUND_ERROR = "IDENTIFICATION_NOT_FOUND_ERROR"
BIRTH_DATE_NOT_FOUND_ERROR = "BIRTH_DATE_NOT_FOUND_ERROR"
NAME_NOT_FOUND_ERROR = "NAME_NOT_FOUND_ERROR"
LAST_NAME_NOT_FOUND_ERROR = "LAST_NAME_NOT_FOUND_ERROR"


# # # # # # # # # # # # # # # # # # #
# VENEZUELA
# # # # # # # # # # # # # # # # # # #

# MODELOS
VENEZUELA_ID_EXTRACTION_MODEL = os.path.join(MODELS_DIR, "cedula_extraction.pt")
VENEZUELA_ID_RECOGNITION_MODEL = os.path.join(MODELS_DIR, "cedula_recognition.pt")

# DOCUMENTOS
VENEZUELA_ID = "cedula_venezuela"

# CONTENIDO
LAST_NAME = "apellidos"
CIVIL_STATUS = "edo_civil"
EXPEDITION_DATE = "fecha_expedicion"
BIRTH_DATE = "fecha_nacimiento"
EXPIRATION_DATE = "fecha_vencimiento"
PHOTO = "foto"
IDENTIFICATION = "identificacion"
NACIONALITY = "nacionalidad"
NAME = "nombres"
