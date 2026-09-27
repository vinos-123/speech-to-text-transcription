import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr


APP_TITLE = "Speech-to-Text Transcription Tool"
WINDOW_SIZE = "800x600"


def transcribe_audio():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[
            ("WAV Audio Files", "*.wav"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        status_label.config(
            text="Processing audio...",
            fg="blue"
        )
        window.update()

        recognizer = sr.Recognizer()

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, text)

        status_label.config(
            text="✓ Transcription completed successfully.",
            fg="green"
        )

    except sr.UnknownValueError:
        text_box.delete("1.0", tk.END)

        status_label.config(
            text="Speech could not be understood.",
            fg="red"
        )

        messagebox.showwarning(
            "Speech Not Recognized",
            "The audio was detected, but the speech could not be understood."
        )

    except sr.RequestError:
        status_label.config(
            text="Speech recognition service unavailable.",
            fg="red"
        )

        messagebox.showerror(
            "Service Error",
            "Could not connect to the speech recognition service.\n"
            "Please check your internet connection."
        )

    except ValueError:
        status_label.config(
            text="Unsupported audio format.",
            fg="red"
        )

        messagebox.showerror(
            "Audio Format Error",
            "Please select a WAV audio file."
        )

    except Exception as error:
        status_label.config(
            text="An unexpected error occurred.",
            fg="red"
        )

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{error}"
        )


def save_transcription():
    text = text_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "No Text",
            "There is no transcription to save."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Transcription",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt")
        ]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        status_label.config(
            text="✓ Transcription saved successfully.",
            fg="green"
        )

        messagebox.showinfo(
            "Success",
            "Transcription saved successfully."
        )

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save the file:\n\n{error}"
        )


def clear_text():
    text_box.delete("1.0", tk.END)

    status_label.config(
        text="Ready for a new transcription.",
        fg="black"
    )


# Main Window
window = tk.Tk()

window.title(APP_TITLE)
window.geometry(WINDOW_SIZE)
window.resizable(True, True)


# Title
title_label = tk.Label(
    window,
    text="Speech-to-Text Transcription",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=(25, 5))


# Subtitle
subtitle_label = tk.Label(
    window,
    text="Convert recorded speech into written text",
    font=("Arial", 12)
)

subtitle_label.pack(pady=(0, 20))


# Button Frame
button_frame = tk.Frame(window)

button_frame.pack(pady=10)


# Select Audio Button
select_button = tk.Button(
    button_frame,
    text="Select Audio File",
    command=transcribe_audio,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10
)

select_button.grid(
    row=0,
    column=0,
    padx=10
)


# Save Button
save_button = tk.Button(
    button_frame,
    text="Save Transcription",
    command=save_transcription,
    font=("Arial", 12),
    padx=20,
    pady=10
)

save_button.grid(
    row=0,
    column=1,
    padx=10
)


# Clear Button
clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_text,
    font=("Arial", 12),
    padx=20,
    pady=10
)

clear_button.grid(
    row=0,
    column=2,
    padx=10
)


# Text Box
text_box = tk.Text(
    window,
    height=18,
    width=85,
    wrap=tk.WORD,
    font=("Arial", 12)
)

text_box.pack(
    padx=30,
    pady=20,
    fill=tk.BOTH,
    expand=True
)


# Status Label
status_label = tk.Label(
    window,
    text="Ready. Select a WAV audio file.",
    font=("Arial", 11)
)

status_label.pack(
    pady=(0, 20)
)


# Start Application
window.mainloop()