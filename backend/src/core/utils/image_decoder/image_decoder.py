import os
import base64
from PIL import Image
from io import BytesIO
from typing import List
from uuid import uuid4

class ImageDecoder:
    def __init__(self, api_uri_prefix: str, storage_prefix_path):
        self.api_uri_prefix = api_uri_prefix
        self.storage_prefix_path = storage_prefix_path

    def decode_base64(self, base64_string: str) -> bytes:
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]

        return base64.b64decode(base64_string)

    def save_image(self, image_bytes: bytes, path: str) -> str:

        image = Image.open(BytesIO(image_bytes))

        image.save(path)

        return os.path.join(self.api_uri_prefix, path)

    def decode_and_save_image(self, base64_string: str, img_id: int = 1) -> str:
        image_bytes = self.decode_base64(base64_string)
        path = os.path.join(self.storage_prefix_path, str(uuid4()), f"{img_id}.png")
        return self.save_image(image_bytes, path)

    def decode_and_save_images(self, base64_strings: List[str], img_id: str = 1) -> List[str]:
        saved_image_paths = []
        for base64_string in base64_strings:
            image_bytes = self.decode_base64(base64_string)
            path = os.path.join(self.storage_prefix_path, str(uuid4()), f"{img_id}.png")
            img_id += 1
            saved_image_paths.append(self.save_image(image_bytes, path))
        return saved_image_paths
