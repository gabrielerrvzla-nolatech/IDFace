from .settings import (
    BIRTH_DATE_NOT_FOUND_ERROR,
    DOCUMENT_NOT_FOUND_ERROR,
    FACE_NOT_FOUND_ERROR,
    FACE_NOT_MATCH_ERROR,
    FILE_NOT_FOUND_ERROR,
    IDENTIFICATION_NOT_FOUND_ERROR,
    LAST_NAME_NOT_FOUND_ERROR,
    NAME_NOT_FOUND_ERROR,
)


class FileNotFoundError(Exception):

    def __init__(self, message: str = FILE_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class DocumentNotFoundError(Exception):
    def __init__(self, message: str = DOCUMENT_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class FaceNotFoundError(Exception):
    def __init__(self, message: str = FACE_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class FaceNotMatchError(Exception):
    def __init__(self, message: str = FACE_NOT_MATCH_ERROR):
        self.message = message
        super().__init__(self.message)


class IdentificationNotFoundError(Exception):
    def __init__(self, message: str = IDENTIFICATION_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class BirthDateNotFoundError(Exception):
    def __init__(self, message: str = BIRTH_DATE_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class NameNotFoundError(Exception):
    def __init__(self, message: str = NAME_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)


class LastNameNotFoundError(Exception):
    def __init__(self, message: str = LAST_NAME_NOT_FOUND_ERROR):
        self.message = message
        super().__init__(self.message)
