import io
import math

import requests
from PIL import Image

TELEGRAPH_URL = 'https://telegra.ph'

session = requests.Session()


def get_file_bytes(file_url: str):
    resp = session.get(file_url)
    return io.BytesIO(resp.content)


def get_image(file_url: str):
    return Image.open(get_file_bytes(file_url))


class PhotoEditor:
    def __init__(self, photo: Image.Image):
        self._photo = photo

    @classmethod
    def open(cls, file_url: str):
        return PhotoEditor(get_image(file_url))

    def crop(self, min_ratio: int | float):
        image = self._photo
        ratio = image.width / image.height

        if ratio >= min_ratio:
            return self

        new_height = image.width / min_ratio
        crop_sides_by = math.ceil((image.height - new_height) // 2)
        new_box = 0, crop_sides_by, image.width, image.height - crop_sides_by
        return PhotoEditor(image.crop(new_box))

    def _get_bytes(self) -> bytes:
        fp = io.BytesIO()
        self._photo.save(fp, 'JPEG')
        return fp.getvalue()

    def upload(self) -> str:
        """ Upload photo to telegraph, return new url """
        files = {'1': self._get_bytes()}

        resp = session.post(f'{TELEGRAPH_URL}/upload', files=files)
        result: dict = resp.json()
        src = result[0]['src']

        return TELEGRAPH_URL + src
