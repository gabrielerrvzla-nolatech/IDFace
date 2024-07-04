from setuptools import setup, find_packages

setup(
    name="IDFace",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "ultralytics==8.2.48",
        "supervision==0.21.0",
        "easyocr==1.7.1",
        "deepface==0.0.92",
        "tf-keras==2.16.0",
        "python-dateutil==2.9.0.post0",
    ],
    author="Nolatech - Gabriel Rueda @gabrielerrvzla",
    author_email="gabrielr@nolatech.ai - gabrielrueda95@gmail.com",
    description="Librería para verificación KYC de cédulas venezolanas, incluyendo validación de documento, verificación facial y extracción de datos.",
    long_description="Librería diseñada para integrar un proceso de Conozca a su Cliente (KYC) específico para cédulas venezolanas. Permite verificar la autenticidad del documento, comparar la imagen facial con la fotografía de la cédula y extraer información del documento de identidad.",
    long_description_content_type="text/plain",
    url="https://github.com/tu_usuario/venezuelan-kyc",
    classifiers=[
        "Private :: Do Not Upload",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
