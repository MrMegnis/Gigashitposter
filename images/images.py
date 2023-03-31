import io
import logging
from PIL import Image
from io import BytesIO


def create_byte_image(bytes_):
    img = Image.open(BytesIO(bytes_))
    buf = io.BytesIO()
    # buf.write(bytes(bytes_))
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
