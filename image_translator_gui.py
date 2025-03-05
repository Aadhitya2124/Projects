import os
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from PIL import Image, ImageTk
import threading
from gemini_image_translator import extract_and_translate
from gtts import gTTS
import tempfile
from playsound import playsound
import uuid

class ImageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Image Translator")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Create temp directory for audio files
        self.temp_dir = tempfile.gettempdir()
        self.current_audio_file = None
        
        # Available languages
        self.languages = [
            "English", "Spanish", "French", "German", "Italian", "Portuguese", 
            "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Hindi", 
            "Dutch", "Swedish", "Norwegian", "Finnish", "Danish", "Polish", 
            "Turkish", "Greek", "Hebrew", "Thai", "Vietnamese"
        ]
        
        # Language codes for TTS
        self.language_codes = {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de",
            "Italian": "it", "Portuguese": "pt", "Russian": "ru", "Japanese": "ja",
            "Chinese": "zh", "Korean": "ko", "Arabic": "ar", "Hindi": "hi",
            "Dutch": "nl", "Swedish": "sv", "Norwegian": "no", "Finnish": "fi",
            "Danish": "da", "Polish": "pl", "Turkish": "tr", "Greek": "el",
            "Hebrew": "he", "Thai": "th", "Vietnamese": "vi"
        }
        
        self.selected_image_path = None
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Gemini Image Translator", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # Image selection frame
        image_frame = tk.LabelFrame(
            main_frame, 
            text="Select Image", 
            font=("Arial", 12),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        image_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Image selection button
        self.select_button = tk.Button(
            image_frame,
            text="Browse...",
            command=self.select_image,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.select_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Selected image path display
        self.path_var = tk.StringVar()
        self.path_var.set("No image selected")
        path_label = tk.Label(
            image_frame,
            textvariable=self.path_var,
            font=("Arial", 10),
            bg="#f0f0f0",
            anchor="w"
        )
        path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Language selection frame
        lang_frame = tk.LabelFrame(
            main_frame,
            text="Target Language",
            font=("Arial", 12),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        lang_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Language dropdown
        self.language_var = tk.StringVar()
        self.language_var.set(self.languages[0])  # Default to English
        language_dropdown = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=self.languages,
            font=("Arial", 10),
            state="readonly",
            width=20
        )
        language_dropdown.pack(side=tk.LEFT)
        
        # Image preview frame
        preview_frame = tk.LabelFrame(
            main_frame,
            text="Image Preview",
            font=("Arial", 12),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Image preview label
        self.preview_label = tk.Label(
            preview_frame,
            text="Image preview will appear here",
            bg="#e0e0e0",
            font=("Arial", 10),
            width=80,
            height=10
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Results frame
        results_frame = tk.LabelFrame(
            main_frame,
            text="Translation Results",
            font=("Arial", 12),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            height=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(pady=(0, 10))
        
        # Process button
        self.process_button = tk.Button(
            buttons_frame,
            text="Process Image",
            command=self.process_image,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        # Read Aloud button
        self.read_button = tk.Button(
            buttons_frame,
            text="Read Aloud",
            command=self.read_translation_aloud,
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.read_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 10, "italic"),
            bg="#f0f0f0",
            fg="#555555"
        )
        status_label.pack()
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.path_var.set(file_path)
            self.process_button.config(state=tk.NORMAL)
            self.display_image_preview(file_path)
    
    def display_image_preview(self, image_path):
        try:
            # Open and resize image for preview
            img = Image.open(image_path)
            
            # Calculate new dimensions while maintaining aspect ratio
            width, height = img.size
            max_width = 400
            max_height = 300
            
            # Resize to fit within the preview area
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for display
            photo = ImageTk.PhotoImage(img)
            
            # Update preview label
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference to prevent garbage collection
            
        except Exception as e:
            self.preview_label.config(text=f"Error loading image: {str(e)}")
    
    def process_image(self):
        if not self.selected_image_path:
            return
        
        # Disable the process button and update status
        self.process_button.config(state=tk.DISABLED)
        self.status_var.set("Processing... Please wait.")
        self.root.update()
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Process in a separate thread to keep UI responsive
        threading.Thread(target=self._process_image_thread).start()
    
    def _process_image_thread(self):
        try:
            target_language = self.language_var.get()
            
            # Call the translation function
            result = extract_and_translate(self.selected_image_path, target_language)
            
            # Update the UI with results (must be done in the main thread)
            self.root.after(0, self._update_results, result)
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.root.after(0, self._show_error, error_message)
    
    def _update_results(self, result):
        # Display results in the text area
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "--- Original Text ---\n")
        self.results_text.insert(tk.END, result["original_text"] + "\n\n")
        
        self.results_text.insert(tk.END, "--- Translated Text ---\n")
        self.results_text.insert(tk.END, result["translated_text"])
        
        # Re-enable the process button and enable read button
        self.process_button.config(state=tk.NORMAL)
        self.read_button.config(state=tk.NORMAL)
        self.status_var.set("Processing complete!")
    
    def _show_error(self, error_message):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, error_message)
        
        # Re-enable the process button and update status
        self.process_button.config(state=tk.NORMAL)
        self.status_var.set("Error occurred during processing")
    
    def read_translation_aloud(self):
        try:
            # Get the translated text
            text_content = self.results_text.get(1.0, tk.END)
            translated_text = text_content.split("--- Translated Text ---\n")[1].strip()
            
            if not translated_text:
                self.status_var.set("No translated text to read")
                return
            
            # Disable the read button and update status
            self.read_button.config(state=tk.DISABLED)
            self.status_var.set("Generating speech...")
            self.root.update()
            
            # Get the language code for TTS
            target_language = self.language_var.get()
            lang_code = self.language_codes.get(target_language, 'en')
            
            # Clean up previous audio file if it exists
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                try:
                    os.remove(self.current_audio_file)
                except:
                    pass
            
            # Generate a unique filename for the audio
            audio_file = os.path.join(self.temp_dir, f"translation_{uuid.uuid4()}.mp3")
            self.current_audio_file = audio_file
            
            # Create and save the audio file
            tts = gTTS(text=translated_text, lang=lang_code, slow=False)
            tts.save(audio_file)
            
            # Update status
            self.status_var.set("Playing translation...")
            
            # Play the audio in a separate thread
            threading.Thread(target=self._play_audio, args=(audio_file,)).start()
            
        except Exception as e:
            self.status_var.set(f"Error reading text: {str(e)}")
            self.read_button.config(state=tk.NORMAL)
    
    def _play_audio(self, audio_file):
        try:
            playsound(audio_file)
            
            # Update UI after playback (in main thread)
            self.root.after(0, self._after_playback)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error playing audio: {str(e)}"))
            self.root.after(0, lambda: self.read_button.config(state=tk.NORMAL))
    
    def _after_playback(self):
        self.status_var.set("Ready")
        self.read_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTranslatorApp(root)
    root.mainloop() 