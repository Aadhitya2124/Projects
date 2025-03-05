import os
import traceback
from gemini_image_translator import extract_and_translate

# Hardcoded image path and target language
IMAGE_PATH = r"C:\Users\bvtaa\OneDrive\Desktop\hf\testimg\img1.4.jpg"
TARGET_LANGUAGE = "English"  # You can change this to any language

def main():
    try:
        print(f"Processing image: {IMAGE_PATH}")
        print(f"Target language: {TARGET_LANGUAGE}")
        
        # Check if the image file exists
        if not os.path.exists(IMAGE_PATH):
            print(f"ERROR: Image file not found at path: {IMAGE_PATH}")
            return
            
        print("Image file exists, proceeding with processing...")
        
        result = extract_and_translate(IMAGE_PATH, TARGET_LANGUAGE)
        
        print("\n--- Original Text ---")
        print(result["original_text"])
        print("\n--- Translated Text ---")
        print(result["translated_text"])
        
    except Exception as e:
        print(f"ERROR: An exception occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("Script execution completed.") 