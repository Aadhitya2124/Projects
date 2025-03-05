# Gemini Image Translator

This tool uses Google's Gemini 1.5 Pro model to extract text from images and translate it to a target language. The model provides enhanced accuracy in text extraction and translation while maintaining formatting and context.

## Prerequisites

- Python 3.7+
- Google API key for Gemini models

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your Google API key:
   ```
   # On Windows
   set GOOGLE_API_KEY=your_api_key_here
   
   # On Linux/Mac
   export GOOGLE_API_KEY=your_api_key_here
   ```

   Alternatively, you can modify the script to directly include your API key (not recommended for shared code).

## Usage

### GUI Interface
Run the graphical interface for an easy-to-use experience:
```
python image_translator_gui.py
```

### Command Line Interface
Run the script with the following command:
```
python gemini_image_translator.py --image path/to/your/image.jpg --language "Spanish"
```

### Parameters

- `--image`: Path to the image file containing text you want to extract and translate
- `--language`: Target language for translation (e.g., "Spanish", "French", "German", "Japanese", etc.)

### Example

```
python gemini_image_translator.py --image sample_image.jpg --language "French"
```

## Features

- Advanced text extraction using Gemini 1.5 Pro
- Maintains original text formatting and structure
- Preserves special characters and numbers
- User-friendly GUI interface
- Support for multiple languages
- Real-time image preview
- Progress tracking

## Output

The script will output:
1. The original text extracted from the image
2. The translated text in the target language

## Notes

- The quality of text extraction depends on the clarity of the image
- For best results, use clear images with good contrast between text and background
- The Gemini 1.5 Pro model provides enhanced accuracy for both text extraction and translation
- Special characters, numbers, and formatting are preserved in the translation 