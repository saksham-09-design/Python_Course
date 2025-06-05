import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from gemini_api import GeminiAPI
import google.generativeai as GenAI
from datetime import datetime
import pyttsx3

# Configure Gemini API
client = GenAI.configure(api_key=GeminiAPI)
model = GenAI.GenerativeModel("gemini-1.5-flash")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# History storage
userPrompts = []
chintuResponse = []
lastResponse = ""  # Track last response for read aloud

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to send user input to Gemini and display result
def send_prompt():
    global lastResponse
    prompt = input_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    input_area.delete("1.0", tk.END)

    userPrompts.append(prompt)
    try:
        response = model.generate_content(prompt).text.replace("**", "")
    except Exception as e:
        response = "Sorry, an error occurred while fetching the response."
    
    chintuResponse.append(response)
    lastResponse = response

    chat_window.configure(state='normal')
    chat_window.insert(tk.END, f"User: {prompt}\n\nChintu: {response}\n\n")
    chat_window.configure(state='disabled')
    chat_window.see(tk.END)

# Function to save history to file
def save_history():
    if not userPrompts:
        messagebox.showinfo("No History", "No conversation to save.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile=f"Chintu_Response_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    )

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Your Conversation with Chintu at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            for i in range(len(userPrompts)):
                file.write(f"\nUser: {userPrompts[i]}\n")
                file.write(f"Chintu: {chintuResponse[i]}\n")
        messagebox.showinfo("Success", f"History saved to {filename}")

# Function to read aloud last response
def read_aloud():
    if lastResponse:
        speak(lastResponse)
    else:
        messagebox.showinfo("Nothing to Read", "No response to read aloud yet.")

# Set up GUI
root = tk.Tk()
root.title("Chintu - Gemini AI Chatbot")
root.geometry("700x600")
root.resizable(False, False)

# Chat history area
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state="disabled")
chat_window.place(x=20, y=20, width=660, height=380)

# Input area
input_area = tk.Text(root, height=4, wrap=tk.WORD, font=("Arial", 12))
input_area.place(x=20, y=420, width=500, height=80)

# Send button
send_button = tk.Button(root, text="Send", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=send_prompt)
send_button.place(x=540, y=420, width=140, height=35)

# Read Aloud button
read_button = tk.Button(root, text="Read Aloud", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=read_aloud)
read_button.place(x=540, y=465, width=140, height=35)

# Save History button
save_button = tk.Button(root, text="Save History", font=("Arial", 12, "bold"), bg="#FF9800", fg="white", command=save_history)
save_button.place(x=540, y=510, width=140, height=35)

root.mainloop()
