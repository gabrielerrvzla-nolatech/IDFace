import supervision as sv
from ultralytics import YOLO

from IDFace.exceptions import DocumentNotFoundError
from IDFace.settings import VENEZUELA_ID


class Recognition:

    def __init__(
        self,
        recognition_model_path: str,
        confidence_threshold: float = 0.8,
    ):
        self.confidence_threshold = confidence_threshold
        self.recognition_model = YOLO(model=recognition_model_path)
        self.recognition_model.fuse()

    def recognize(self, image_path: str) -> dict:
        prediction = self.recognition_model.predict(image_path, verbose=False)

        detections = sv.Detections(
            xyxy=prediction[0].boxes.xyxy.cpu().numpy(),
            confidence=prediction[0].boxes.conf.cpu().numpy(),
            class_id=prediction[0].boxes.cls.cpu().numpy().astype(int),
        )

        response = [
            {
                "data": {
                    "confidence": round(confidence, 2),
                    "cropped_image": xyxy,
                    "class_id": self.recognition_model.names[class_id],
                }
            }
            for xyxy, confidence, class_id in zip(
                detections.xyxy, detections.confidence, detections.class_id
            )
        ]

        if len(response) == 0:
            raise DocumentNotFoundError

        if len(response) > 1:
            response = sorted(
                response,
                key=lambda x: x["data"]["confidence"],
                reverse=True,
            )
            response = response[:1]

        response = response[0]["data"]

        # @TODO: Remover cuando se tenga un modelo que reconozca cédulas de otros países
        if not VENEZUELA_ID in response["class_id"]:
            raise DocumentNotFoundError

        if response["confidence"] < self.confidence_threshold:
            raise DocumentNotFoundError

        x, y, w, h = response["cropped_image"]

        return {
            "class_id": response["class_id"],
            "confidence": response["confidence"],
            "value": {"x": x, "y": y, "w": w, "h": h},
        }
