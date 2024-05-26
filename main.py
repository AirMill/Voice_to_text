import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import speech_recognition as sr

class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=10)
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)

        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(self.main_frame, text="Press 'Start' and speak into the microphone")
        self.label.pack(pady=10)

        self.text_area = tk.Text(self.main_frame, height=10, width=50, wrap=tk.WORD, font=('Helvetica', 12))
        self.text_area.pack(pady=10)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_recognition)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.recognizer = sr.Recognizer()

    def start_recognition(self):
        with sr.Microphone() as source:
            self.label.config(text="Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, text + "\n")
                self.label.config(text="Press 'Start' and speak into the microphone")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Google Web Speech API could not understand the audio")
                self.label.config(text="Press 'Start' and speak into the microphone")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results from Google Web Speech API; {e}")
                self.label.config(text="Press 'Start' and speak into the microphone")

    def save_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file; {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
