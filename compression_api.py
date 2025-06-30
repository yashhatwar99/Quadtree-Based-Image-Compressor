
import numpy as np
from PIL import Image
from image_compressor import ImageCompressor



def compress_and_encode_image_data(
        image_data: np.array,
        iterations: int = 20000,
        detail_error_threshold: float = 10) -> bytes:
    """Compress image data and return binary representation"""
    compressor = ImageCompressor(image_data)
    compressor.add_detail(iterations, detail_error_threshold)
    return compressor.encode_to_binary()


def compress_image_file(
        image_path: str,
        output_path: str,
        iterations: int = 20000,
        detail_error_threshold: float = 10):
    """Compress an image file and save to output path"""
    image = Image.open(image_path)
    image_data = np.array(image)

    data = compress_and_encode_image_data(image_data, iterations, detail_error_threshold)

    with open(output_path, "wb") as file:
        file.write(data)
