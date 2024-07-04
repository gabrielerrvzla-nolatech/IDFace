from pathlib import Path

from .exceptions import FileNotFoundError
from .modules.extract_information import ExtractInformation
from .modules.face_comparison import FaceComparison
from .modules.recognition import Recognition


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
            raise FileNotFoundError

        if not Path(document_image_path).exists():
            raise FileNotFoundError

        # Reconocer documento
        document_recognized = self.recognize(document_image_path)

        # Comparar rostro
        self.compare(document_image_path, face_image_path)

        # Extraer información
        document_information = self.extract(document_image_path)

        return {"document": document_recognized, "information": document_information}

    def recognize(self, document_image_path: str):
        return self.recognition.recognize(document_image_path)

    def compare(self, document_image_path: str, face_image_path: str):
        return self.face_comparison.compare(document_image_path, face_image_path)

    def extract(self, document_image_path: str):
        return self.extract_information.extract(document_image_path)
