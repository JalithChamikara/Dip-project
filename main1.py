import tkinter as tk
from tkinter import filedialog, ttk
from app import (
    add_image, auto_contrast, auto_sharpen, auto_cartoon, auto_invert, bypass_censorship, rotate_image, crop_image,
    change_brightness, change_contrast, change_saturation, apply_color_mask, detect_faces
)  # Import your functions

# Initialize the main application window
root = tk.Tk()
root.geometry("1000x600")
root.title("Image Editor")
root.config(bg="#2e2e2e")

# Create the main frame to hold the left and canvas frames
main_frame = ttk.Frame(root)
main_frame.pack(side="top", fill="both", expand=True)

# Create the left frame
left_frame = ttk.Frame(main_frame, width=350)
left_frame.pack(side="left", fill="y")
left_frame.config(style="TFrame")

# Add buttons and bind them to the functions
button_texts = [
    ("Open Image", lambda: add_image(canvas)),
    ("Auto Invert", lambda: auto_invert(canvas)),
    ("Bypass Censorship", lambda: bypass_censorship(canvas)),
    ("Rotate Image", lambda: rotate_image(canvas)),
    ("Crop Image", lambda: crop_image(canvas)),
    ("Change Brightness", lambda: change_brightness(canvas)),
    ("Change Contrast", lambda: change_contrast(canvas)),
    ("Change Saturation", lambda: change_saturation(canvas)),
    ("Color Mask", lambda: apply_color_mask(canvas)),
    ("Face Detection", lambda: detect_faces(canvas))
]

for idx, (text, command) in enumerate(button_texts):
    button = ttk.Button(left_frame, text=text, command=command, style="Custom.TButton")
    button.pack(pady=0.5, padx=5, fill='both')

# Create the canvas frame (right side)
canvas_frame = ttk.Frame(main_frame)
canvas_frame.pack(side="right", fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, bg="#3c3f41")
canvas.pack(fill="both", expand=True)

# Create the bottom frame for the slider
bottom_frame = ttk.Frame(root, height=50)
bottom_frame.pack(side="bottom", fill="x", pady=10)
bottom_frame.config(style="TFrame")

# Variable to keep track of the selected adjustment type
adjustment_type = tk.StringVar(value="brightness")

# Style for the slider
style = ttk.Style()
style.theme_use('clam')
style.configure("TScale", background="#2e2e2e", troughcolor="#555555", sliderthickness=15, sliderlength=20)
style.configure("TButton", font=("Arial", 10), padding=10, background="#3c3f41", foreground="#ffffff")
style.configure("Custom.TButton", font=("Arial", 10), padding=10, background="#3c3f41", foreground="#ffffff")
style.map("Custom.TButton", background=[("active", "#4e5052")])
style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", font=("Arial", 12), background="#2e2e2e", foreground="#ffffff")
style.configure("TEntry", fieldbackground="#3c3f41", background="#3c3f41", foreground="#ffffff")

# Single slider for adjustment
adjustment_slider = ttk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=800)
adjustment_slider.set(50)
adjustment_slider.pack(side="left", padx=100)

# Slider value display
slider_value_label = ttk.Label(bottom_frame, text="50", style="TLabel")
slider_value_label.pack(side="left", padx=10)

def update_slider_value(event):
    slider_value_label.config(text=str(int(adjustment_slider.get())))

adjustment_slider.bind("<Motion>", update_slider_value)

# Center the image in the canvas
def center_image():
    if canvas.image:
        canvas.create_image(
            canvas.winfo_width() // 2, 
            canvas.winfo_height() // 2, 
            image=canvas.image, 
            anchor="center"
        )

canvas.bind("<Configure>", lambda e: center_image())

root.mainloop()
