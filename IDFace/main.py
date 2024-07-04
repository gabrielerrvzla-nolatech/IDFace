from pathlib import Path

from modules.extract_information import ExtractInformation
from modules.face_comparison import FaceComparison
from modules.recognition import Recognition

from .exceptions import (
    BirthDateNotFoundError,
    DocumentNotFoundError,
    FaceNotFoundError,
    FaceNotMatchError,
    IdentificationNotFoundError,
    LastNameNotFoundError,
    NameNotFoundError,
)
from .settings import (
    BIRTH_DATE_NOT_FOUND_ERROR,
    DOCUMENT_NOT_FOUND_ERROR,
    FACE_NOT_FOUND_ERROR,
    FACE_NOT_MATCH_ERROR,
    IDENTIFICATION_NOT_FOUND_ERROR,
    LAST_NAME_NOT_FOUND_ERROR,
    NAME_NOT_FOUND_ERROR,
)


class IDFace:

    def __init__(
        self,
        recognition_confidence_threshold: float = 0.8,
        extraction_ocr_model_gpu: bool = False,
        extraction_ocr_model_lang: str = "es",
        extraction_confidence_threshold: float = 0.8,
    ):
        self.face_comparison = FaceComparison()
        self.recognition = Recognition(
            confidence_threshold=recognition_confidence_threshold,
        )
        self.extract_information = ExtractInformation(
            ocr_model_gpu=extraction_ocr_model_gpu,
            ocr_model_lang=extraction_ocr_model_lang,
            confidence_threshold=extraction_confidence_threshold,
        )

    def execute(self, face_image_path: str, document_image_path: str):

        # Verificar si las imagenes existen
        if not Path(face_image_path).exists():
            return {
                "message": "Imagen de rostro no encontrada",
                "error": FACE_NOT_FOUND_ERROR,
            }

        if not Path(document_image_path).exists():
            return {
                "message": "Imagen de documento no encontrada",
                "error": DOCUMENT_NOT_FOUND_ERROR,
            }

        # Reconocer documento
        document_recognized = self.recognize(document_image_path)

        # Comparar rostro
        self.compare(document_image_path, face_image_path)

        # Extraer información
        document_information = self.extract(document_image_path)

        return {
            "document": document_recognized,
            "information": document_information,
        }

    def recognize(self, document_image_path: str):
        try:
            document_recognized = self.recognition.recognize(document_image_path)

        except DocumentNotFoundError:
            return {
                "message": "Documento no encontrado",
                "error": DOCUMENT_NOT_FOUND_ERROR,
            }

        except Exception as e:
            return {
                "message": "Error desconocido",
                "error": str(e),
            }

        return document_recognized

    def compare(self, document_image_path: str, face_image_path: str):
        try:
            face_comparision = self.face_comparison.compare(
                document_image_path, face_image_path
            )

        except FaceNotFoundError:
            return {
                "message": "Cara no encontrada",
                "error": FACE_NOT_FOUND_ERROR,
            }

        except FaceNotMatchError:
            return {
                "message": "Cara no coincide",
                "error": FACE_NOT_MATCH_ERROR,
            }

        except Exception as e:
            return {
                "message": "Error desconocido",
                "error": str(e),
            }

        return face_comparision

    def extract(self, document_image_path: str):
        try:
            document_information = self.extract_information.extract(document_image_path)

        except NameNotFoundError:
            return {
                "message": "Nombre no encontrado",
                "error": NAME_NOT_FOUND_ERROR,
            }

        except LastNameNotFoundError:
            return {
                "message": "Apellido no encontrado",
                "error": LAST_NAME_NOT_FOUND_ERROR,
            }

        except BirthDateNotFoundError:
            return {
                "message": "Fecha de nacimiento no encontrada",
                "error": BIRTH_DATE_NOT_FOUND_ERROR,
            }

        except IdentificationNotFoundError:
            return {
                "message": "Identificación no encontrada",
                "error": IDENTIFICATION_NOT_FOUND_ERROR,
            }

        except Exception as e:
            return {
                "message": "Error desconocido",
                "error": str(e),
            }

        return document_information
