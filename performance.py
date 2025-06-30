# Path Handling
from pathlib import Path

# Entropy calculation
from skimage.filters.rank import entropy as sk_entropy
from skimage.morphology import disk as sk_disk
from skimage.exposure import histogram as sk_histogram
from skimage.color import rgb2gray

# Image processing and maths
import numpy as np
import math
from PIL import Image

# "Virtual files" for estimating size of the images
from io import BytesIO

# String formatting
from tabulate import tabulate

import os
from compression_api import compress_and_encode_image_data


def get_image_file_size(image: Image, format: str = "png"):
    stream = BytesIO()
    image.save(stream, format, quality=90)
    return len(stream.getvalue())


def mean_squared_error(image_a: np.array, image_b: np.array) -> float:
    image_a = image_a.astype(np.single)
    image_b = image_b.astype(np.single)

    mse_per_channel = np.mean((image_a - image_b) ** 2, axis=(0, 1))
    mse = np.sum(mse_per_channel) / 3
    return float(mse)


def root_mean_squared_error(image_a: np.array, image_b: np.array) -> float:
    return math.sqrt(mean_squared_error(image_a, image_b))


def mean_average_error(image_a: np.array, image_b: np.array) -> float:
    image_a = image_a.astype(np.single)
    image_b = image_b.astype(np.single)
    mae_per_channel = np.mean(np.abs(image_a - image_b), axis=(0, 1))
    mae = np.sum(mae_per_channel) / 3
    return float(mae)


def compute_image_similarity(image_a: np.array, image_b: np.array) -> float:
    return 1 - mean_average_error(image_a, image_b) / 255


def compute_mean_local_entropy(image: np.array, radius=5) -> float:
    gray = (rgb2gray(image) * 255).astype(np.uint8)
    local_entropy = sk_entropy(gray, sk_disk(radius))
    entropy = np.mean(local_entropy)
    return float(entropy)


def compute_channel_histogram_entropy(image_channel: np.array) -> float:
    histogram, _ = sk_histogram(image_channel, nbins=256, source_range="dtype")
    relative_occurrence = histogram / histogram.sum()
    return -(relative_occurrence * np.ma.log2(relative_occurrence)).sum()


def compute_histogram_entropy(image: np.array) -> float:
    return (compute_channel_histogram_entropy(image[:, :, 0])
            + compute_channel_histogram_entropy(image[:, :, 1])
            + compute_channel_histogram_entropy(image[:, :, 2])) / 3


def benchmark_image(image_path: str, iterations: int, output_path: str):
    """Simple compression benchmark that shows size reduction"""

    # Load image
    image = Image.open(image_path)
    image_data = np.array(image)

    # Get original file size
    original_size = os.path.getsize(image_path)

    # Compress image
    compressed_data = compress_and_encode_image_data(image_data, iterations)

    # Save compressed file
    with open(output_path, "wb") as f:
        f.write(compressed_data)

    # Calculate metrics
    compressed_size = len(compressed_data)
    size_reduction = original_size - compressed_size
    size_reduction_percent = (size_reduction / original_size) * 100

    # Print results
    image_name = Path(image_path).name
    print(f"Image: {image_name}")
    print(f"Original size: {original_size:,} bytes")
    print(f"Compressed size: {compressed_size:,} bytes")
    print(f"Size reduced: {size_reduction:,} bytes")
    print(f"Size reduction: {size_reduction_percent:.2f}%")
    print("-" * 50)

# TODO: Add totally empty image to the examples