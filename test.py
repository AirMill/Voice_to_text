import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import speech_recognition as sr
import threading

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

        self.pause_button = ttk.Button(self.button_frame, text="Pause", state=tk.DISABLED, command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.is_paused = False

        # Blinking dot
        self.dot_canvas = tk.Canvas(self.main_frame, width=20, height=20)
        self.dot_canvas.pack(pady=5)
        self.dot = self.dot_canvas.create_oval(5, 5, 15, 15, fill='white')

    def start_recognition(self):
        self.is_recording = True
        self.is_paused = False
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.blink_dot()
        threading.Thread(target=self.record).start()

    def record(self):
        with sr.Microphone() as source:
            while self.is_recording:
                if not self.is_paused:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        text = self.recognizer.recognize_google(audio)
                        self.text_area.insert(tk.END, text + "\n")
                    except sr.WaitTimeoutError:
                        pass  # Ignore timeout errors and continue listening
                    except sr.UnknownValueError:
                        messagebox.showerror("Error", "Google Web Speech API could not understand the audio")
                    except sr.RequestError as e:
                        messagebox.showerror("Error", f"Could not request results from Google Web Speech API; {e}")

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.label.config(text="Listening...")
        else:
            self.is_paused = True
            self.pause_button.config(text="Resume")
            self.label.config(text="Paused")

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

    def blink_dot(self):
        if self.is_recording and not self.is_paused:
            current_color = self.dot_canvas.itemcget(self.dot, "fill")
            new_color = 'red' if current_color == 'white' else 'white'
            self.dot_canvas.itemconfig(self.dot, fill=new_color)
        else:
            self.dot_canvas.itemconfig(self.dot, fill='white')
        if self.is_recording:
            self.root.after(500, self.blink_dot)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
