from tkinter import *
from tkinter import ttk
import requests
from tkinter import messagebox

def data_get():
    try:
        city = city_name.get()
        if not city:
            messagebox.showwarning("Warning", "Please select or enter a city name!")
            return
        data = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=04c18249cf61b56960f41cff97dcc544").json()
        w_label1.config(text = data["weather"][0]["main"])
        wb_label1.config(text = data["weather"][0]["description"])
        temp_label1.config(text = str(int(data["main"]["temp"]-273.15)) + "°C")
        per_label1.config(text = str(data["main"]["pressure"]) + " mb")
    except:
        messagebox.showerror("Error", "City not found or API error!")


# Main Window
win = Tk()
win.title("Kylarfu - Weather App")
win.geometry("500x570")

# Modern Color Scheme
bg_color = "#1a1a2e"
primary_color = "#16213e"
accent_color = "#0f3460"
text_color = "#eaeaea"
highlight_color = "#e94560"
success_color = "#00d4ff"

win.config(bg=bg_color)
win.resizable(False, False)

# Title Frame
title_frame = Frame(win, bg=primary_color, height=80)
title_frame.pack(fill=X, padx=0, pady=0)

name_label = Label(title_frame, text="🌤️ Kylarfu Weather", font=("Segoe UI", 26, "bold"), 
                   bg=primary_color, fg=highlight_color)
name_label.pack(pady=15)

subtitle_label = Label(title_frame, text="Real-time Weather Check", font=("Segoe UI", 9), 
                       bg=primary_color, fg=success_color)
subtitle_label.pack(pady=(0, 10))

# Input Section
input_frame = Frame(win, bg=bg_color)
input_frame.pack(fill=X, padx=15, pady=12)

city_label = Label(input_frame, text="📍 Select or Enter City:", font=("Segoe UI", 10, "bold"), 
                   bg=bg_color, fg=text_color)
city_label.pack(anchor=W, pady=(0, 6))

city_name = StringVar()
list_name = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
             "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
             "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
             "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
             "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
             "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
             "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
             "Wisconsin", "Wyoming"]

style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', 
                fieldbackground=accent_color,
                background=accent_color,
                foreground=text_color,
                font=("Segoe UI", 10))

com = ttk.Combobox(input_frame, textvariable=city_name, values=list_name, 
                   font=("Segoe UI", 10), state="normal", width=35)
com.pack(fill=X, ipady=6)

# Button
button_frame = Frame(win, bg=bg_color)
button_frame.pack(fill=X, padx=15, pady=10)

done_button = Button(button_frame, text="🔍 SEARCH WEATHER", font=("Segoe UI", 11, "bold"), 
                     command=data_get, bg=highlight_color, fg="white", 
                     activebackground="#ff6b7a", activeforeground="white",
                     border=0, cursor="hand2", padx=20, pady=8)
done_button.pack(fill=X, ipady=3)

# Results Frame with Scrollbar
results_outer_frame = Frame(win, bg=primary_color, relief=FLAT, bd=0)
results_outer_frame.pack(fill=BOTH, expand=True, padx=12, pady=12)

# Canvas and Scrollbar
canvas = Canvas(results_outer_frame, bg=primary_color, highlightthickness=0)
scrollbar = Scrollbar(results_outer_frame, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas, bg=primary_color)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Mouse wheel scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Weather Info Cards
def create_info_card(parent, icon, title):
    card = Frame(parent, bg=accent_color, relief=FLAT, bd=0)
    card.pack(fill=X, pady=5, padx=0)
    
    title_label = Label(card, text=f"{icon} {title}", font=("Segoe UI", 9, "bold"), 
                        bg=accent_color, fg=success_color, anchor=W)
    title_label.pack(anchor=W, padx=12, pady=(8, 2))
    
    value_label = Label(card, text="--", font=("Segoe UI", 16, "bold"), 
                        bg=accent_color, fg=highlight_color, anchor=W)
    value_label.pack(anchor=W, padx=12, pady=(2, 8))
    
    return value_label

# Create Info Cards
w_label1 = create_info_card(scrollable_frame, "☁️", "Weather Condition")
wb_label1 = create_info_card(scrollable_frame, "📝", "Description")
temp_label1 = create_info_card(scrollable_frame, "🌡️", "Temperature")
per_label1 = create_info_card(scrollable_frame, "🔐", "Pressure")

# Footer
footer = Label(win, text="Powered by OpenWeather API", 
               font=("Segoe UI", 8), bg=bg_color, fg="#666666")
footer.pack(pady=5)

win.mainloop()