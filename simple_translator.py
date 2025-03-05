import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import google.generativeai as genai
from gtts import gTTS
import os
import threading
from playsound import playsound

# Configure API
API_KEY = "AIzaSyCfGoJk0S2QS84mocHI6n1sESUYV_YQIXk"
genai.configure(api_key=API_KEY)

class SimpleTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Translator")
        self.root.geometry("800x600")
        
        # Language codes for TTS
        self.language_codes = {
            "English": "en", "Spanish": "es", "French": "fr",
            "German": "de", "Italian": "it", "Japanese": "ja",
            "Chinese": "zh", "Korean": "ko"
        }
        
        self.languages = list(self.language_codes.keys())
        self.setup_ui()
        
    def setup_ui(self):
        # Select image button
        self.select_btn = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_btn.pack(pady=10)
        
        # Language dropdown
        self.lang_var = tk.StringVar(value="English")
        self.lang_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.lang_var,
            values=self.languages,
            state="readonly"
        )
        self.lang_dropdown.pack(pady=5)
        
        # Process button
        self.process_btn = tk.Button(
            self.root, 
            text="Process Image",
            command=self.process_image,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=5)
        
        # Read aloud button
        self.read_btn = tk.Button(
            self.root,
            text="Read Aloud",
            command=self.read_text,
            state=tk.DISABLED
        )
        self.read_btn.pack(pady=5)
        
        # Results text
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(pady=10, padx=10, expand=True, fill='both')
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.process_btn.config(state=tk.NORMAL)
            self.status_var.set("Image selected")
            
    def process_image(self):
        self.status_var.set("Processing...")
        self.process_btn.config(state=tk.DISABLED)
        self.read_btn.config(state=tk.DISABLED)
        
        def process():
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                image = Image.open(self.image_path)
                
                prompt = f"""
                Please perform these tasks:
                1. Extract all text from the provided image
                2. Translate the text to {self.lang_var.get()}
                
                Format:
                Original Text: [extracted text]
                Translated Text: [translated text]
                """
                
                response = model.generate_content([prompt, image])
                self.root.after(0, self.update_results, response.text)
                
            except Exception as e:
                self.root.after(0, self.show_error, str(e))
        
        threading.Thread(target=process).start()
        
    def update_results(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.process_btn.config(state=tk.NORMAL)
        self.read_btn.config(state=tk.NORMAL)
        self.status_var.set("Processing complete")
        
    def show_error(self, error):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Error: {error}")
        self.process_btn.config(state=tk.NORMAL)
        self.status_var.set("Error occurred")
        
    def read_text(self):
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            return
            
        try:
            # Extract translated text
            translated_text = text.split("Translated Text:")[1].strip()
            
            # Get language code
            lang_code = self.language_codes.get(self.lang_var.get(), 'en')
            
            # Create and play audio
            self.status_var.set("Generating speech...")
            self.read_btn.config(state=tk.DISABLED)
            
            def speak():
                try:
                    tts = gTTS(text=translated_text, lang=lang_code)
                    temp_file = "temp_speech.mp3"
                    tts.save(temp_file)
                    
                    self.root.after(0, lambda: self.status_var.set("Playing..."))
                    playsound(temp_file)
                    
                    # Cleanup
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    self.root.after(0, self.finish_reading)
                    
                except Exception as e:
                    self.root.after(0, self.show_error, f"Speech error: {str(e)}")
                    self.root.after(0, lambda: self.read_btn.config(state=tk.NORMAL))
            
            threading.Thread(target=speak).start()
            
        except Exception as e:
            self.show_error(f"Error preparing speech: {str(e)}")
            self.read_btn.config(state=tk.NORMAL)
            
    def finish_reading(self):
        self.status_var.set("Ready")
        self.read_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTranslatorApp(root)
    root.mainloop() 