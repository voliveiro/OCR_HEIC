import pyheif
from PIL import Image
import pytesseract
import os

# Convert HEIC image to a format compatible with OCR (like JPEG)
def convert_heic_to_image(heic_path, output_image_path):
    # Read HEIC file
    heif_file = pyheif.read(heic_path)
    
    # Convert to a PIL Image object
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    
    # Save the image in JPEG format
    image.save(output_image_path, "JPEG")
    return output_image_path

# Perform OCR on the image
def perform_ocr(image_path):
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Process all HEIC files in a folder, sorted by filename
def process_heic_files_in_folder(folder_path, output_text_file):
    # Get a sorted list of all HEIC files in the directory
    heic_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".heic")])
    
    # Create/overwrite the output file
    with open(output_text_file, "w") as output_file:
        # Loop through each sorted HEIC file
        for filename in heic_files:
            heic_path = os.path.join(folder_path, filename)
            
            # Temporary image file for the converted image
            temp_image_path = "temp_image.jpg"
            
            try:
                # Convert HEIC to JPEG
                convert_heic_to_image(heic_path, temp_image_path)
                
                # Perform OCR
                ocr_text = perform_ocr(temp_image_path)
                
                # Write the filename and the extracted text to the output file
                output_file.write(f"File: {filename}\n")
                output_file.write(ocr_text)
                output_file.write("\n\n")  # Add some spacing between files

                print(f"Processed {filename}")
            
            finally:
                # Clean up temporary image file
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)

# Example usage
folder_path = "."  # Folder containing HEIC files
output_text_file = "output_text.txt"  # Output combined .txt file

process_heic_files_in_folder(folder_path, output_text_file)
