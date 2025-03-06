import os
import google.generativeai as genai
from PIL import Image
import argparse

# Configure your API key
# Using the provided API key directly
API_KEY = " Google API key here"

# Configure the Gemini API
genai.configure(api_key=API_KEY)

def extract_and_translate(image_path, target_language):
    """
    Extract text from an image and translate it to the target language using Gemini 1.5 Pro.
    
    Args:
        image_path (str): Path to the image file
        target_language (str): Target language for translation (e.g., 'Spanish', 'French', 'German')
    
    Returns:
        dict: A dictionary containing the original text and translated text
    """
    try:
        # Load the image
        image = Image.open(image_path)
        
        # Initialize Gemini 1.5 Pro model (most advanced version currently available)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create a prompt for text extraction and translation
        prompt = f"""
        Please perform the following tasks with high accuracy:
        1. Extract all text from the provided image, maintaining the original formatting and structure.
        2. Translate the extracted text to {target_language}, preserving the meaning and context.
        
        Return the results in the following format:
        Original Text: [extracted text]
        Translated Text: [translated text]
        
        Note: Please maintain any special characters, numbers, or formatting in the original text.
        """
        
        # Generate content with the image
        response = model.generate_content([prompt, image])
        
        # Parse the response to extract original and translated text
        response_text = response.text
        
        # Simple parsing of the response
        lines = response_text.strip().split('\n')
        original_text = ""
        translated_text = ""
        
        original_started = False
        translated_started = False
        
        for line in lines:
            if "Original Text:" in line:
                original_started = True
                original_text = line.replace("Original Text:", "").strip()
                continue
            elif "Translated Text:" in line:
                translated_started = True
                translated_text = line.replace("Translated Text:", "").strip()
                continue
            
            if original_started and not translated_started:
                original_text += " " + line.strip()
            elif translated_started:
                translated_text += " " + line.strip()
        
        return {
            "original_text": original_text.strip(),
            "translated_text": translated_text.strip()
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "original_text": "",
            "translated_text": f"Error processing image: {str(e)}"
        }

def main():
    parser = argparse.ArgumentParser(description='Extract text from an image and translate it using Gemini 1.5 Pro')
    parser.add_argument('--image', required=True, help='Path to the image file')
    parser.add_argument('--language', required=True, help='Target language for translation')
    
    args = parser.parse_args()
    
    result = extract_and_translate(args.image, args.language)
    
    print("\n--- Original Text ---")
    print(result["original_text"])
    print("\n--- Translated Text ---")
    print(result["translated_text"])

if __name__ == "__main__":
    main() 
