import cv2
import easyocr
import supervision as sv
from dateutil import parser
from ultralytics import YOLO

from IDFace.exceptions import (
    BirthDateNotFoundError,
    IdentificationNotFoundError,
    LastNameNotFoundError,
    NameNotFoundError,
)
from IDFace.settings import (
    BIRTH_DATE,
    CIVIL_STATUS,
    EXPEDITION_DATE,
    EXPIRATION_DATE,
    IDENTIFICATION,
    LAST_NAME,
    NAME,
    PHOTO,
)


class ExtractInformation:

    def __init__(
        self,
        extract_information_model_path: str,
        ocr_model_gpu: bool = False,
        ocr_model_lang: str = "es",
        confidence_threshold: float = 0.8,
    ):
        self.reader = easyocr.Reader([ocr_model_lang], gpu=ocr_model_gpu)
        self.extract_information_model = YOLO(model=extract_information_model_path)
        self.extract_information_model.fuse()
        self.confidence_threshold = confidence_threshold

    def extract(self, document_image) -> dict:
        # Obtener trozos de la imagen
        chunks = self.__get_chunks(document_image)

        response_obj = {}

        for chunk in chunks:
            class_id = chunk["data"]["class_id"]
            confidence = chunk["data"]["confidence"]
            cropped_image = self.__get_cropped_image(document_image, chunk)

            # Fecha de vencimiento
            if class_id == EXPIRATION_DATE and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[EXPIRATION_DATE] = {
                    "confidence": confidence,
                    "value": self.__get_date(value[0]),
                }

            # Numero de identicicacion
            if class_id == IDENTIFICATION and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[IDENTIFICATION] = {
                    "confidence": confidence,
                    "value": "".join(value)
                    .replace(".", "")
                    .replace(" ", "")
                    .replace("-", "")
                    .replace(",", "")
                    .replace(":", "")
                    .replace(";", ""),
                }

            # Fecha de expedicion
            if class_id == EXPEDITION_DATE and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[EXPEDITION_DATE] = {
                    "confidence": confidence,
                    "value": self.__get_date(value[0]),
                }

            # Estado civil
            if class_id == CIVIL_STATUS and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[CIVIL_STATUS] = {
                    "confidence": confidence,
                    "value": value[0],
                }

            # Nombres
            if class_id == NAME and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[NAME] = {
                    "confidence": confidence,
                    "value": " ".join(value),
                }

            # Apellidos
            if class_id == LAST_NAME and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[LAST_NAME] = {
                    "confidence": confidence,
                    "value": " ".join(value),
                }

            # Fecha de nacimiento
            if class_id == BIRTH_DATE and confidence >= self.confidence_threshold:
                value = self.__get_text(cropped_image)
                response_obj[BIRTH_DATE] = {
                    "confidence": confidence,
                    "value": self.__get_date(value[0]),
                }

            # Foto
            if class_id == PHOTO and confidence >= self.confidence_threshold:
                x, y, w, h = chunk["data"]["cropped_image"]
                response_obj[PHOTO] = {
                    "confidence": confidence,
                    "value": {"x": x, "y": y, "w": w, "h": h},
                }

        if IDENTIFICATION not in response_obj:
            raise IdentificationNotFoundError

        if BIRTH_DATE not in response_obj:
            raise BirthDateNotFoundError

        if NAME not in response_obj:
            raise NameNotFoundError

        if LAST_NAME not in response_obj:
            raise LastNameNotFoundError

        return response_obj

    def __get_chunks(self, image):
        prediction = self.extract_information_model.predict(image, verbose=False)

        detections = sv.Detections(
            xyxy=prediction[0].boxes.xyxy.cpu().numpy(),
            confidence=prediction[0].boxes.conf.cpu().numpy(),
            class_id=prediction[0].boxes.cls.cpu().numpy().astype(int),
        )

        return [
            {
                "data": {
                    "confidence": round(confidence, 2),
                    "cropped_image": xyxy,
                    "class_id": self.extract_information_model.names[class_id],
                }
            }
            for xyxy, confidence, class_id in zip(
                detections.xyxy, detections.confidence, detections.class_id
            )
        ]

    def __get_cropped_image(self, image, chunk):
        x, y, w, h = chunk["data"]["cropped_image"]
        int_x, int_y, int_w, int_h = int(x), int(y), int(w), int(h)
        return cv2.imread(image)[int_y:int_h, int_x:int_w]

    def __get_text(self, cropped_image):
        return self.reader.readtext(cropped_image, detail=0, paragraph=False)

    def __get_date(self, date_str):
        date = parser.parse(date_str, dayfirst=True, yearfirst=False)

        if date_str.count("/") == 1 or date_str.count("-") == 1:
            return date.strftime("%m/%Y")

        return date.strftime("%d/%m/%Y")
