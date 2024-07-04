from deepface import DeepFace

from IDFace.exceptions import FaceNotFoundError, FaceNotMatchError


class FaceComparison:

    def __init__(self):
        self.deepface = DeepFace

    def compare(self, document_image_path: str, face_image_path: str):
        try:
            prediction = self.deepface.verify(document_image_path, face_image_path)
            match = prediction["verified"]

            if not match:
                raise FaceNotMatchError

            return match

        except ValueError:
            raise FaceNotFoundError

        except Exception as e:
            raise e
