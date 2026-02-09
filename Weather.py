import tkinter as tk
from tkinter import messagebox

try:
    import requests
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def get_weather():
    # Get city name from the input field
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    # You need to replace this with your actual OpenWeatherMap API key
    # You can get one for free at https://openweathermap.org/api
    api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    # URL to fetch data from
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Complete url with city and api key (units=metric gives Celsius)
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    try:
        # Request data from the server
        response = requests.get(complete_url, timeout=10)
        data = response.json()
        
        # Check if city is found (cod 200 means success)
        if data["cod"] != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]
            
            # Extracting specific info
            temp = main_data["temp"]
            humidity = main_data["humidity"]
            description = weather_data["description"]
            
            # Update the result label
            result_text = (f"Temperature: {temp}°C\n"
                           f"Humidity: {humidity}%\n"
                           f"Condition: {description.capitalize()}")
            result_label.config(text=result_text)
            
        else:
            messagebox.showerror("Error", "City not found! Please check the spelling.")
    
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", "No internet connection!\nPlease check your network and try again.")
    except requests.exceptions.Timeout:
        messagebox.showerror("Timeout Error", "Request timed out!\nServer is taking too long to respond.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Network error occurred:\n{e}")
    except KeyError:
        messagebox.showerror("API Error", "Invalid API response. The API key may be invalid or expired.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App")
root.geometry("350x400")
root.config(bg="#f0f0f0")

# Heading
title_label = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Input Field
city_entry = tk.Entry(root, font=("Helvetica", 14), width=20)
city_entry.pack(pady=10)

# Search Button
search_button = tk.Button(root, text="Check Weather", font=("Helvetica", 12), command=get_weather)
search_button.pack(pady=10)

# Display Result
result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0", justify="left")
result_label.pack(pady=30)

# Start the app
root.mainloop()