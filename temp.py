import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
from gen_AI_Api import apiKey
import pyttsx3
import datetime


genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-1.5-flash")


engine = pyttsx3.init()


userPrompts = []
geminiResponses = []

def ask_gemini(prompt):
    try:
        response = model.generate_content(contents=prompt)
        return response.text.replace('**', '').replace('`', '')
    except Exception as e:
        return f"[Error from Gemini API]: {str(e)}"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def send_prompt():
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_area.insert(tk.END, f"You: {user_input}\n", "user")
    userPrompts.append(user_input)
    entry.delete(0, tk.END)

    response = ask_gemini(user_input)
    chat_area.insert(tk.END, f"Gemini: {response}\n\n", "gemini")
    geminiResponses.append(response)
    chat_area.yview(tk.END)

def save_history():
    if not userPrompts:
        messagebox.showinfo("Save History", "No history found yet.")
        return

    filename = f"Gemini_Chat_{datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"--- Conversation History at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        for u, g in zip(userPrompts, geminiResponses):
            f.write(f"\nUser: {u}\nGemini: {g}\n")

    messagebox.showinfo("Save History", f"Chat saved as '{filename}'")

def speak_response():
    if not geminiResponses:
        messagebox.showinfo("Speak", "No Gemini response to speak.")
    else:
        speak(geminiResponses[-1])


root = tk.Tk()
root.title("Gemini AI Chatbot")
root.geometry("700x600")


chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("gemini", foreground="green")
chat_area.config(state=tk.NORMAL)


entry_frame = tk.Frame(root)
entry_frame.pack(fill=tk.X, padx=10)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_btn = tk.Button(entry_frame, text="Send", command=send_prompt)
send_btn.pack(side=tk.RIGHT)


btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

save_btn = tk.Button(btn_frame, text="Save History", command=save_history, width=15)
save_btn.grid(row=0, column=0, padx=5)

speak_btn = tk.Button(btn_frame, text="Speak", command=speak_response, width=15)
speak_btn.grid(row=0, column=1, padx=5)


chat_area.insert(tk.END, "Hello Welcome Sir! How Can I assist You?\n", "gemini")

root.mainloop()
