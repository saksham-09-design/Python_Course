import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from gen_AI_Api import weather_API

url_current = 'http://api.weatherapi.com/v1/current.json'
url_forecast = 'http://api.weatherapi.com/v1/forecast.json'

def fetch_weather(location):
    try:
        params = {
            'key': weather_API,
            'q': location
        }
        params_forecast = {
            'key': weather_API,
            'q': location,
            'days': 3
        }

        response = requests.get(url_current, params=params).json()
        forecast_response = requests.get(url_forecast, params=params_forecast).json()

        # Clear previous content
        for widget in current_frame.winfo_children():
            widget.destroy()
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        # Current weather
        cur = response['current']
        loc = response['location']
        icon_url = "https:" + cur['condition']['icon']
        icon_img = get_icon_image(icon_url)

        tk.Label(current_frame, text=f"Weather in {loc['name']}, {loc['country']}", 
                 font=("Segoe UI", 20, "bold"), bg="#f0f8ff", fg="#333").pack(pady=(10,5))
        tk.Label(current_frame, image=icon_img, bg="#f0f8ff").pack()
        tk.Label(current_frame, text=cur['condition']['text'], 
                 font=("Segoe UI", 14), bg="#f0f8ff", fg="#444").pack()
        tk.Label(current_frame, text=f"Temperature: {cur['temp_c']}°C", 
                 font=("Segoe UI", 12), bg="#f0f8ff").pack()
        tk.Label(current_frame, text=f"Humidity: {cur['humidity']}%", 
                 font=("Segoe UI", 12), bg="#f0f8ff").pack()
        tk.Label(current_frame, text=f"Wind Speed: {cur['wind_kph']} km/h", 
                 font=("Segoe UI", 12), bg="#f0f8ff").pack()
        tk.Label(current_frame, text=f"UV Index: {cur['uv']}", 
                 font=("Segoe UI", 12), bg="#f0f8ff").pack()
        current_frame.image = icon_img

        # Forecast
        for day in forecast_response['forecast']['forecastday']:
            date = day['date']
            max_temp = day['day']['maxtemp_c']
            condition = day['day']['condition']['text']
            icon_url = "https:" + day['day']['condition']['icon']
            icon_img = get_icon_image(icon_url)

            day_frame = tk.Frame(forecast_frame, bg="#e6f0ff", bd=1, relief="solid")
            day_frame.pack(side=tk.LEFT, padx=10, pady=10)

            tk.Label(day_frame, text=date, font=("Segoe UI", 12, "bold"), bg="#e6f0ff", fg="#222").pack(pady=(5,0))
            tk.Label(day_frame, image=icon_img, bg="#e6f0ff").pack(pady=5)
            tk.Label(day_frame, text=condition, font=("Segoe UI", 11), bg="#e6f0ff", fg="#444").pack()
            tk.Label(day_frame, text=f"Max Temp: {max_temp}°C", font=("Segoe UI", 11), bg="#e6f0ff").pack()
            day_frame.image = icon_img

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather: {str(e)}")

def get_icon_image(url):
    response = requests.get(url)
    img_data = response.content
    image = Image.open(BytesIO(img_data))
    image = image.resize((60, 60), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# GUI Window Setup
root = tk.Tk()
root.title("Modern Weather App")
root.geometry("800x700")
root.configure(bg="#d6eaf8")

# Search bar
search_frame = tk.Frame(root, bg="#d6eaf8")
search_frame.pack(pady=30)

entry = tk.Entry(search_frame, font=("Segoe UI", 14), width=35)
entry.pack(side=tk.LEFT, padx=10, ipady=5)

def on_search():
    loc = entry.get().strip()
    if loc:
        fetch_weather(loc)

tk.Button(search_frame, text="Search", command=on_search, font=("Segoe UI", 12, "bold"), 
          bg="#2980b9", fg="white", padx=10, pady=2).pack(side=tk.LEFT)

# Current Weather Panel
current_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="ridge")
current_frame.pack(pady=20, ipadx=10, ipady=10)

# Forecast Panel
forecast_frame = tk.Frame(root, bg="#d6eaf8")
forecast_frame.pack(pady=10)

root.mainloop()
