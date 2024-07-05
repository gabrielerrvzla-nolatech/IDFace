from pathlib import Path

from .exceptions import FileNotFoundError
from .modules.extract_information import ExtractInformation
from .modules.face_comparison import FaceComparison
from .modules.recognition import Recognition


class IDFace:

    def __init__(
        self,
        recognition_model_path: str,
        extract_information_model_path: str,
        recognition_confidence_threshold: float = 0.8,
        extraction_ocr_model_gpu: bool = False,
        extraction_ocr_model_lang: str = "es",
        extraction_confidence_threshold: float = 0.8,
    ):
        self.face_comparison = FaceComparison()

        if not Path(recognition_model_path).exists():
            raise FileNotFoundError(recognition_model_path)

        self.recognition = Recognition(
            recognition_model_path=recognition_model_path,
            confidence_threshold=recognition_confidence_threshold,
        )

        if not Path(extract_information_model_path).exists():
            raise FileNotFoundError(extract_information_model_path)

        self.extract_information = ExtractInformation(
            extract_information_model_path=extract_information_model_path,
            ocr_model_gpu=extraction_ocr_model_gpu,
            ocr_model_lang=extraction_ocr_model_lang,
            confidence_threshold=extraction_confidence_threshold,
        )

    def execute(self, face_image_path: str, document_image_path: str):
        if not Path(face_image_path).exists():
            raise FileNotFoundError(face_image_path)

        if not Path(document_image_path).exists():
            raise FileNotFoundError(document_image_path)

        document_recognized = self.recognize(document_image_path)
        self.compare(document_image_path, face_image_path)
        document_information = self.extract(document_image_path)

        return {"document": document_recognized, "information": document_information}

    def recognize(self, document_image_path: str):
        return self.recognition.recognize(document_image_path)

    def compare(self, document_image_path: str, face_image_path: str):
        return self.face_comparison.compare(document_image_path, face_image_path)

    def extract(self, document_image_path: str):
        return self.extract_information.extract(document_image_path)
