
from compression_api import compress_image_file
from reconstruction_api import reconstruct_image_from_file
from performance import benchmark_image


def get_iterations_from_user():
    """Get iteration count from user with validation"""
    print("Iteration range: 1000 - 50000")
    print("Recommended: 10000-20000 for good quality")
    
    while True:
        try:
            iterations = int(input("Enter number of iterations: "))
            if 1000 <= iterations <= 50000:
                return iterations
            else:
                print("Please enter a value between 1000 and 50000")
        except ValueError:
            print("Please enter a valid integer")


def main():
    """Demo of the quad tree compression system"""
    
    # Get iterations from user
    iterations = get_iterations_from_user()
    
    # Example: Compress an image
    input_image = "input/download.jpg"  # Replace with your image path
    compressed_file = "output/compressed.qid"
    reconstructed_file = "output/rec_download.jpg"
    
    try:
        # Compress the image
        print(f"\nCompressing image with {iterations} iterations...")
        compress_image_file(input_image, compressed_file, iterations=iterations)
        print(f"Image compressed and saved to {compressed_file}")
        
        # Reconstruct the image
        print("Reconstructing image...")
        reconstructed_image = reconstruct_image_from_file(compressed_file)
        reconstructed_image.save(reconstructed_file)
        print(f"Image reconstructed and saved to {reconstructed_file}")
        
        # Run benchmark
        print("\nRunning performance...")
        benchmark_image(input_image, iterations, compressed_file)
        
    except FileNotFoundError:
        print(f"Image file {input_image} not found. Please provide a valid image path.")
        print("You can test with any image by updating the input_image variable.")


if __name__ == "__main__":
    main()
