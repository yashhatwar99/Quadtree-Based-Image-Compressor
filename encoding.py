
import math
import lzma
from io import BytesIO


def encode_uint32(number: int) -> bytes:
    return number.to_bytes(4, byteorder="little", signed=False)


def decode_uint32(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=False)


def encode_uint8(number: int) -> bytes:
    return number.to_bytes(1, byteorder="little", signed=False)


def decode_uint8(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=False)


def encode_bitset(boolean_flags: list, stream: BytesIO):
    # Encode the number of booleans
    stream.write(encode_uint32(len(boolean_flags)))

    # Encode the booleans
    byte_count = math.ceil(len(boolean_flags) / 8)
    for byte_index in range(byte_count):
        byte = 0

        for bit_index in range(8):
            list_index = byte_index * 8 + bit_index
            if list_index >= len(boolean_flags) or not boolean_flags[list_index]:
                continue
            # Fill the byte from left to right
            byte |= 1 << bit_index

        stream.write(encode_uint8(byte))


def decode_bitset(stream: BytesIO) -> list:
    flag_count = decode_uint32(stream.read(4))
    boolean_flags = []

    byte_count = math.ceil(flag_count / 8)
    for byte_index in range(byte_count):
        byte = decode_uint8(stream.read(1))

        for bit_index in range(8):
            list_index = byte_index * 8 + bit_index
            if list_index >= flag_count:
                continue

            boolean_flags.append((byte & (1 << bit_index)) > 0)

    return boolean_flags


def encode_image_data(width: int, height: int, subdivided_flags: list, colors: list) -> bytes:
    stream = BytesIO()
    
    # Encode the image dimensions
    stream.write(encode_uint32(width))
    stream.write(encode_uint32(height))

    # Encode the is_subdivided flags
    encode_bitset(subdivided_flags, stream)

    # Encode the colors
    for color in colors:
        r, g, b = color
        stream.write(encode_uint8(r))
        stream.write(encode_uint8(g))
        stream.write(encode_uint8(b))

    blob = stream.getvalue()
    return lzma.compress(blob)


def decode_image_data(compressed: bytes) -> tuple:
    stream = BytesIO(lzma.decompress(compressed))

    width = decode_uint32(stream.read(4))
    height = decode_uint32(stream.read(4))

    subdivided_flags = decode_bitset(stream)

    # Only the leaf nodes (nodes that are not subdivided => flag is False) can draw a color
    color_count = sum(0 if flag else 1 for flag in subdivided_flags)
    colors = []

    for i in range(color_count):
        r = decode_uint8(stream.read(1))
        g = decode_uint8(stream.read(1))
        b = decode_uint8(stream.read(1))
        colors.append((r, g, b))

    return width, height, subdivided_flags, colors
