# 🖼️ QuadTree-Based Image Compression

This project implements an **image compression and reconstruction system** using **QuadTree decomposition** with additional **LZMA-based encoding**.  
It compresses images by recursively subdividing regions with high detail, encoding the structure and colors efficiently, and reconstructing them with minimal loss.

---

## ✨ Features
- ✅ **QuadTree Compression** – subdivides images based on detail level.  
- ✅ **Custom Binary Encoding** – efficiently stores subdivided flags and color data.  
- ✅ **LZMA Compression** – further compresses binary data for storage.  
- ✅ **Image Reconstruction** – restores compressed images to a near-original quality.  
- ✅ **Performance Benchmarking** – evaluates compression ratio and error metrics.  
- ✅ **Configurable Parameters** – set number of iterations and detail error threshold.  

---
## 📸 Example (Before vs After)

| Original Image        | Compressed & Reconstructed |
|----------------------|----------------------------|
| ![Original](input/download.jpg) | ![Reconstructed](output/rec_download.jpg) |



## 📂 Project Structure
```bash
├── compression_api.py # Functions for compressing image data/files
├── encoding.py # Encoding & decoding utilities (bitsets, LZMA, etc.)
├── image_compressor.py # Main compression logic using QuadTree nodes
├── main.py # Entry point – runs compression, reconstruction, benchmark
├── performance.py # Functions to benchmark compression & measure quality
├── quadtree_nodes.py # QuadTree, CompressNode & ReconstructNode classes
├── reconstruction_api.py # Functions to rebuild image from compressed data
├── input
├── output
└── README.md # Project documentation

```

---

## ⚡ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quadtree-image-compression.git
   cd quadtree-image-compression
2. Install required dependencies:
    ```bash
    pip install numpy pillow sortedcontainers scikit-image tabulate

## 🚀 Usage
### 1. Run the compression demo
```bash
python main.py


You’ll be prompted to enter the number of iterations (1000–50000).

Example input image is input/download.jpg (replace with your own).

Outputs:

Compressed file → output/compressed.qid

Reconstructed image → output/rec_download.jpg
```
### 2. Compress an image directly
```bash
from compression_api import compress_image_file

compress_image_file(
    image_path="input/myphoto.jpg",
    output_path="output/myphoto.qid",
    iterations=20000,
    detail_error_threshold=10
)
```

### 3. Reconstruct an image
```bash
from reconstruction_api import reconstruct_image_from_file

image = reconstruct_image_from_file("output/myphoto.qid")
image.save("output/restored.jpg")
```

## 📊 Performance Benchmark

The system reports:

Original vs Compressed size

Size reduction percentage

Image similarity metrics (MSE, RMSE, entropy, etc.)

Example output:
```bash
Image: download.jpg
Original size: 1,024,500 bytes
Compressed size: 210,345 bytes
Size reduced: 814,155 bytes
Size reduction: 79.45%
```
--------------------------------------------------

## ⚙️ Configuration

Iterations (1000–50000) – higher values improve quality but increase file size.

Detail Error Threshold – controls how much detail is preserved in each region.

## 🧠 How It Works

The image is represented as a QuadTree.

Regions with high detail (variance in color) are recursively subdivided.

Leaf nodes store average color values.

Data is serialized into a binary format with:

Subdivided flags

RGB values for leaf nodes

The binary blob is compressed with LZMA for storage.

During reconstruction, the binary data is decoded and the QuadTree is redrawn.
	
## 🛠️ Future Improvements

Implement adaptive thresholds per region.

Integrate GUI for interactive compression.

Support video compression using frame-wise QuadTree.

## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software with attribution.

## 👨‍💻 Author

Developed by Yash Hatwar,
IIT Ropar 