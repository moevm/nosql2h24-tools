import hashlib
import os
import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from typing import List
from uuid import uuid4
from binascii import Error as BinAsciiError
from src.core.exceptions.client_error import InvalidBase64Error
from src.core.exceptions.server_error import DirectoryCreationError, ImageProcessingError


class ImageDecoder:
    def __init__(self, api_uri_prefix: str, storage_prefix_path):
        self.api_uri_prefix = api_uri_prefix
        self.storage_prefix_path = storage_prefix_path

    def decode_base64(self, base64_string: str) -> bytes:
        try:
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]

            return base64.b64decode(base64_string)
        except (BinAsciiError, ValueError, Exception):
            raise InvalidBase64Error(message="Failed to decode Base64 string", details={"base64_string": base64_string})

    def save_image(self, image_bytes: bytes, path: str) -> str:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except OSError:
            raise DirectoryCreationError("Failed to process image")

        try:
            image = Image.open(BytesIO(image_bytes))
            image.save(path)

            return os.path.join(self.api_uri_prefix, path)
        except (UnidentifiedImageError, OSError, IOError):
            raise ImageProcessingError("Failed to process image")

    def get_hashed_directory(self, identifier: str):
        hash_obj = hashlib.sha256(identifier.encode())
        hex_hash = hash_obj.hexdigest()
        return hex_hash

    def decode_and_save_image(self, base64_string: str, identifier: str, img_id: int = 1) -> str:
        image_bytes = self.decode_base64(base64_string)
        path = os.path.join(self.storage_prefix_path, str(self.get_hashed_directory(identifier)), f"{img_id}.png")
        return self.save_image(image_bytes, path)

    def decode_and_save_images(self, base64_strings: List[str], identifier: str, img_id: str = 1) -> List[str]:
        saved_image_paths = []
        for base64_string in base64_strings:
            image_bytes = self.decode_base64(base64_string)
            path = os.path.join(self.storage_prefix_path, str(self.get_hashed_directory(identifier)), f"{img_id}.png")
            img_id += 1
            saved_image_paths.append(self.save_image(image_bytes, path))
        return saved_image_paths
